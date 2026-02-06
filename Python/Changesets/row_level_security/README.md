# Row-Level Security Policy Check Examples

This directory contains sample changesets demonstrating the row-level security policy checks.

## Overview

The row-level security policy checks enforce team-based access control on shared configuration tables. They ensure that teams can only perform DML operations (INSERT, UPDATE, DELETE) on records that belong to them.

## Available Checks

### 1. `row_level_security_basic.py` - Pattern Matching

**Implementation:** Uses string patterns and regex to validate SQL
**Performance:** Fast
**Accuracy:** ~80-85% (good for standard SQL)
**Best For:** Organizations with straightforward SQL patterns

### 2. `row_level_security_advanced.py` - SQL Parsing

**Implementation:** Uses sqlparse library for semantic analysis
**Performance:** Slightly slower
**Accuracy:** ~95% (handles complex SQL)
**Best For:** Organizations with complex SQL or requiring high accuracy

## Sample Changesets

### `passing_examples.sql`

Contains valid changesets that comply with row-level security requirements:
- INSERTs with correct team column and value
- UPDATEs with proper WHERE clause filtering
- DELETEs with proper WHERE clause filtering
- Operations on non-protected tables

**Run these to see successful deployments:**
```bash
export TEAM_ID=RISK
liquibase update --changelog-file=Python/Changesets/row_level_security/passing_examples.sql
```

### `failing_examples.sql`

Contains invalid changesets that violate row-level security (for educational purposes):
- INSERTs missing team column
- INSERTs with wrong team value
- UPDATEs without team filtering
- DELETEs without team filtering
- Dangerous operations (no WHERE clause, OR conditions)

**⚠️ WARNING: These will fail the policy check and block deployment!**

## Configuration

### Enable the Check

```bash
# Basic version (pattern matching)
liquibase checks customize --check-name=CustomCheckTemplate

# When prompted, configure:
# - Script Path: Python/Scripts/Any/row_level_security_basic.py
# - Script Arguments:
#     ENV_VAR_NAME=TEAM_ID
#     PROTECTED_TABLES=FRAMEWORK_CONFIG,JOB_DEFINITIONS,SHARED_PARAMETERS
#     TEAM_COLUMN=SOURCE
# - Message Template:
#     Row-level security violation: __OPERATION__ on table __TABLE_NAME__ must filter by __TEAM_COLUMN__ = '__TEAM_VALUE__'
```

### Set Environment Variable

The check identifies the deploying team via environment variable:

```bash
# For RISK team
export TEAM_ID=RISK

# For TRADING team
export TEAM_ID=TRADING

# For IoT team
export TEAM_ID=IOT
```

### Enable Script Execution

Liquibase requires enabling script execution for Python checks:

```bash
export LIQUIBASE_COMMAND_CHECKS_RUN_CHECKS_SCRIPTS_ENABLED='true'
```

## Example Scenarios

### Scenario 1: Risk Team Deployment

```bash
# Set team identifier
export TEAM_ID=RISK
export LIQUIBASE_COMMAND_CHECKS_RUN_CHECKS_SCRIPTS_ENABLED='true'

# This will PASS - proper team filtering
liquibase update --changelog-file=<(cat <<'EOF'
--changeset risk:1
INSERT INTO FRAMEWORK_CONFIG (job_name, SOURCE, enabled)
VALUES ('risk_calculator', 'RISK', 1);

UPDATE FRAMEWORK_CONFIG
SET enabled = 1
WHERE job_name = 'risk_calculator' AND SOURCE = 'RISK';
EOF
)

# This will FAIL - missing team filtering
liquibase update --changelog-file=<(cat <<'EOF'
--changeset risk:1
UPDATE FRAMEWORK_CONFIG
SET enabled = 0
WHERE job_name = 'some_job';  -- Missing SOURCE = 'RISK'
EOF
)
```

### Scenario 2: CI/CD Integration

**GitHub Actions:**
```yaml
jobs:
  deploy-risk-team:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy Risk Team Changes
        env:
          TEAM_ID: RISK
          LIQUIBASE_COMMAND_CHECKS_RUN_CHECKS_SCRIPTS_ENABLED: 'true'
        run: |
          liquibase checks run
          liquibase update --changelog-file=risk_team_changes.sql
```

**Jenkins:**
```groovy
pipeline {
    agent any
    environment {
        TEAM_ID = 'RISK'
        LIQUIBASE_COMMAND_CHECKS_RUN_CHECKS_SCRIPTS_ENABLED = 'true'
    }
    stages {
        stage('Deploy') {
            steps {
                sh 'liquibase checks run'
                sh 'liquibase update --changelog-file=risk_team_changes.sql'
            }
        }
    }
}
```

## Validation Rules

### INSERT Statements

**Required:** Team column must be present with correct value

