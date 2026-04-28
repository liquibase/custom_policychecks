# NoReassignOwned

Do not allow `REASSIGN OWNED` statements.

regex: `(?i)\breassign\s+owned\b`

# Sample Failing Scripts
``` sql
--changeset asmith:reassign_owned
REASSIGN OWNED BY role1, role2 TO new_owner;
```

# Sample Error Message
```
CHANGELOG CHECKS
----------------
Checks completed validation of the changelog and found the following issues:

Check Name:         Check for specific patterns in sql (NoReassignOwned)
Changeset ID:       reassign_owned
Changeset Filepath: changeLogs/logins/01_reassign_owned.sql
Check Severity:     INFO (Return code: 0)
Message:            Error! REASSIGN OWNED statements not allowed.
```

# Step-by-Step
| Prompt | Command or User Input |
| ------ | ----------------------|
| > | `liquibase checks customize --check-name=SqlUserDefinedPatternCheck` |
| Give your check a short name for easier identification (up to 64 alpha-numeric characters only) [SqlUserDefinedPatternCheck1]: | `NoReassignOwned` |
| Set the Severity to return a code of 0-4 when triggered. (options: 'INFO'=0, 'MINOR'=1, 'MAJOR'=2, 'CRITICAL'=3, 'BLOCKER'=4)? [INFO]: | `<Choose a value: 0, 1, 2, 3, 4>` |
| Set 'SEARCH_STRING' (options: a string, or a valid regular expression): | `(?i)\breassign\s+owned\b` |
| Set 'MESSAGE' [A match for regular expression <SEARCH_STRING> was detected in Changeset <CHANGESET>.]: | `Error! REASSIGN OWNED statements not allowed.` |
| Set 'STRIP_COMMENTS' (options: true, false) [true]: | `true` |
