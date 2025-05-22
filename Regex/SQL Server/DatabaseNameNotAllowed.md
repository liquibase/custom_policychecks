# DatabaseNameNotAllowed

Database name in object prefix is not allowed. E.g., `CMS_QA.dbo.uspGetCutomerCompany`.

regex: `(?is)(.+)\.(.+)\.(.+)(.+)`

# Sample Passing Scripts
```sql
CREATE TABLE lion.table1 (val1 number, val2 date);
EXEC CMS_QA.dbo.uspGetCustomerCompany N'Cannon', N'Chris';
```

# Sample Failing Scripts
```sql
CREATE TABLE EDS.lion.table1 (val1 number, val2 date);
EXEC CMS_QA.dbo.uspGetCustomerCompany N'Cannon', N'Chris';
```

# Sample Error Message
``` 
CHANGELOG CHECKS
----------------
Checks completed validation of the changelog and found the following issues:

Check Name:         Check for specific patterns in sql (DatabaseNameNotAllowed)
Changeset ID:       2
Changeset Filepath: Changelogs/adeel1.sql: Line 1
Check Severity:     MAJOR (Return code: 2)
Message:            Error! Database name in object prefix is not allowed.
```

# Step-by-Step
| Prompt | Command or User Input |
| ------ | ----------------------|
| > | `liquibase checks customize --check-name=SqlUserDefinedPatternCheck` |
| Give your check a short name for easier identification (up to 64 alpha-numeric characters only) [SqlUserDefinedPatternCheck1]: | `DatabaseNameNotAllowed` |
| Set the Severity to return a code of 0-4 when triggered. (options: 'INFO'=0, 'MINOR'=1, 'MAJOR'=2, 'CRITICAL'=3, 'BLOCKER'=4)? [INFO]: | `<Choose a value: 0, 1, 2, 3, 4>` |
| Set 'SEARCH_STRING' (options: a string, or a valid regular expression): | `(?is)(.+)\.(.+)\.(.+)(.+)` |
| Set 'MESSAGE' [A match for regular expression <SEARCH_STRING> was detected in Changeset <CHANGESET>.]: | `Error! Database name in object prefix is not allowed.` |
| Set 'STRIP_COMMENTS' (options: true, false) [true]: | `true` |