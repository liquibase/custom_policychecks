# NoAlterTable

Every `ALTER TABLE` statement should be flagged.

regex: `(?i:alter)[\t\r\n\s]+(?i:table)[\t\r\n\s]+`

# Sample Failing Scripts
``` sql
--changeset amalik:alter_sales
ALTER TABLE dbo.sales
   ADD COUNTRY varchar(50);
```

# Sample Error Message
```
CHANGELOG CHECKS
----------------
Checks completed validation of the changelog and found the following issues:

Check Name:         Check for specific patterns in sql (NoAlterTable)
Changeset ID:       alter_sales
Changeset Filepath: changeLogs/1_tables/01_createTable1.sql
Check Severity:     INFO (Return code: 0)
Message:            Warning! ALTER TABLE statements found.
```

# Step-by-Step
| Prompt | Command or User Input |
| ------ | ----------------------|
| > | `liquibase checks customize --check-name=SqlUserDefinedPatternCheck` |
| Give your check a short name for easier identification (up to 64 alpha-numeric characters only) [SqlUserDefinedPatternCheck1]: | `NoAlterTable` |
| Set the Severity to return a code of 0-4 when triggered. (options: 'INFO'=0, 'MINOR'=1, 'MAJOR'=2, 'CRITICAL'=3, 'BLOCKER'=4)? [INFO]: | `<Choose a value: 0, 1, 2, 3, 4>` |
| Set 'SEARCH_STRING' (options: a string, or a valid regular expression): | `(?i:alter)[\t\r\n\s]+(?i:table)[\t\r\n\s]+` |
| Set 'MESSAGE' [A match for regular expression <SEARCH_STRING> was detected in Changeset <CHANGESET>.]: | `Warning! ALTER TABLE statements found.` |
| Set 'STRIP_COMMENTS' (options: true, false) [true]: | `true` |
