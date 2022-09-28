# NoOpenDataSource

No statements with `OPENDATASOURCE` allowed. 

regex: `(?i:opendatasource)\s*\(`

# Sample Failing Scripts
``` sql
--changeset amalik:open_datasource
SELECT GroupName, Name, DepartmentID  
FROM OPENDATASOURCE('MSOLEDBSQL', 'Server=Seattle1;Database=AdventureWorks2016;TrustServerCertificate=Yes;Trusted_Connection=Yes;').HumanResources.Department  
ORDER BY GroupName, Name;  
```

# Sample Error Message
``` 
CHANGELOG CHECKS
----------------
Checks completed validation of the changelog and found the following issues:

Check Name:         Check for specific patterns in sql (NoOpenDataSource)
Changeset ID:       open_datasource
Changeset Filepath: changeLogs/3_data/opendatasource.sql
Check Severity:     INFO (Return code: 4)
Message:            Error! OPENDATASOURCE detected.
```

# Step-by-Step
| Prompt | Command or User Input |
| ------ | ----------------------|
| > | `liquibase checks customize --check-name=SqlUserDefinedPatternCheck` |
| Give your check a short name for easier identification (up to 64 alpha-numeric characters only) [SqlUserDefinedPatternCheck1]: | `NoOpenDataSource` |
| Set the Severity to return a code of 0-4 when triggered. (options: 'INFO'=0, 'MINOR'=1, 'MAJOR'=2, 'CRITICAL'=3, 'BLOCKER'=4)? [INFO]: | `<Choose a value: 0, 1, 2, 3, 4>` |
| Set 'SEARCH_STRING' (options: a string, or a valid regular expression): | `(?i:opendatasource)\s*\(` |
| Set 'MESSAGE' [A match for regular expression <SEARCH_STRING> was detected in Changeset <CHANGESET>.]: | `Error! OPENDATASOURCE detected.` |
| Set 'STRIP_COMMENTS' (options: true, false) [true]: | `true` |
