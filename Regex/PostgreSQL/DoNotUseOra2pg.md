# DoNotUseOra2pg

Do not use ora2pg.

regex: `(?i)\bora2pg\b`

# Sample Failing Scripts
``` sql
SELECT * FROM ora2pg_config;
```

# Sample Error Message
```
CHANGELOG CHECKS
----------------
Checks completed validation of the changelog and found the following issues:

Check Name:         Check for specific patterns in sql (DoNotUseOra2pg)
Changeset ID:       ora2pg_config
Changeset Filepath: changeLogs/tools/ora2pg_config.sql
Check Severity:     INFO (Return code: 0)
Message:            Do not use ora2pg.
```
# Step-by-Step

| Prompt | Command or User Input |
| ------ | ----------------------|
| > | `liquibase checks customize --check-name=SqlUserDefinedPatternCheck` |
| Give your check a short name for easier identification (up to 64 alpha-numeric characters only) [SqlUserDefinedPatternCheck1]: | `DoNotUseOra2pg` |
| Set the Severity to return a code of 0-4 when triggered. (options: 'INFO'=0, 'MINOR'=1, 'MAJOR'=2, 'CRITICAL'=3, 'BLOCKER'=4)? [INFO]: | `<Choose a value: 0, 1, 2, 3, 4>` |
| Set 'SEARCH_STRING' (options: a string, or a valid regular expression): | `(?i)\bora2pg\b` |
| Set 'MESSAGE' [A match for regular expression <SEARCH_STRING> was detected in Changeset <CHANGESET>.]: | `Do not use ora2pg.` |
| Set 'STRIP_COMMENTS' (options: true, false) [true]: | `true` |

