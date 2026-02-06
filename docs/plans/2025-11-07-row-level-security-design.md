# Row-Level Security Policy Check Design

**Date:** 2025-11-07
**Status:** Approved
**Target:** Shared configuration tables

## Problem Statement

Organizations with shared configuration tables accessed by multiple vertical teams (Risk, IoT, PCM, etc.) need to ensure each team only performs DML operations on records where a specific column matches their team identifier.

**Current Issue:** Developers occasionally copy scripts from other teams and accidentally modify records belonging to different teams. This causes production issues when framework jobs fail because their configuration records were deleted or updated by someone from another team.

**Example Scenario:**
- Risk developer copies a script from IoT team
- Script contains: `UPDATE FRAMEWORK_CONFIG SET enabled = 0 WHERE job_name = 'iot_daily_batch'`
- Risk developer runs it, disabling IoT's job
- IoT framework job fails in production

## Requirements

### Functional Requirements
1. Validate that INSERT/UPDATE/DELETE operations on protected tables only affect records belonging to the deploying team
2. Identify deploying team via environment variable
3. Support configurable list of protected tables
4. Support configurable team identifier column name (same across all protected tables)
5. Block deployments on violations (ERROR severity)

### Non-Functional Requirements
1. Database-agnostic (works with SQL Server, Oracle, Databricks)
2. Testable with existing Python test harness
3. Clear, actionable error messages
4. Minimal performance overhead
5. Easy to configure and maintain

## Solution Design

### Team Identification
- Use environment variable to identify deploying team (e.g., `TEAM_ID=RISK`)
- Environment variable name is configurable when enabling the check
- CI/CD pipelines set this variable before Liquibase deployment
- Check fails gracefully if environment variable is not set

### Configuration Parameters

When enabling the check, users configure:

| Parameter | Description | Example |
|-----------|-------------|---------|
| `ENV_VAR_NAME` | Environment variable containing team identifier | `TEAM_ID` or `DEPLOYMENT_SOURCE` |
| `PROTECTED_TABLES` | Comma-separated list of tables requiring row-level security | `FRAMEWORK_CONFIG,JOB_DEFINITIONS,SHARED_PARAMETERS` |
| `TEAM_COLUMN` | Column name identifying record ownership | `SOURCE` or `SUBSYSTEM` |

### Validation Rules

**INSERT Statements:**
- Must include team column in insert
- Team column value must match environment variable value
- Example: `INSERT INTO FRAMEWORK_CONFIG (job_name, SOURCE, ...) VALUES ('my_job', 'RISK', ...)`

**UPDATE Statements:**
- WHERE clause must include `team_column = 'team_value'`
- Example: `UPDATE FRAMEWORK_CONFIG SET enabled = 1 WHERE job_name = 'my_job' AND SOURCE = 'RISK'`

**DELETE Statements:**
- WHERE clause must include `team_column = 'team_value'`
- Example: `DELETE FROM FRAMEWORK_CONFIG WHERE job_name = 'my_job' AND SOURCE = 'RISK'`

**SELECT Statements:**
- Not validated (teams can read all configuration data)

## Implementation Approaches

We will provide two implementations as working demonstrations:

### Approach 1: Pattern Matching (Basic)

**File:** `Python/Scripts/Any/row_level_security_basic.py`

**Method:**
- Use Python string operations and regex patterns to validate SQL
- Search for required patterns in WHERE clauses and INSERT statements
- Case-insensitive matching with flexible whitespace handling

**Advantages:**
- Simple implementation, easy to understand and maintain
- No external dependencies beyond standard Python
- Fast execution
- Good for 80% of common SQL patterns

**Limitations:**
- May have false positives/negatives with complex SQL
- Cannot understand SQL semantics
- Struggles with nested conditions, subqueries, complex JOINs
- May miss violations in cleverly constructed SQL

**Best For:**
- Organizations with straightforward SQL patterns
- Teams wanting quick implementation
- Standard DML operations without complex logic

### Approach 2: SQL Parsing (Advanced)

**File:** `Python/Scripts/Any/row_level_security_advanced.py`

**Method:**
- Use `sqlparse` library to parse SQL into Abstract Syntax Tree
- Semantically analyze WHERE clauses and INSERT statements
- Validate that required conditions exist in parsed structure

**Advantages:**
- Understands SQL structure, not just text patterns
- Handles complex queries (JOINs, subqueries, nested conditions)
- More accurate violation detection
- Resilient to formatting variations, comments, case differences

**Limitations:**
- More complex implementation
- Dependency on sqlparse library (must be available in Liquibase GraalPy)
- Slightly slower than pattern matching
- May have edge cases with non-standard SQL dialects

**Best For:**
- Organizations with complex SQL patterns
- Teams requiring high accuracy (95%+ detection)
- Sophisticated database development practices

## Error Messages

When a violation is detected, the check provides clear, actionable guidance:

