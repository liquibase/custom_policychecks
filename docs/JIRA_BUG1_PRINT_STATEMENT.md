# DAT JIRA Ticket: Print Statement Framework Bug

**JIRA Issue**: **DAT-21026**
**Link**: https://datical.atlassian.net/browse/DAT-21026

## Ticket Information
**Project**: DAT (Datical/Liquibase)
**Issue Type**: Bug
**Priority**: Critical
**Labels**: custom-policy-checks, framework, critical, liquibase-secure
**Status**: Created

---

## Summary
Custom Policy Check Framework: print() statements corrupt JSON output

---

## Description

### Problem
Custom policy checks that use Python's `print()` function corrupt Liquibase's JSON output, causing the entire policy check run to fail with JSONDecodeError. One wayward policy check can break all policy checks in an installation.

### Steps to Reproduce

1. **Create a custom policy check script** (e.g., `example_check.py`):

```python
import liquibase_utilities

liquibase_logger = liquibase_utilities.get_logger()
liquibase_status = liquibase_utilities.get_status()

# This print statement corrupts output
print("Debug: checking table name")

changes = liquibase_utilities.get_changeset().getChanges()
for change in changes:
    sql = liquibase_utilities.generate_sql(change)
    # ... check logic here ...

False  # Default return
```

2. **Configure the check** in Liquibase:
```bash
liquibase checks customize --check-name=CustomCheckTemplate
# Configure with above script path
liquibase checks enable --check-name=ExampleCheck
```

3. **Create a test changeset**:
```xml
<databaseChangeLog>
    <changeSet id="1" author="test">
        <createTable tableName="users">
            <column name="id" type="INT"/>
        </createTable>
    </changeSet>
</databaseChangeLog>
```

4. **Run checks**:
```bash
liquibase checks run
```

### Expected Behavior
- Print statements should be redirected to Liquibase's logging subsystem
- Policy check output should remain valid JSON
- Liquibase should complete policy check run successfully
- **OR**: Clear error message indicating which policy check is malformed (e.g., "Policy check 'ExampleCheck' wrote to stdout, which is not allowed")

### Actual Behavior
- Print output goes directly to stdout: `Debug: checking table name`
- This corrupts the JSON that Liquibase expects to parse
- Liquibase fails with error: `JSONDecodeError: Extra data: line 1 column X (char Y)`
- Entire policy check run fails
- No clear indication of which policy check caused the problem
- All other policy checks are prevented from running

### Impact

**Severity**: CRITICAL

- **Large installations at risk**: Organizations with multiple custom policy checks are vulnerable to complete failure from a single developer's debug statement
- **No safeguards**: Framework provides no protection against stdout corruption
- **Silent failure**: No indication which check is problematic or how to fix it
- **Cascading failure**: One bad check breaks entire policy check infrastructure
- **Production risk**: Debug statements left in policy checks can break production deployments

### Root Cause

The custom policy check execution environment does not:
1. Override or redirect Python's `print()` built-in function
2. Capture or validate stdout output
3. Detect when policy checks write to stdout
4. Provide clear error messages when JSON parsing fails

### Suggested Fixes

**Option 1 (Recommended)**: **Override print() in execution context**
```python
# In policy check execution framework
import builtins
import liquibase_utilities

# Redirect print to logging
def safe_print(*args, **kwargs):
    logger = liquibase_utilities.get_logger()
    message = ' '.join(str(arg) for arg in args)
    logger.info(message)

builtins.print = safe_print
```

Benefits:
- Existing checks with print statements continue to work
- Output goes to logs where it belongs
- No JSON corruption
- Backward compatible

**Option 2**: **Detect stdout corruption**
```python
# Wrap policy check execution
import sys
from io import StringIO

stdout_capture = StringIO()
sys.stdout = stdout_capture

# Execute policy check...

stdout_output = stdout_capture.getvalue()
if stdout_output:
    raise PolicyCheckError(
        f"Policy check '{check_name}' wrote to stdout: {stdout_output[:100]}"
        f"\nUse liquibase_logger.info() instead of print()"
    )
```

Benefits:
- Clear error message identifying problematic check
- Prevents JSON corruption
- Guides developers to correct solution

**Option 3**: **Validate policy check output**

Before parsing JSON, check for corruption and provide actionable error.

### Workaround

Policy check developers must manually replace all `print()` statements with:
```python
liquibase_logger.info("message")
```

However, this requires:
- Finding all affected checks (no detection mechanism)
- Educating all policy check authors
- No protection against future occurrences

### Additional Notes

- This issue affects both community-developed and enterprise custom policy checks
- The problem is particularly insidious because it works in development/testing but fails in production
- Similar issues may exist with other stdout/stderr usage (e.g., `sys.stdout.write()`, `warnings.warn()`)

### Environment
- **Liquibase Version**: [version]
- **Liquibase Secure**: [version]
- **Python Version**: [GraalPy version]
- **OS**: Cross-platform (affects all operating systems)

---

## Acceptance Criteria

- [ ] Custom policy checks using `print()` do not corrupt JSON output
- [ ] Clear error message when policy checks write to stdout
- [ ] Documentation updated with guidance on logging vs print
- [ ] Backward compatibility maintained for existing checks
- [ ] Test coverage added for stdout detection

---

## Related Issues
- Related to DAT-[XXXX] (sys.exit framework issue) - both are framework-level policy check bugs