✅ **Valid:**
```sql
INSERT INTO FRAMEWORK_CONFIG (job_name, SOURCE, enabled)
VALUES ('my_job', 'RISK', 1);
```

❌ **Invalid:**
```sql
-- Missing team column
INSERT INTO FRAMEWORK_CONFIG (job_name, enabled)
VALUES ('my_job', 1);

-- Wrong team value
INSERT INTO FRAMEWORK_CONFIG (job_name, SOURCE, enabled)
VALUES ('my_job', 'TRADING', 1);

-- NULL team value
INSERT INTO FRAMEWORK_CONFIG (job_name, SOURCE, enabled)
VALUES ('my_job', NULL, 1);
```

### UPDATE Statements

**Required:** WHERE clause must include `team_column = 'team_value'`

✅ **Valid:**
```sql
UPDATE FRAMEWORK_CONFIG
SET enabled = 1
WHERE job_name = 'my_job' AND SOURCE = 'RISK';
```

❌ **Invalid:**
```sql
-- Missing team filter
UPDATE FRAMEWORK_CONFIG
SET enabled = 0
WHERE job_name = 'my_job';

-- No WHERE clause at all
UPDATE FRAMEWORK_CONFIG
SET enabled = 1;

-- Wrong team value
UPDATE FRAMEWORK_CONFIG
SET enabled = 1
WHERE job_name = 'my_job' AND SOURCE = 'TRADING';
```

### DELETE Statements

**Required:** WHERE clause must include `team_column = 'team_value'`

✅ **Valid:**
```sql
DELETE FROM FRAMEWORK_CONFIG
WHERE job_name = 'obsolete_job' AND SOURCE = 'RISK';
```

❌ **Invalid:**
```sql
-- Missing team filter
DELETE FROM FRAMEWORK_CONFIG
WHERE job_name = 'obsolete_job';

-- No WHERE clause (very dangerous!)
DELETE FROM FRAMEWORK_CONFIG;

-- Wrong team value
DELETE FROM FRAMEWORK_CONFIG
WHERE job_name = 'obsolete_job' AND SOURCE = 'IOT';
```

## Troubleshooting

### Check Not Firing

**Problem:** Valid violations aren't being caught

**Solutions:**
1. Verify script execution is enabled:
   ```bash
   echo $LIQUIBASE_COMMAND_CHECKS_RUN_CHECKS_SCRIPTS_ENABLED
   ```

2. Check environment variable is set:
   ```bash
   echo $TEAM_ID
   ```

3. Verify table is in PROTECTED_TABLES list

4. Check Liquibase logs for warnings

### Check Firing on Valid SQL

**Problem:** Valid SQL is being flagged as a violation

**Solutions:**
1. **Basic check:** May have false positives on complex SQL
   - Try the advanced check instead (`row_level_security_advanced.py`)

2. **Verify team column name matches configuration:**
   - If your column is `SUBSYSTEM` but config says `SOURCE`, it will fail

3. **Case sensitivity:** Column names and values should be compared case-insensitively
   - Both `SOURCE` and `source` should work

### Environment Variable Not Set

**Problem:** Check is skipped with warning about missing environment variable

**Solution:**
```bash
# Set the environment variable before running Liquibase
export TEAM_ID=RISK

# Verify it's set
env | grep TEAM_ID
```

## Advanced Usage

### Using Different Environment Variables

You can configure different environment variable names per check instance:

```bash
# For one team using TEAM_ID
export TEAM_ID=RISK

# For another using DEPLOYMENT_SOURCE
export DEPLOYMENT_SOURCE=TRADING

# Configure check to use DEPLOYMENT_SOURCE
# Script Arguments: ENV_VAR_NAME=DEPLOYMENT_SOURCE,...
```

### Multiple Team Columns

If different protected tables use different column names, you currently need to:
1. Use separate check instances for each column name, OR
2. Standardize on one column name across all protected tables

**Future Enhancement:** Per-table column mapping

### Audit Mode

To log violations without blocking (for initial rollout):
1. Set severity to INFO or WARNING instead of ERROR
2. Monitor logs to identify violations
3. Fix violations in code
4. Increase severity to ERROR for enforcement

## Testing

Run the test suite to validate the checks:

```bash
# Basic check tests
python3 -m pytest Python/tests/test_row_level_security_basic.py -v

# Advanced check tests
python3 -m pytest Python/tests/test_row_level_security_advanced.py -v

# Run only pure Python tests (faster)
python3 -m pytest Python/tests/test_row_level_security_*.py -m pure_python -v

# Run integration tests (requires Liquibase)
python3 -m pytest Python/tests/test_row_level_security_*.py -m integration -v
```

## Support

For questions or issues:
1. Review the design document: `docs/plans/2025-11-07-row-level-security-design.md`
2. Check test examples: `Python/tests/test_row_level_security_*.py`
3. Review your organization's database governance policies
