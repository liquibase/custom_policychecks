# Test Plan: Custom Policy Check Test Coverage Expansion

**Date**: 2025-10-12
**Objective**: Create comprehensive tests for SQL pattern-based custom policy checks to validate test harness functionality and discover bugs in policy implementations.

## Executive Summary

This test plan focuses on expanding test coverage for Liquibase custom policy checks by creating comprehensive test suites for 5 selected policy checks. The primary goals are:
1. Validate the custom policy check test harness API capabilities
2. Discover bugs in policy check implementations
3. Establish testing patterns for future policy check development
4. Achieve comprehensive coverage of SQL pattern-based checks

## Scope

### In Scope
- SQL pattern-based policy checks (tokenization/parsing)
- Database-agnostic checks from `Python/Scripts/Any/`
- Oracle-specific checks with clear SQL patterns
- Test creation using liquibase-test-builder subagent
- Bug documentation with pytest best practices

### Out of Scope
- Snapshot-dependent checks (`get_database_object()`, `get_snapshot()`)
- Database query-based checks (`query_for_list()`)
- Informational/non-validation checks
- MongoDB/NoSQL checks (uncertain compatibility)
- Database-specific checks requiring specific database versions (e.g., MySQL 8.0)

## Selected Policy Checks

### 1. fk_names.py (Python/Scripts/Any/)
**Purpose**: Enforces foreign key naming convention `FK_<child_table>_<parent_table>`

**Test Coverage Areas**:
- Valid FK names matching pattern
- Invalid FK names (missing parts, wrong order)
- CREATE TABLE with inline FK constraints
- ALTER TABLE ADD CONSTRAINT
- Schema-qualified table names
- Case sensitivity handling
- Multiple FK constraints in one statement
- Malformed SQL edge cases

**Confidence Level**: HIGH
**Rationale**: Clear pattern matching on FK constraint names using SQL parsing

---

### 2. identifiers_without_quotes.py (Python/Scripts/Any/)
**Purpose**: Prevents use of quoted identifiers (double quotes) in SQL

**Test Coverage Areas**:
- Unquoted identifiers (valid)
- Double-quoted table names (invalid)
- Double-quoted column names (invalid)
- Mixed quoted/unquoted identifiers
- String literals with single quotes (valid)
- Case sensitivity considerations
- Schema-qualified names with quotes
- Complex SQL with multiple identifiers

**Confidence Level**: HIGH
**Rationale**: Simple pattern detection using sqlparse tokenization

---

### 3. table_name_is_camelcase.py (Python/Scripts/Any/)
**Purpose**: Enforces camelCase naming convention for tables

**Test Coverage Areas**:
- Valid camelCase names (myTableName)
- Invalid lowercase names (mytablename)
- Invalid uppercase names (MYTABLENAME)
- Invalid snake_case names (my_table_name)
- Single character table names
- Numeric characters in names
- Schema-qualified table names
- CREATE TABLE vs CREATE OR REPLACE
- Quoted identifiers handling
- Multiple CREATE TABLE statements

**Confidence Level**: HIGH
**Rationale**: Similar pattern to existing table_names_uppercase test, regex validation

---

### 4. timestamp_column_name.py (Python/Scripts/Any/)
**Purpose**: Enforces column naming postfix for specific data types (e.g., `_ts` for TIMESTAMP)

**Test Coverage Areas**:
- TIMESTAMP columns with correct postfix (valid)
- TIMESTAMP columns without postfix (invalid)
- Non-TIMESTAMP columns (ignored)
- Configurable COLUMN_TYPE argument
- Configurable COLUMN_POSTFIX argument
- Multiple columns with same type
- Mixed column types in same table
- ALTER TABLE ADD COLUMN scenarios
- Case sensitivity in data types
- Column name extraction from complex SQL

**Confidence Level**: HIGH
**Rationale**: Tests argument handling and column validation, clear pattern matching

---

### 5. varchar2_must_use_char.py (Python/Scripts/Oracle/)
**Purpose**: Ensures Oracle VARCHAR2 columns specify CHAR length semantics (not BYTE)

**Test Coverage Areas**:
- VARCHAR2(n CHAR) syntax (valid)
- VARCHAR2(n) syntax without CHAR (invalid)
- VARCHAR2(n BYTE) syntax (invalid)
- Multiple VARCHAR2 columns in one table
- Mixed VARCHAR2 with/without CHAR
- Non-VARCHAR2 data types (ignored)
- Case sensitivity in data type names
- Parentheses parsing for size
- Column constraints after data type
- Complex CREATE TABLE statements

**Confidence Level**: HIGH
**Rationale**: Clear pattern matching on Oracle data type syntax

## Excluded Policy Checks (Snapshot-Dependent)

The following checks were excluded due to snapshot dependencies that may not be fully supported by current test harness:

- **pk_names.py**: Uses `get_database_object()` to check primary key names from snapshot
- **table_column_name_size.py**: Uses `get_database_object()` to validate name lengths
- **varchar_data_integrity.py**: Uses `get_snapshot()` to validate data against column types
- **create_index_count.py**: Uses snapshot for existing index counts (tests already exist but all skipped)
- **count_rows.py**: Uses `query_for_list()` requiring live database execution
- **show_rollback.py**: Informational only, not a validation check

## Excluded Policy Checks (Database-Specific)

- **illegalAlter.py** (MySQL): Requires MySQL 8.0, test harness uses H2 (tests exist but mostly skipped)
- **MongoDB checks**: Use JavaScript syntax, uncertain test harness compatibility
- **Oracle checks** (except varchar2_must_use_char): May require Oracle-specific features

