# NoCreateRole

Do not allow `CREATE ROLE` statements.

regex: `(?is)(?=.*\b(create)\b)(?=.*\b(role)\b).*`

# Sample Failing Scripts
``` sql
CREATE ROLE lb_role;
```

# Sample Error Message
```
CHANGELOG CHECKS
----------------
Checks completed validation of the changelog and found the following issues:

Check Name:         Check for specific patterns in sql (NoCreateRole)
Changeset ID:       01
Changeset Filepath: sql/main/100_ddl/98_create_role.sql
Check Severity:     CRITICAL (Return code: 3)
Message:            Error! CREATE ROLE not allowed.
```

# Step-by-Step
| Prompt | Command or User Input |
| ------ | ----------------------|
| > | `liquibase checks customize --check-name=SqlUserDefinedPatternCheck` |
| Give your check a short name for easier identification (up to 64 alpha-numeric characters only) [SqlUserDefinedPatternCheck1]: | `NoCreateRole` |
| Set the Severity to return a code of 0-4 when triggered. (options: 'INFO'=0, 'MINOR'=1, 'MAJOR'=2, 'CRITICAL'=3, 'BLOCKER'=4)? [INFO]: | `<Choose a value: 0, 1, 2, 3, 4>` |
| Set 'SEARCH_STRING' (options: a string, or a valid regular expression): | `(?is)(?=.*\b(create)\b)(?=.*\b(role)\b).*` |
| Set 'MESSAGE' [A match for regular expression <SEARCH_STRING> was detected in Changeset <CHANGESET>.]: | `Error! CREATE ROLE not allowed.` |
| Set 'STRIP_COMMENTS' (options: true, false) [true]: | `true` |
