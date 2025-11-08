# Row-Level Security Policy Checks - User Guide

## Table of Contents

1. [Overview](#overview)
2. [Problem Statement](#problem-statement)
3. [Solution](#solution)
4. [Installation](#installation)
5. [Configuration](#configuration)
6. [Usage](#usage)
7. [Examples](#examples)
8. [Troubleshooting](#troubleshooting)
9. [Best Practices](#best-practices)
10. [FAQ](#faq)

## Overview

The row-level security policy checks enforce team-based access control on shared configuration tables in your database. They prevent teams from accidentally or intentionally modifying records that don't belong to them.

**Key Features:**
- Validates INSERT, UPDATE, and DELETE operations
- Environment variable-based team identification
- Configurable table and column names
- Two implementation options (basic pattern matching or advanced SQL parsing)
- Blocks deployments that violate team boundaries

## Problem Statement

In organizations with shared configuration tables accessed by multiple teams, developers occasionally:

- Copy scripts from other teams
- Modify records belonging to different teams
- Delete configuration data used by other teams' jobs
- Cause production issues when framework jobs fail

**Example:**
```sql
-- Risk developer copies IoT script
UPDATE FRAMEWORK_CONFIG
SET enabled = 0
WHERE job_name = 'iot_daily_batch';  -- Accidentally disables IoT's job!
```

## Solution

These policy checks validate that all DML operations on protected tables include proper team filtering:

**For INSERT:**
```sql
-- Required: Team column with correct value
INSERT INTO FRAMEWORK_CONFIG (job_name, SOURCE, enabled)
VALUES ('my_job', 'RISK', 1);  -- SOURCE must match TEAM_ID
```

**For UPDATE/DELETE:**
```sql
-- Required: WHERE clause with team filtering
UPDATE FRAMEWORK_CONFIG
SET enabled = 1
WHERE job_name = 'my_job' AND SOURCE = 'RISK';  -- Must filter by SOURCE

DELETE FROM FRAMEWORK_CONFIG
WHERE status = 'OBSOLETE' AND SOURCE = 'RISK';  -- Must filter by SOURCE
```

## Installation

### Prerequisites

- Liquibase Pro 4.20+ (for Python script support)
- Python 3.8+ (provided by Liquibase GraalPy runtime)
- Liquibase license key set in environment

### Files Required

Copy these files to your Liquibase project:

**For Basic Check (Pattern Matching):**
```
Python/Scripts/Any/row_level_security_basic.py
```

**For Advanced Check (SQL Parsing):**
```
Python/Scripts/Any/row_level_security_advanced.py
```

**Tests (Optional):**
```
Python/tests/test_row_level_security_basic.py
Python/tests/test_row_level_security_advanced.py
```

**Examples (Optional):**
```
Python/Changesets/row_level_security/passing_examples.sql
Python/Changesets/row_level_security/failing_examples.sql
Python/Changesets/row_level_security/README.md
```

## Configuration

### Step 1: Enable Script Execution

Liquibase requires this environment variable to run Python checks:

```bash
export LIQUIBASE_COMMAND_CHECKS_RUN_CHECKS_SCRIPTS_ENABLED='true'
```

### Step 2: Customize the Check

```bash
liquibase checks customize --check-name=CustomCheckTemplate
```

When prompted, provide:

**Script Path:**
```
Python/Scripts/Any/row_level_security_basic.py
```
(or `row_level_security_advanced.py` for the advanced version)

**Script Arguments:**
```
ENV_VAR_NAME=TEAM_ID,PROTECTED_TABLES=FRAMEWORK_CONFIG,JOB_DEFINITIONS,SHARED_PARAMETERS,TEAM_COLUMN=SOURCE
```

**Message Template:**
```
Row-level security violation: __OPERATION__ on table __TABLE_NAME__ must filter by __TEAM_COLUMN__ = '__TEAM_VALUE__'
```

**Severity:**
```
ERROR
```
(or WARNING for audit-only mode)

### Step 3: Set Team Identifier

Before each deployment, set the environment variable:

```bash
# For Risk team
export TEAM_ID=RISK

# For Trading team
export TEAM_ID=TRADING

# For IoT team
export TEAM_ID=IOT
```

## Usage

### Running Checks

**Check without deployment:**
```bash
liquibase checks run --changelog-file=my_changelog.sql
```

**Check and deploy:**
```bash
liquibase update --changelog-file=my_changelog.sql
```
(Checks run automatically before update)

### CI/CD Integration

**GitHub Actions:**
```yaml
name: Deploy Database Changes

on:
  push:
    branches: [main]

jobs:
  deploy-risk-team:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Setup Liquibase
        uses: liquibase/setup-liquibase@v1
        with:
          edition: 'pro'

      - name: Deploy Changes
        env:
          TEAM_ID: RISK
          LIQUIBASE_COMMAND_CHECKS_RUN_CHECKS_SCRIPTS_ENABLED: 'true'
          LIQUIBASE_LICENSE_KEY: ${{ secrets.LIQUIBASE_LICENSE_KEY }}
        run: |
          liquibase update --changelog-file=risk_team_changes.sql
```

**Jenkins:**
```groovy
pipeline {
    agent any

    environment {
        TEAM_ID = 'RISK'
        LIQUIBASE_COMMAND_CHECKS_RUN_CHECKS_SCRIPTS_ENABLED = 'true'
        LIQUIBASE_LICENSE_KEY = credentials('liquibase-license')
    }

    stages {
        stage('Deploy Database Changes') {
            steps {
                sh '''
                    liquibase checks run --changelog-file=risk_team_changes.sql
                    liquibase update --changelog-file=risk_team_changes.sql
                '''
            }
        }
    }
}
```

**Azure DevOps:**
```yaml
trigger:
  - main

variables:
  TEAM_ID: 'RISK'
  LIQUIBASE_COMMAND_CHECKS_RUN_CHECKS_SCRIPTS_ENABLED: 'true'

steps:
- task: Bash@3
  displayName: 'Deploy Database Changes'
  inputs:
    targetType: 'inline'
    script: |
      liquibase update --changelog-file=risk_team_changes.sql
  env:
    LIQUIBASE_LICENSE_KEY: $(LiquibaseLicenseKey)
```

## Examples

### Example 1: Valid Risk Team Deployment

```sql
--changeset risk_team:1
-- Valid: Includes SOURCE = 'RISK'
INSERT INTO FRAMEWORK_CONFIG (job_name, SOURCE, enabled, created_date)
VALUES ('risk_daily_calculation', 'RISK', 1, CURRENT_DATE);

--changeset risk_team:2
-- Valid: WHERE clause filters by SOURCE = 'RISK'
UPDATE FRAMEWORK_CONFIG
SET enabled = 1,
    last_modified = CURRENT_TIMESTAMP
WHERE job_name = 'risk_daily_calculation'
  AND SOURCE = 'RISK';

--changeset risk_team:3
-- Valid: DELETE includes SOURCE = 'RISK' filter
DELETE FROM JOB_DEFINITIONS
WHERE status = 'OBSOLETE'
  AND SOURCE = 'RISK';
```

**Deployment:**
```bash
export TEAM_ID=RISK
export LIQUIBASE_COMMAND_CHECKS_RUN_CHECKS_SCRIPTS_ENABLED='true'
liquibase update --changelog-file=risk_changes.sql
```

**Result:** ✅ Deployment succeeds

### Example 2: Invalid Deployment (Violation)

```sql
--changeset risk_team:1
-- VIOLATION: Missing SOURCE column
INSERT INTO FRAMEWORK_CONFIG (job_name, enabled)
VALUES ('some_job', 1);

--changeset risk_team:2
-- VIOLATION: WHERE clause doesn't include SOURCE = 'RISK'
UPDATE FRAMEWORK_CONFIG
SET enabled = 0
WHERE job_name = 'some_job';

--changeset risk_team:3
-- VIOLATION: No WHERE clause at all!
DELETE FROM FRAMEWORK_CONFIG;
```

**Deployment:**
```bash
export TEAM_ID=RISK
liquibase update --changelog-file=invalid_changes.sql
```

**Result:** ❌ Deployment blocked with error:
```
Row-level security violation: INSERT on table FRAMEWORK_CONFIG must filter by SOURCE = 'RISK'
```

## Troubleshooting

### Check Not Running

**Symptom:** No validation occurs, changes deploy without checking

**Possible Causes:**
1. Script execution not enabled
2. Check not enabled in Liquibase
3. Wrong Liquibase version

**Solutions:**
```bash
# Verify script execution enabled
echo $LIQUIBASE_COMMAND_CHECKS_RUN_CHECKS_SCRIPTS_ENABLED

# List enabled checks
liquibase checks show

# Enable the check
liquibase checks enable --check-name=<your-check-name>

# Verify Liquibase version
liquibase --version  # Should be 4.20+ for Python support
```

### Environment Variable Not Set

**Symptom:** Check logs warning about missing environment variable and is skipped

**Solution:**
```bash
# Set the variable
export TEAM_ID=RISK

# Verify it's set
env | grep TEAM_ID

# Re-run deployment
liquibase update
```

### False Positives (Valid SQL Flagged)

**Symptom:** Valid SQL with proper team filtering is flagged as a violation

**Possible Causes:**
1. Basic check struggles with complex SQL
2. Column name mismatch
3. Case sensitivity issues

**Solutions:**

**Try Advanced Check:**
```bash
# Switch to advanced check for better SQL parsing
# In checks configuration, change script path to:
# Python/Scripts/Any/row_level_security_advanced.py
```

**Verify Configuration:**
```bash
# Check that column name matches your schema
liquibase checks show --check-name=<your-check-name>

# Verify TEAM_COLUMN argument matches actual column name
# If your column is "SUBSYSTEM" but config says "SOURCE", it will fail
```

### False Negatives (Violations Not Caught)

**Symptom:** Invalid SQL passes the check when it shouldn't

**Possible Causes:**
1. Table not in PROTECTED_TABLES list
2. Wrong team identifier value
3. Complex SQL patterns not detected by basic check

**Solutions:**

**Verify Protected Tables:**
```bash
# List should include the table in question
liquibase checks show --check-name=<your-check-name>
```

**Use Advanced Check:**
```bash
# For complex SQL, use the advanced parsing version
# Change script path to: Python/Scripts/Any/row_level_security_advanced.py
```

## Best Practices

### 1. Start with Audit Mode

When first rolling out, use WARNING severity to identify violations without blocking:

```bash
liquibase checks customize --check-name=<your-check-name>
# Set severity to: WARNING

# Monitor logs for violations
liquibase update --log-level=INFO
```

After fixing violations, increase to ERROR severity.

### 2. Standardize Column Names

Use the same team identifier column across all protected tables:

```sql
-- Good: Consistent column name
CREATE TABLE FRAMEWORK_CONFIG (
    job_name VARCHAR(100),
    SOURCE VARCHAR(50),  -- Team identifier
    enabled BIT
);

CREATE TABLE JOB_DEFINITIONS (
    job_id INT,
    SOURCE VARCHAR(50),  -- Same column name
    description VARCHAR(500)
);
```

### 3. CI/CD Best Practices

**Per-Team Pipelines:**
```yaml
# Separate pipeline per team
jobs:
  deploy-risk:
    env:
      TEAM_ID: RISK
    steps:
      - run: liquibase update --changelog-file=risk/

  deploy-trading:
    env:
      TEAM_ID: TRADING
    steps:
      - run: liquibase update --changelog-file=trading/
```

**Branch Protection:**
- Require checks to pass before merging
- Prevent force-pushing to protected branches
- Require code review for changelog changes

### 4. Choose the Right Check Version

| Scenario | Recommended Check |
|----------|-------------------|
| Simple DML, standard SQL patterns | Basic (pattern matching) |
| Complex SQL, subqueries, CTEs | Advanced (SQL parsing) |
| Maximum performance | Basic |
| Maximum accuracy | Advanced |
| Initial rollout/testing | Basic (faster feedback) |
| Production enforcement | Advanced (fewer false positives) |

### 5. Documentation

Document your team's protected tables and conventions:

```markdown
# Our Protected Tables

| Table | Team Column | Purpose |
|-------|-------------|---------|
| FRAMEWORK_CONFIG | SOURCE | Framework job configurations |
| JOB_DEFINITIONS | SOURCE | Batch job definitions |
| SHARED_PARAMETERS | SUBSYSTEM | System parameters |

# Team Identifiers
- Risk: RISK
- Trading: TRADING
- IoT: IOT
- Compliance: COMPLIANCE
```

## FAQ

**Q: Can we use different column names for different tables?**

A: Not in the current version. All protected tables must use the same team identifier column name. Future enhancement: per-table column mapping.

**Q: What about SELECT statements?**

A: SELECT operations are not validated. Teams can read all configuration data for reporting and cross-team visibility.

**Q: Can we allow specific cross-team operations?**

A: Not currently. All DML on protected tables must filter by the deploying team. Future enhancement: whitelist patterns for approved cross-team operations.

**Q: How do we handle legitimate cross-team changes?**

A: Options:
1. Manual review process with elevated privileges
2. Dedicated "admin" team identifier for cross-team operations
3. Temporarily disable check for specific changesets (not recommended)

**Q: Does this work with all databases?**

A: Yes, the checks are database-agnostic. They analyze SQL syntax, not database-specific features.

**Q: Performance impact?**

A: Minimal. Checks run during validation phase, adding seconds to deployment time. Advanced check is ~10-20% slower than basic due to SQL parsing.

**Q: Can we run both basic and advanced checks?**

A: Not recommended. Choose one check per protected tables list. Running both would duplicate validation and potentially conflict.

**Q: How do we test changes before deployment?**

A: Use `liquibase checks run` to validate without deploying:
```bash
liquibase checks run --changelog-file=my_changes.sql
```

## Additional Resources

- Design Document: `docs/plans/2025-11-07-row-level-security-design.md`
- Sample Changesets: `Python/Changesets/row_level_security/`
- Test Suite: `Python/tests/test_row_level_security_*.py`
- Liquibase Policy Checks: https://docs.liquibase.com/policy-checks
