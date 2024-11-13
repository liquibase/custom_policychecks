# PreventLockingColumnOrIndex

`ADD COLUMN` and `ADD INDEX` must be done in an online manner to prevent locking. `ALGORITHM=INPLACE, LOCK=NONE` is required when using the following statements: 
<br>`ALTER TABLE ... ADD COLUMN`
<br>`ALTER TABLE ... ADD INDEX`
<br>`CREATE INDEX`

regex: `(?is)(?=.*\b(alter\s*table|create)\b)(?=.*\b(column|index)\b)(?!.*\b(algorithm\s*=\s*inplace\s*,\s*lock\s*=\s*none)\b).*`

# Sample Failing Scripts
``` sql
ALTER TABLE new_table_01 ADD COLUMN A VARCHAR(45) NULL DEFAULT NULL AFTER name;
```
``` sql
ALTER TABLE new_table_01 ADD INDEX b_index (b);
```
``` sql
CREATE INDEX b_index ON new_table_01 (b);
```

# Sample Passing Scripts
``` sql
ALTER TABLE new_table_01 ADD COLUMN A VARCHAR(45) NULL DEFAULT NULL AFTER name,
algorithm = inplace, lock=none;
```
``` sql
ALTER TABLE new_table_01 ADD INDEX b_index (b),
algorithm = inplace, lock=none;
```
``` sql
CREATE INDEX b_index ON new_table_01 (b),
algorithm = inplace, lock=none;
```

# Sample Error Message
```
CHANGELOG CHECKS
----------------
Checks completed validation of the changelog and found the following issues:

Check Name:         Check for specific patterns in sql (CannotModifyUsersOrRoles)
Changeset ID:       01
Changeset Filepath: sql/main/100_ddl/97_add_column.sql
Check Severity:     MINOR (Return code: 1)
Message:            Adding a COLUMN or INDEX needs to be done in an online manner.
```

# Step-by-Step
| Prompt | Command or User Input |
| ------ | ----------------------|
| > | `liquibase checks customize --check-name=SqlUserDefinedPatternCheck` |
| Give your check a short name for easier identification (up to 64 alpha-numeric characters only) [SqlUserDefinedPatternCheck1]: | `PreventLockingColumnOrIndex` |
| Set the Severity to return a code of 0-4 when triggered. (options: 'INFO'=0, 'MINOR'=1, 'MAJOR'=2, 'CRITICAL'=3, 'BLOCKER'=4)? [INFO]: | `<Choose a value: 0, 1, 2, 3, 4>` |
| Set 'SEARCH_STRING' (options: a string, or a valid regular expression): | `(?is)(?=.*\b(alter\s*table\|create)\b)(?=.*\b(column\|index)\b)(?!.*\b(algorithm\s*=\s*inplace\s*,\s*lock\s*=\s*none)\b).*` |
| Set 'MESSAGE' [A match for regular expression <SEARCH_STRING> was detected in Changeset <CHANGESET>.]: | `Adding a COLUMN or INDEX needs to be done in an online manner.` |
| Set 'STRIP_COMMENTS' (options: true, false) [true]: | `true` |