## Test Structure

Each test file will follow the established pattern from existing tests:

```python
"""
Comprehensive test suite for <policy_check_name>.py custom policy check.

Policy Intent: <brief description>
"""

import pytest
from liquibase_test_harness import LiquibaseCheck

class Test<PolicyName>:
    """Test suite for <policy_check_name>.py policy check."""

    # ========================================
    # POLICY COMPLIANCE TESTS (Should NOT fire)
    # ========================================

    # ========================================
    # POLICY VIOLATION TESTS (Should fire)
    # ========================================

    # ========================================
    # EDGE CASE TESTS
    # ========================================

    # ========================================
    # BOUNDARY CONDITION TESTS
    # ========================================

    # ========================================
    # MALFORMED SQL TESTS
    # ========================================

    # ========================================
    # BUG EXPOSURE TESTS
    # ========================================
```

### Bug Documentation

When bugs are discovered, they will be documented using pytest best practices:

```python
@pytest.mark.xfail(
    reason="BUG: <policy_check_name>.py <specific issue>. "
           "Root cause: <line numbers and explanation>. "
           "Fix: <suggested fix>."
)
def test_<scenario>():
    """Test that would pass if bug were fixed."""
    # Test implementation
```

## Execution Strategy

### Phase 1: Test Plan Creation
- Document test plan in `TEST_PLAN.md`
- Get approval before proceeding

### Phase 2: Parallel Test Creation
- Launch 5 liquibase-test-builder subagents in parallel (one per policy)
- Each subagent creates: `Python/tests/test_<policy_name>.py`
- Each subagent independently retrieves Python API documentation
- Subagents follow established test patterns and structure

**Subagent Task Template**:
```
Create comprehensive tests for the <policy_name>.py custom policy check.

Policy location: Python/Scripts/<folder>/<policy_name>.py
Test file to create: Python/tests/test_<policy_name>.py

Requirements:
1. Read the policy check source code to understand its logic
2. Retrieve Python API documentation using available tools
3. Create comprehensive test coverage including:
   - Policy compliance tests (should NOT fire)
   - Policy violation tests (SHOULD fire)
   - Edge cases and boundary conditions
   - Malformed SQL handling
   - Bug exposure tests
4. Follow the test structure from existing tests (test_table_names_uppercase.py)
5. Document any bugs found using @pytest.mark.xfail with detailed descriptions
6. Test should validate both the policy check AND the test harness capabilities
```

### Phase 3: Test Execution and Reporting
After all subagents complete:
1. Run all new tests: `pytest Python/tests/test_*.py -v`
2. Run with coverage: `pytest Python/tests/ --cov --cov-report=html --cov-report=term-missing -v`
3. Generate bug report summarizing findings
4. Document test harness limitations discovered

## Success Criteria

### Minimum Requirements
- [ ] All 5 policy checks have comprehensive test files created
- [ ] Each test file has at least 10 test methods
- [ ] Tests cover compliance, violations, edge cases, and boundaries
- [ ] All tests execute without crashing (may pass, fail, or be skipped)
- [ ] Bugs are documented with clear `@pytest.mark.xfail` annotations

### Stretch Goals
- [ ] Discover at least 3 new bugs in policy check implementations
- [ ] Discover at least 1 limitation in test harness API
- [ ] Achieve >80% code coverage for tested policy checks
- [ ] All test files follow consistent structure and naming conventions
- [ ] Create reusable test patterns for future policy check testing

## Deliverables

1. **TEST_PLAN.md**: This comprehensive test plan document
2. **Test Files**: 5 new test files in `Python/tests/`:
   - `test_fk_names.py`
   - `test_identifiers_without_quotes.py`
   - `test_table_name_is_camelcase.py`
   - `test_timestamp_column_name.py`
   - `test_varchar2_must_use_char.py`
3. **Test Execution Report**: Summary of test results and coverage
4. **Bug Report**: Documented bugs found in policy checks and test harness

## Timeline

- **Phase 1**: Test plan creation and approval (Complete)
- **Phase 2**: Parallel test creation with subagents (Est. 30-45 minutes)
- **Phase 3**: Test execution and reporting (Est. 15 minutes)

**Total Estimated Time**: 1 hour

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Test harness API limitations | Medium | Document limitations, skip tests as needed |
| Policy checks more complex than expected | Medium | Focus on core functionality, document complex edge cases |
| Subagents produce inconsistent test quality | Low | Use liquibase-test-builder with clear requirements |
| Database compatibility issues | Low | Focus on SQL pattern checks, not execution |

## Appendix: Policy Check Inventory

Total policy checks in repository: **31**

### By Folder
- `Python/Scripts/Any/`: 12 checks
- `Python/Scripts/Oracle/`: 8 checks
- `Python/Scripts/MongoDB/`: 4 checks
- `Python/Scripts/MySQL/`: 1 check
- `Python/Scripts/PostgreSQL/`: 1 check
- `Python/Scripts/Db2zos/`: 1 check
- `Python/Scripts/DynamoDB/`: 1 check
- `Python/Scripts/FormattedSQL/`: 1 check

### Test Coverage Status
- **Tested (4)**: delete_without_where, table_names_uppercase, create_index_count*, illegalAlter*
  - *Tests exist but mostly skipped due to limitations
- **In Progress (5)**: Selected for this test plan
- **Not Yet Tested (22)**: Remaining policy checks