```
Row-level security violation detected!

Table: FRAMEWORK_CONFIG
Operation: UPDATE
Team: RISK (from environment variable TEAM_ID)
Required: WHERE clause must include "SOURCE = 'RISK'"

Problem: The SQL statement attempts to modify rows that may not belong to team RISK.

SQL: UPDATE FRAMEWORK_CONFIG SET enabled = 1 WHERE job_name = 'daily_batch'

Fix: Add team filtering to your WHERE clause:
  UPDATE FRAMEWORK_CONFIG SET enabled = 1
  WHERE job_name = 'daily_batch' AND SOURCE = 'RISK'
```

## Testing Strategy

### Test Coverage
Both implementations will have comprehensive test suites covering:

1. **Environment Variable Handling**
   - Check passes when env var is set and SQL is compliant
   - Check fires when env var is set but SQL violates policy
   - Check handles missing env var gracefully

2. **DML Operation Validation**
   - INSERT with correct team value → pass
   - INSERT with wrong team value → fire
   - INSERT missing team column → fire
   - UPDATE with proper WHERE clause → pass
   - UPDATE without team filtering → fire
   - DELETE with proper WHERE clause → pass
   - DELETE without team filtering → fire

3. **Table Filtering**
   - DML on protected table → validated
   - DML on non-protected table → ignored

4. **Edge Cases**
   - Case variations (source vs SOURCE vs SoUrCe)
   - Extra whitespace and formatting variations
   - SQL comments
   - Multiple tables in one changeset
   - sqlFile vs inline SQL changes
   - Empty or NULL values

### Test Implementation
- Tests located in `Python/tests/test_row_level_security_basic.py` and `test_row_level_security_advanced.py`
- Use existing `LiquibaseCheck` test harness
- Both integration tests (with Liquibase) and pure Python tests (with mocks)
- Target: >90% code coverage for both implementations
- Follow TDD: write tests before implementation

## CI/CD Integration

### Setting Environment Variables

**GitHub Actions:**
```yaml
- name: Deploy Risk Team Changes
  env:
    TEAM_ID: RISK
    LIQUIBASE_COMMAND_CHECKS_RUN_CHECKS_SCRIPTS_ENABLED: 'true'
  run: |
    liquibase update
```

**Jenkins:**
```groovy
environment {
    TEAM_ID = 'RISK'
    LIQUIBASE_COMMAND_CHECKS_RUN_CHECKS_SCRIPTS_ENABLED = 'true'
}
```

**Azure DevOps:**
```yaml
variables:
  TEAM_ID: 'RISK'
  LIQUIBASE_COMMAND_CHECKS_RUN_CHECKS_SCRIPTS_ENABLED: 'true'
```

### Configuration Example

`.liquibase/checks-settings.conf`:
```
checks:
  - name: RowLevelSecurityBasic
    enabled: true
    severity: ERROR
    parameters:
      ENV_VAR_NAME: TEAM_ID
      PROTECTED_TABLES: FRAMEWORK_CONFIG,JOB_DEFINITIONS,SHARED_PARAMETERS
      TEAM_COLUMN: SOURCE
```

## Comparison Matrix

| Feature | Basic (Pattern Matching) | Advanced (SQL Parsing) |
|---------|-------------------------|------------------------|
| **Complexity** | Simple | Moderate |
| **Dependencies** | None (standard Python) | sqlparse library |
| **Performance** | Fast | Slightly slower |
| **Accuracy** | 80-85% | 95%+ |
| **Complex SQL** | May miss violations | Handles well |
| **Maintenance** | Easy | Moderate |
| **False Positives** | Possible | Rare |
| **Best Use Case** | Standard DML patterns | Complex SQL, high accuracy needs |

## Recommendation

Both implementations will be provided as working demonstrations. Organizations should:

1. **Start with Basic implementation** for quick wins and team education
2. **Test with actual changelogs** from all vertical teams (Risk, IoT, PCM, etc.)
3. **Evaluate false positives/negatives** in real-world usage
4. **Switch to Advanced** if complex SQL patterns are common or accuracy is insufficient

## Success Criteria

- Both checks have >90% test coverage
- Clear documentation allows teams to configure and use
- Sample changesets demonstrate pass/fail scenarios
- Error messages provide actionable guidance
- No false negatives on standard DML patterns
- Minimal false positives (< 5% of legitimate queries flagged)

## Future Enhancements

Potential improvements for future consideration:

1. **Per-table column mapping:** Support different team columns per table
2. **Multiple column validation:** Require multiple columns to match (AND logic)
3. **Audit mode:** Log violations without blocking (for initial rollout)
4. **Environment-based severity:** Block in production, warn in dev/test
5. **Team mapping file:** Map database usernames to team identifiers automatically
6. **Whitelist patterns:** Allow specific SQL patterns to bypass validation

## References

- Liquibase Policy Checks: https://docs.liquibase.com/policy-checks
- Python Policy Check Development: (internal documentation)
