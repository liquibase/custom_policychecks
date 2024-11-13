# NoDataDmlStatements

Do not allow any upper/lowercase variation of the string "databasechangelog" outside comments.

regex: `(?i)databasechangelog`

# Sample Failing Scripts
``` sql
DELETE FROM databasechangelog WHERE condition;
```
``` sql
UPDATE DATABASECHANGELOGHISTORY
SET column1 = value1, column2 = value2, ...
WHERE condition;
```
``` sql
DROP TABLE DATABASECHANGELOGlock;
```

# Sample Error Message
```
CHANGELOG CHECKS
----------------
Checks completed validation of the changelog and found the following issues:

Check Name:         Check for specific patterns in sql (ForbidDBCLKeyword)
Changeset ID:       myChangeset
Changeset Filepath: root_changelog.xml
Check Severity:     BLOCKER (Return code: 4)
Message:            A match for regular expression (?i)databasechangelog was detected in Changeset myChangeset.
```
# Step-by-Step

| Prompt | Command or User Input                                                                                                                   |
| ------ |-----------------------------------------------------------------------------------------------------------------------------------------|
| > | `liquibase checks copy --check-name=SqlUserDefinedPatternCheck`                                                                         |
| Give your check a short name for easier identification (up to 64 alpha-numeric characters only) [SqlUserDefinedPatternCheck1]: | `ForbidDBCLKeyword`                                                                                                                     |
| Set the Severity to return a code of 0-4 when triggered. (options: 'INFO'=0, 'MINOR'=1, 'MAJOR'=2, 'CRITICAL'=3, 'BLOCKER'=4)? [INFO]: | `<Choose a value: 0, 1, 2, 3, 4>`                                                                                                       |
| Set 'SEARCH_STRING' (options: a string, or a valid regular expression): | `(?i)databasechangelog`                                                                                                                 |
| Set 'MESSAGE' [A match for regular expression <SEARCH_STRING> was detected in Changeset <CHANGESET>.]: | `SQL referencing Liquibase tables is not allowed. A match for regular expression <SEARCH_STRING> was detected in Changeset <CHANGESET>` |
| Set 'STRIP_COMMENTS' (options: true, false) [true]: | `true`                                                                                                                                  |

