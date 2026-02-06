# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Structure

This is a collection of Liquibase Pro Policy Checks with two main components:
- **Regex Policy Checks** (`Regex/`): Pattern-based checks organized by database type
- **Python Policy Checks** (`Python/`): Advanced programmatic checks with test harness

### Python Policy Checks Architecture

The Python checks are organized as follows:
- `Python/Scripts/`: Policy check implementations organized by database type (Any/, Oracle/, MongoDB/, etc.)
- `Python/tests/`: Test harness for validating policy check behavior  
- `Python/Changesets/`: Sample changelog files for testing

Each Python check script receives Liquibase context objects (snapshot, changeset, utilities) and validates database changes according to configured rules.

## Development Commands

### Running Tests
Tests are located in the `tests/` directory and validate Python policy check behavior.

**Run all tests:**
```bash
cd Python
python3 -m pytest tests/ -v
```

**Run tests by category:**
```bash
# Integration tests (require Liquibase)
python3 -m pytest tests/ -m integration -v

# Pure Python tests (mocked environment)
python3 -m pytest tests/ -m pure_python -v
```

**Run single test file:**
```bash
python3 -m pytest tests/test_create_index_count.py -v
```

### Test Coverage

Coverage reporting tracks code coverage for Python policy checks that have tests. The coverage configuration only measures coverage for policy check scripts that have corresponding test files.

**Currently tested policy checks:**
- `Python/Scripts/Any/create_index_count.py`
- `Python/Scripts/Any/table_names_uppercase.py`

**Run tests with coverage:**
```bash
# NOTE: All commands should be run from the project root directory

# All tests with coverage (uses pyproject.toml configuration)
python3 -m pytest Python/tests/ --cov --cov-report=html --cov-report=xml --cov-report=term-missing -v

# Pure Python tests only (faster feedback)
python3 -m pytest Python/tests/ -m pure_python --cov --cov-report=html --cov-report=xml --cov-report=term-missing -v

# Integration tests with coverage  
python3 -m pytest Python/tests/ -m integration --cov --cov-report=html --cov-report=xml --cov-report=term-missing -v
```

**Coverage reports:**
```bash
# View coverage summary
python3 -m coverage report

# Open HTML coverage report
open htmlcov/index.html

# Generate XML report for CI/CD
python3 -m coverage xml
```

**Coverage Requirements:**
- Target 90% minimum coverage for policy check scripts that have tests
- HTML reports generated in `htmlcov/` directory  
- XML reports for CI/CD integration in `coverage.xml`
- Only policy checks with tests are included in coverage measurement

**Coverage Limitations:**
- Policy check scripts run via dynamic execution (`exec()`) within the test harness
- Pure Python mode uses mocks and may not capture all execution paths
- Integration mode provides more realistic coverage but requires Liquibase Pro license
- Coverage tracking works best for test harness code itself, not the executed policy checks

### Testing Policy Checks with Liquibase

Policy checks require Liquibase Pro with the environment variable:
```bash
export LIQUIBASE_COMMAND_CHECKS_RUN_CHECKS_SCRIPTS_ENABLED='true'
```

**Basic Liquibase commands:**
```bash
# Show available checks
liquibase checks show

# Run all enabled checks
liquibase checks run

# Disable all checks (useful for debugging)
liquibase checks bulk-set --disable

# Enable a specific custom check
liquibase checks enable --check-name=<check-name>

# Customize check configuration
liquibase checks customize --check-name=<check-name>
```

## Code Conventions

### Python Policy Check Structure
Each policy check script follows this pattern:
1. Import required Liquibase utilities
2. Initialize logger, status, and snapshot objects
3. Process changeset changes or snapshot data
4. Set `liquibase_status.fired = True` with error message if violations found
5. Return `False` by default (check passed)

### Test Structure
Tests use a custom `LiquibaseCheck` test harness with two modes:
- **Integration mode**: Executes checks via actual Liquibase
- **Pure Python mode**: Uses mocked Liquibase objects for faster testing

Test classes should include both `@pytest.mark.integration` and `@pytest.mark.pure_python` test methods.

### Message Templates
Policy check messages support replacement tokens:
- `__TABLE_NAME__`: Table name from violations
- `__INDEX_COUNT__`: Current index count  
- `__COLUMN_NAME__`: Column name
- Custom tokens defined per check

## Key Dependencies

The Python checks require these Liquibase-provided modules:
- `liquibase_utilities`: Core functions for SQL parsing, caching, arguments
- `liquibase_changesets`: Changeset metadata access
- `sqlparse`: SQL parsing library (when available)

Checks are designed to work within Liquibase's GraalPy runtime environment but can also run in standard Python for testing.

## Testing Notes

- Tests use database-agnostic SQL for maximum compatibility
- The test harness mocks Liquibase snapshot data for isolated testing
- Policy checks process one changeset at a time but maintain state via caching
- Sample changesets in `Python/Changesets/` provide realistic test data
- Always use the liquibase-test-builder subagent when creating new tests for Python Policy Tests in the Python/tests directory.
- Use the liquibase-test-builder when creating new tests for python poliy checks