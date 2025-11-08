# DAT JIRA Ticket: sys.exit Framework Bug

**JIRA Issue**: **DAT-21027**
**Link**: https://datical.atlassian.net/browse/DAT-21027

## Ticket Information
**Project**: DAT (Datical/Liquibase)
**Issue Type**: Bug
**Priority**: High
**Labels**: custom-policy-checks, framework, user-experience, liquibase-secure
**Status**: Created

---

## Summary
Custom Policy Check Framework: sys.exit(1) prevents multiple violation reporting

---

## Description

### Problem
Custom policy checks that use `sys.exit(1)` terminate immediately on first violation, preventing detection and reporting of additional violations in the same changeset. Users must fix and re-run multiple times to find all issues, leading to poor user experience and inefficient workflows.

### Steps to Reproduce

1. **Create a custom policy check** that validates table names must be uppercase (e.g., `table_uppercase_check.py`):

```python
import sys
import liquibase_utilities

liquibase_status = liquibase_utilities.get_status()
changes = liquibase_utilities.get_changeset().getChanges()

for change in changes:
    sql = liquibase_utilities.generate_sql(change).lower()

    # Check if CREATE TABLE with lowercase name
    if "create table" in sql:
        sql_list = sql.split()
        if "table" in sql_list:
            table_idx = sql_list.index("table")
            if table_idx + 1 < len(sql_list):
                table_name = sql_list[table_idx + 1]
                if table_name != table_name.upper():
                    liquibase_status.fired = True
                    liquibase_status.message = f"Table {table_name} must be UPPERCASE"
                    sys.exit(1)  # PROBLEM: Exits immediately!

False  # Default return
```

2. **Configure the check**:
```bash
liquibase checks customize --check-name=CustomCheckTemplate
# Configure with above script
liquibase checks enable --check-name=TableUppercaseCheck
```

3. **Create a changeset with multiple violations**:
```xml
<databaseChangeLog>
    <changeSet id="1" author="test">
        <createTable tableName="users">       <!-- Violation 1 -->
            <column name="id" type="INT"/>
        </createTable>
        <createTable tableName="products">    <!-- Violation 2 -->
            <column name="id" type="INT"/>
        </createTable>
        <createTable tableName="orders">      <!-- Violation 3 -->
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
- Policy check should detect ALL violations in the changeset
- Report all three violations in a single run:
  ```
  Policy Check Failed: TableUppercaseCheck
  - Table users must be UPPERCASE
  - Table products must be UPPERCASE
  - Table orders must be UPPERCASE
  ```
- User can fix all issues at once
- Efficient workflow: one check → one fix cycle

### Actual Behavior
- Policy check reports only first violation:
  ```
  Policy Check Failed: TableUppercaseCheck
  - Table users must be UPPERCASE
  ```
- `sys.exit(1)` terminates check immediately
- Violations 2 and 3 are never detected or reported
- User workflow:
  1. Run check → Find "users" violation
  2. Fix "users" table
  3. Run check again → Find "products" violation
  4. Fix "products" table
  5. Run check again → Find "orders" violation
  6. Fix "orders" table
  7. Finally succeeds

**Result**: 3 separate fix/test cycles instead of 1

### Impact

**Severity**: HIGH

- **Poor user experience**: Frustrating iterative fix/test/repeat workflow
- **Inefficient development**: Developers waste time in multiple check cycles
- **Hidden violations**: Users unaware of full scope of issues
- **Widespread pattern**: Many example policy checks demonstrate this anti-pattern
- **Training issue**: New policy check authors likely to copy this pattern
- **Large changesets affected**: Impact multiplies with number of changes in changeset

### Affected Population
This pattern appears to be common in custom policy checks. Based on code analysis:
- Example policy checks in documentation may use this pattern
- Community-contributed checks likely follow examples
- Estimated: Potentially affects majority of custom policy check implementations

### Root Cause

The custom policy check execution framework does not:
1. Catch or handle `sys.exit()` calls
2. Provide violation accumulation helpers
3. Document recommended patterns for multiple violations
4. Detect this anti-pattern during check registration

Policy check authors naturally use `sys.exit(1)` because:
- It's a common Python pattern for error exits
- No guidance provided on alternative approaches
- Works "correctly" for single violations
- Problem only apparent with multiple violations

### Suggested Fixes

**Option 1 (Recommended for Framework)**: **Catch sys.exit and accumulate violations**

```python
# In policy check execution framework
import sys

