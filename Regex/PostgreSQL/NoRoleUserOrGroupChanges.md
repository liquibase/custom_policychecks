# NoRoleUserOrGroupChanges

Changes to ROLES, USERS, and GROUPS not allowed.

regex: `(?i)\b(CREATE|DROP|ALTER)\s+(ROLE|USER|GROUP)\b`

# Sample Failing Scripts
``` sql
CREATE ROLE username WITH LOGIN PASSWORD 'password';
```
``` sql
CREATE USER username WITH PASSWORD 'password';
```
``` sql
ALTER GROUP staff ADD USER karl, john;
```
``` sql
DROP ROLE poola;
```

# Sample Error Message
```
CHANGELOG CHECKS
----------------
Checks completed validation of the changelog and found the following issues:

Check Name:         Check for specific patterns in sql (NoRoleUserOrGroupChanges)
Changeset ID:       new_user
Changeset Filepath: changeLogs/users/asmith.sql
Check Severity:     INFO (Return code: 4)
Message:            Changes to ROLES, USERS, and GROUPS not allowed.
```
# Step-by-Step

| Prompt | Command or User Input |
| ------ | ----------------------|
| > | `liquibase checks customize --check-name=SqlUserDefinedPatternCheck` |
| Give your check a short name for easier identification (up to 64 alpha-numeric characters only) [SqlUserDefinedPatternCheck1]: | `NoRoleUserOrGroupChanges` |
| Set the Severity to return a code of 0-4 when triggered. (options: 'INFO'=0, 'MINOR'=1, 'MAJOR'=2, 'CRITICAL'=3, 'BLOCKER'=4)? [INFO]: | `<Choose a value: 0, 1, 2, 3, 4>` |
| Set 'SEARCH_STRING' (options: a string, or a valid regular expression): | `(?i)\b(CREATE\|DROP\|ALTER)\s+(ROLE\|USER\|GROUP)\b` |
| Set 'MESSAGE' [A match for regular expression <SEARCH_STRING> was detected in Changeset <CHANGESET>.]: | `Changes to ROLES, USERS, and GROUPS not allowed.` |
| Set 'STRIP_COMMENTS' (options: true, false) [true]: | `true` |

