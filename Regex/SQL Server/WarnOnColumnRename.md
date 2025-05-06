# WarnOnColumnRename

`EXECUTE sp_rename ... 'COLUMN';` not allowed.

regex: `(?is)EXEC(?:UTE)?\s*sp_rename.+'COLUMN'$`

# Sample Passing Script
``` sql
--changeset dev01:rename_column_test_pass
EXECUTE sp_rename 'Sales.SalesTerritory', 'SalesTerr';
 ```
# Sample Failing Script
``` sql
--changeset dev01:rename_column_test_fail
EXEC sp_rename 'Sales.SalesTerritory.TerritoryID', 'TerrID', 'COLUMN';
```

# Sample Error Message
``` 
CHANGELOG CHECKS
----------------
Checks completed validation of the changelog and found the following issues:

Check Name:         Check for specific patterns in sql (WarnOnColumnRename)
Changeset ID:       rename_column_test_fail
Changeset Filepath: sqlcode/1.0/schema1/changelog.yaml :: rename_column_fail.sql
Check Severity:     INFO (Return code: 0)
Message:            WARNING: Column renamed in Changeset rename_column_test_fail.
```

# Step-by-Step
| Prompt | Command or User Input |
| ------ | ----------------------|
| > | `liquibase checks customize --check-name=SqlUserDefinedPatternCheck` |
| Give your check a short name for easier identification (up to 64 alpha-numeric characters only) [SqlUserDefinedPatternCheck1]: | `WarnOnColumnRename` |
| Set the Severity to return a code of 0-4 when triggered. (options: 'INFO'=0, 'MINOR'=1, 'MAJOR'=2, 'CRITICAL'=3, 'BLOCKER'=4)? [INFO]: | `<Choose a value: 0, 1, 2, 3, 4>` |
| Set 'SEARCH_STRING' (options: a string, or a valid regular expression): | `(?is)EXEC(?:UTE)?\s*sp_rename.+'COLUMN'$` |
| Set 'MESSAGE' [A match for regular expression <SEARCH_STRING> was detected in Changeset <CHANGESET>.]: | `WARNING: Column renamed in Changeset <CHANGESET>.` |
| Set 'STRIP_COMMENTS' (options: true, false) [true]: | `true` |
| Set 'PATH_FILTER_REGEX': |  |
| Set 'STRIP_COMMENTS' (options: true, false) [true]: | `true` |
