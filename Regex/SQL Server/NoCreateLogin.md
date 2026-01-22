# NoCreateLogin

Do not allow `CREATE LOGIN` statements.

regex: `(?i)create\s*login`

# Sample Failing Scripts
``` sql
--changeset asmith:create_login
CREATE LOGIN [joe@acme.com] FROM EXTERNAL PROVIDER
```

# Sample Error Message
```
CHANGELOG CHECKS
----------------
Checks completed validation of the changelog and found the following issues:

Check Name:         Check for specific patterns in sql (NoAlterTable)
Changeset ID:       create_login
Changeset Filepath: changeLogs/logins/01_createLogin1.sql
Check Severity:     INFO (Return code: 0)
Message:            Error! CREATE LOGIN statements not allowed.
```

# Step-by-Step
| Prompt | Command or User Input |
| ------ | ----------------------|
| > | `liquibase checks customize --check-name=SqlUserDefinedPatternCheck` |
| Give your check a short name for easier identification (up to 64 alpha-numeric characters only) [SqlUserDefinedPatternCheck1]: | `NoCreateLogin` |
| Set the Severity to return a code of 0-4 when triggered. (options: 'INFO'=0, 'MINOR'=1, 'MAJOR'=2, 'CRITICAL'=3, 'BLOCKER'=4)? [INFO]: | `<Choose a value: 0, 1, 2, 3, 4>` |
| Set 'SEARCH_STRING' (options: a string, or a valid regular expression): | `(?i)create\s*login` |
| Set 'MESSAGE' [A match for regular expression <SEARCH_STRING> was detected in Changeset <CHANGESET>.]: | `Error! CREATE LOGIN statements not allowed.` |
| Set 'STRIP_COMMENTS' (options: true, false) [true]: | `true` |
