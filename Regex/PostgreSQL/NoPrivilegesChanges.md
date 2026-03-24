# NoPrivilegesChanges

Do not allow updates to `privileges`.

regex: `(?i)\b(ALL|ALTER(\s+DEFAULT)?)\s+PRIVILEGES\b`

# Sample Failing Scripts
``` sql
--changeset asmith:update_privileges
ALTER DEFAULT PRIVILEGES IN SCHEMA public
```

# Sample Error Message
```
CHANGELOG CHECKS
----------------
Checks completed validation of the changelog and found the following issues:

Check Name:         Check for specific patterns in sql (NoPgSettings)
Changeset ID:       update_privileges
Changeset Filepath: changeLogs/updates/01_update_privileges.sql
Check Severity:     INFO (Return code: 0)
Message:            Error! Updates to privileges not allowed.
```

# Step-by-Step
| Prompt | Command or User Input |
| ------ | ----------------------|
| > | `liquibase checks customize --check-name=SqlUserDefinedPatternCheck` |
| Give your check a short name for easier identification (up to 64 alpha-numeric characters only) [SqlUserDefinedPatternCheck1]: | `NoPrivilegesChanges` |
| Set the Severity to return a code of 0-4 when triggered. (options: 'INFO'=0, 'MINOR'=1, 'MAJOR'=2, 'CRITICAL'=3, 'BLOCKER'=4)? [INFO]: | `<Choose a value: 0, 1, 2, 3, 4>` |
| Set 'SEARCH_STRING' (options: a string, or a valid regular expression): | `(?i)\b(ALL|ALTER(\s+DEFAULT)?)\s+PRIVILEGES\b` |
| Set 'MESSAGE' [A match for regular expression <SEARCH_STRING> was detected in Changeset <CHANGESET>.]: | `Error! Updates to privileges not allowed.` |
| Set 'STRIP_COMMENTS' (options: true, false) [true]: | `true` |
