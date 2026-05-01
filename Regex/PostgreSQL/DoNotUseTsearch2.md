# DoNotUseTsearch2

Do not use tsearch2.

regex: `(?i)\btsearch2\b`

# Sample Failing Scripts
``` sql
SELECT * FROM pg_available_extensions WHERE name = 'tsearch2';
```

# Sample Error Message
```
CHANGELOG CHECKS
----------------
Checks completed validation of the changelog and found the following issues:

Check Name:         Check for specific patterns in sql (DoNotUseTsearch2)
Changeset ID:       tsearch2
Changeset Filepath: changeLogs/tools/tsearch2.sql
Check Severity:     INFO (Return code: 0)
Message:            Do not use tsearch2.
```
# Step-by-Step

| Prompt | Command or User Input |
| ------ | ----------------------|
| > | `liquibase checks customize --check-name=SqlUserDefinedPatternCheck` |
| Give your check a short name for easier identification (up to 64 alpha-numeric characters only) [SqlUserDefinedPatternCheck1]: | `DoNotUseTsearch2` |
| Set the Severity to return a code of 0-4 when triggered. (options: 'INFO'=0, 'MINOR'=1, 'MAJOR'=2, 'CRITICAL'=3, 'BLOCKER'=4)? [INFO]: | `<Choose a value: 0, 1, 2, 3, 4>` |
| Set 'SEARCH_STRING' (options: a string, or a valid regular expression): | `(?i)\btsearch2\b` |
| Set 'MESSAGE' [A match for regular expression <SEARCH_STRING> was detected in Changeset <CHANGESET>.]: | `Do not use tsearch2.` |
| Set 'STRIP_COMMENTS' (options: true, false) [true]: | `true` |

