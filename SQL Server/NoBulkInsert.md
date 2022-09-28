# NoBulkInsert

No statements with `BULK INSERT` allowed. 

regex: `(?i:bulk\s)\s*(?i:insert\s)`

# Sample Failing Scripts
``` sql
--changeset amalik:bulk_insert
BULK INSERT Sales
FROM 'C:\temp\1500000 Sales Records.csv'
WITH (FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR='\n',
    BATCHSIZE=250000,
    MAXERRORS=2);
```

# Sample Error Message
``` 
CHANGELOG CHECKS
----------------
Checks completed validation of the changelog and found the following issues:

Check Name:         Check for specific patterns in sql (NoBulkInsert)
Changeset ID:       bulk_insert
Changeset Filepath: changeLogs/3_data/bulkinsert.sql
Check Severity:     INFO (Return code: 4)
Message:            Error! BULK INSERT detected.
```

# Step-by-Step
| Prompt | Command or User Input |
| ------ | ----------------------|
| > | `liquibase checks customize --check-name=SqlUserDefinedPatternCheck` |
| Give your check a short name for easier identification (up to 64 alpha-numeric characters only) [SqlUserDefinedPatternCheck1]: | `NoBulkInsert` |
| Set the Severity to return a code of 0-4 when triggered. (options: 'INFO'=0, 'MINOR'=1, 'MAJOR'=2, 'CRITICAL'=3, 'BLOCKER'=4)? [INFO]: | `<Choose a value: 0, 1, 2, 3, 4>` |
| Set 'SEARCH_STRING' (options: a string, or a valid regular expression): | `(?i:bulk\s)\s*(?i:insert\s)` |
| Set 'MESSAGE' [A match for regular expression <SEARCH_STRING> was detected in Changeset <CHANGESET>.]: | `Error! BULK INSERT detected.` |
| Set 'STRIP_COMMENTS' (options: true, false) [true]: | `true` |
