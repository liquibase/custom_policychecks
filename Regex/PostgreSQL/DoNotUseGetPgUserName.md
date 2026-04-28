# DoNotUseGetPgUserName

Do not use getpgusername().

regex: `(?i)\bgetpgusername\s*\(\s*\)`

# Sample Failing Scripts
``` sql
SELECT * FROM users WHERE 'admin' = getpgusername();
```

# Sample Error Message
```
CHANGELOG CHECKS
----------------
Checks completed validation of the changelog and found the following issues:

Check Name:         Check for specific patterns in sql (DoNotUseGetPgUserName)
Changeset ID:       getpgusername
Changeset Filepath: changeLogs/tools/getpgusername.sql
Check Severity:     INFO (Return code: 0)
Message:            Do not use getpgusername().
```
# Step-by-Step

| Prompt | Command or User Input |
| ------ | ----------------------|
| > | `liquibase checks customize --check-name=SqlUserDefinedPatternCheck` |
| Give your check a short name for easier identification (up to 64 alpha-numeric characters only) [SqlUserDefinedPatternCheck1]: | `DoNotUseGetPgUserName` |
| Set the Severity to return a code of 0-4 when triggered. (options: 'INFO'=0, 'MINOR'=1, 'MAJOR'=2, 'CRITICAL'=3, 'BLOCKER'=4)? [INFO]: | `<Choose a value: 0, 1, 2, 3, 4>` |
| Set 'SEARCH_STRING' (options: a string, or a valid regular expression): | `(?i)\bgetpgusername\s*\(\s*\)` |
| Set 'MESSAGE' [A match for regular expression <SEARCH_STRING> was detected in Changeset <CHANGESET>.]: | `Do not use getpgusername().` |
| Set 'STRIP_COMMENTS' (options: true, false) [true]: | `true` |