class ViolationAccumulator:
    def __init__(self):
        self.violations = []

    def exit_handler(self, exit_code):
        # Intercept sys.exit, don't actually exit
        if liquibase_status.fired and liquibase_status.message:
            self.violations.append(liquibase_status.message)
        # Reset for next iteration
        liquibase_status.fired = False
        liquibase_status.message = None

# Execute check with exit interception
accumulator = ViolationAccumulator()
sys.exit = accumulator.exit_handler

# Run check...

# After check completes:
if accumulator.violations:
    liquibase_status.fired = True
    liquibase_status.message = "; ".join(accumulator.violations)
```

Benefits:
- Existing checks work without modification
- Multiple violations automatically accumulated
- Backward compatible
- No code changes required from users

**Option 2**: **Provide liquibase_utilities helper**

Add to `liquibase_utilities`:
```python
def add_violation(message):
    """Add a violation to be reported. Multiple violations will be accumulated."""
    if not hasattr(liquibase_utilities, '_violations'):
        liquibase_utilities._violations = []
    liquibase_utilities._violations.append(message)

def finalize_violations():
    """Internal: Called by framework after check execution."""
    if hasattr(liquibase_utilities, '_violations') and liquibase_utilities._violations:
        liquibase_status.fired = True
        liquibase_status.message = "; ".join(liquibase_utilities._violations)
        return True
    return False
```

Usage in policy checks:
```python
# Instead of:
#   liquibase_status.fired = True
#   liquibase_status.message = "Error message"
#   sys.exit(1)

# Use:
liquibase_utilities.add_violation("Error message")
# Continue processing more changes...
```

Benefits:
- Explicit API for violation accumulation
- Clear intent
- Framework handles accumulation automatically

**Option 3**: **Detect and warn**

During policy check registration, scan script for `sys.exit` and warn:
```
WARNING: Policy check 'TableUppercaseCheck' contains sys.exit()
This will prevent reporting multiple violations.
Consider using liquibase_utilities.add_violation() instead.
See documentation: [link]
```

**Option 4**: **Documentation and migration guide**

Provide:
- Clear documentation of violation accumulation pattern
- Migration guide for existing checks
- Updated examples
- Best practices guide

### Recommended Pattern (for documentation)

```python
import liquibase_utilities

liquibase_status = liquibase_utilities.get_status()
changes = liquibase_utilities.get_changeset().getChanges()

violations = []  # Accumulate all violations

for change in changes:
    sql = liquibase_utilities.generate_sql(change)
    # ... validation logic ...
    if violation_found:
        violations.append(f"Violation in {change_id}: {error_message}")

# Report all violations at end
if violations:
    liquibase_status.fired = True
    liquibase_status.message = "; ".join(violations)
    # Optional: sys.exit(1) only at very end

False  # Default return
```

### Workaround

Policy check developers must manually refactor checks to accumulate violations. However:
- Requires awareness of the issue
- No detection mechanism for affected checks
- Time-consuming for large check libraries
- Risk of regression

### Additional Notes

- This affects user perception of Liquibase quality ("why doesn't it show all errors at once?")
- Similar issue may exist with other Python patterns (exceptions, early returns)
- Consider reviewing all example policy checks for this pattern
- Good opportunity to establish policy check best practices

### Example Real-World Impact

Organization with 20 custom policy checks:
- Developer creates changeset with 5 violations across different checks
- Must run `liquibase checks run` 5 separate times
- 10-15 minutes wasted in repeated executions
- Frustration leads to "disabling checks temporarily" (defeating the purpose)

### Environment
- **Liquibase Version**: [version]
- **Liquibase Secure**: [version]
- **Python Version**: [GraalPy version]
- **OS**: Cross-platform (affects all operating systems)

---

## Acceptance Criteria

- [ ] Policy checks can report multiple violations in single run
- [ ] Framework catches or works around sys.exit(1) pattern
- [ ] Clear documentation of recommended violation handling pattern
- [ ] Migration guide for existing checks
- [ ] Updated examples demonstrate best practices
- [ ] Optional: Warning system for anti-patterns in policy checks
- [ ] Test coverage for multiple violation scenarios

---

## Related Issues
- Related to DAT-[XXXX] (print statement framework issue) - both are framework-level policy check bugs
- May relate to general policy check best practices documentation

---

## Priority Justification

While not as critical as DAT-[XXXX] (print corrupts entire run), this significantly impacts:
- Developer productivity
- User experience with Liquibase
- Adoption of custom policy checks feature
- Time wasted in repeated check runs

Fixing this would greatly improve the custom policy check feature's usability and value proposition.
