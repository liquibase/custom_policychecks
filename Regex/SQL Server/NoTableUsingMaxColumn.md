# NoTableUsingMaxColumn

Avoid using MAX. Consider VARCHAR(8000) or less instead.

regex: `(?i)(?:CREATE|ALTER)\s+TABLE\s+.*?\b(?:VARCHAR|NVARCHAR|VARBINARY)\s*\(\s*MAX\s*\)`

# Sample Failing Scripts
``` sql
--changeset asmith:alter_table
ALTER TABLE [dbo].[table01] ADD column_a varbinary(max) NULL;
```

# Sample Error Message
``` 
CHANGELOG CHECKS
----------------
Checks completed validation of the changelog and found the following issues:

Check Name:         Check for specific patterns in sql (NoTableUsingMaxColumn)
Changeset ID:       alter_table
Changeset Filepath: changeLogs/1_tables/01_createTable1.sql
Check Severity:     INFO (Return code: 0)
Message:            Warning! Avoid using MAX. Consider VARCHAR(8000) or less instead.
```

# Step-by-Step
| Prompt | Command or User Input |
| ------ | ----------------------|
| > | `liquibase checks customize --check-name=SqlUserDefinedPatternCheck` |
| Give your check a short name for easier identification (up to 64 alpha-numeric characters only) [SqlUserDefinedPatternCheck1]: | `NoTableUsingMaxColumn` |
| Set the Severity to return a code of 0-4 when triggered. (options: 'INFO'=0, 'MINOR'=1, 'MAJOR'=2, 'CRITICAL'=3, 'BLOCKER'=4)? [INFO]: | `<Choose a value: 0, 1, 2, 3, 4>` |
| Set 'SEARCH_STRING' (options: a string, or a valid regular expression): | `(?i)(?:CREATE\|ALTER)\s+TABLE\s+.*?\b(?:VARCHAR\|NVARCHAR\|VARBINARY)\s*\(\s*MAX\s*\)` |
| Set 'MESSAGE' [A match for regular expression <SEARCH_STRING> was detected in Changeset <CHANGESET>.]: | `Warning! Avoid using MAX. Consider VARCHAR(8000) or less instead.` |
| Set 'STRIP_COMMENTS' (options: true, false) [true]: | `true` |
