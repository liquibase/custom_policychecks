# NoDataDmlStatements

Do not allow DELETE FROM statements.

regex: `(?i)delete\s*from`

# Sample Failing Scripts
``` sql
DELETE FROM table_name WHERE condition;
```
``` sql
DELETE FROM table_name;
```

# Sample Error Message
```
CHANGELOG CHECKS
----------------
Checks completed validation of the changelog and found the following issues:

Check Name:         Check for specific patterns in sql (NoDataDMLStatements)
Changeset ID:       sales_insert
Changeset Filepath: changeLogs/data/sales_insert.sql
Check Severity:     MINOR (Return code: 1)
Message:            DATA DML statements are not allowed.
```
# Step-by-Step

| Prompt | Command or User Input                                           |
| ------ |-----------------------------------------------------------------|
| > | `liquibase checks copy --check-name=SqlUserDefinedPatternCheck` |
| Give your check a short name for easier identification (up to 64 alpha-numeric characters only) [SqlUserDefinedPatternCheck1]: | `NoDeleteFrom`                                                  |
| Set the Severity to return a code of 0-4 when triggered. (options: 'INFO'=0, 'MINOR'=1, 'MAJOR'=2, 'CRITICAL'=3, 'BLOCKER'=4)? [INFO]: | `<Choose a value: 0, 1, 2, 3, 4>`                               |
| Set 'SEARCH_STRING' (options: a string, or a valid regular expression): | `(?i)delete\s*from`                                             |
| Set 'MESSAGE' [A match for regular expression <SEARCH_STRING> was detected in Changeset <CHANGESET>.]: | `DELETE FROM statements are not allowed.`                       |
| Set 'STRIP_COMMENTS' (options: true, false) [true]: | `true`                                                          |

