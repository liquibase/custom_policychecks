# DoNotUseQaOrProdDatabases

Do not use *_QA or *_PROD databases (when deployment is restricted to *_DEV database only).


regex: `(?is)(?=create|drop|alter|insert|select|delete).*(?:_prod|_qa)\.`

# Sample Passing Scripts
``` sql
CREATE TABLE myschema.table1 (val1 number, val2 date);
```

# Sample Failing Scripts
``` sql
CREATE TABLE CMS_QA.myschema.table1 (val1 number, val2 date);
```
```sql
CREATE TABLE CMS_PROD.myschema.table1 (val1 number, val2 date);
```

# Sample Error Message
``` 
CHANGELOG CHECKS
----------------
Checks completed validation of the changelog and found the following issues:

Check Name:         Check for specific patterns in sql (DoNotUseQaOrProdDatabases)
Changeset ID:       1
Changeset Filepath: Changelogs/adeel1.sql
Check Severity:     BLOCKER (Return code: 4)
Message:            Error! Do not use *_QA or *_PROD databases (deployment is restricted to *_DEV databases only)
```

# Step-by-Step
| Prompt | Command or User Input |
| ------ | ----------------------|
| > | `liquibase checks customize --check-name=SqlUserDefinedPatternCheck` |
| Give your check a short name for easier identification (up to 64 alpha-numeric characters only) [SqlUserDefinedPatternCheck1]: | `DoNotUseQaOrProdDatabases` |
| Set the Severity to return a code of 0-4 when triggered. (options: 'INFO'=0, 'MINOR'=1, 'MAJOR'=2, 'CRITICAL'=3, 'BLOCKER'=4)? [INFO]: | `<Choose a value: 0, 1, 2, 3, 4>` |
| Set 'SEARCH_STRING' (options: a string, or a valid regular expression): | `(?is)(?=create\|drop\|alter\|insert\|select\|delete).*(?:_prod\|_qa)\.` |
| Set 'MESSAGE' [A match for regular expression <SEARCH_STRING> was detected in Changeset <CHANGESET>.]: | `Error! Do not use *_QA or *_PROD databases (deployment is restricted to *_DEV databases only)` |
| Set 'STRIP_COMMENTS' (options: true, false) [true]: | `true` |
| Set 'PATH_FILTER_REGEX': | `false` |
Set 'SPLIT_STATEMENTS' to split multiple SQL statements on the delimiter, and evaluate each individually (options: true, false) [false]:  | `false` |
