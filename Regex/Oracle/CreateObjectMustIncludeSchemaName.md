# CreateObjectMustIncludeSchemaName

CREATE OBJECT statements should be fully qualified and include a schema name.

regex: `(?i)\bCREATE\s+(TABLE|VIEW|FUNCTION|PROCEDURE|INDEX|TRIGGER|SEQUENCE|SYNONYM|PACKAGE|PACKAGE\s+BODY|TYPE|TYPE\s+BODY|MATERIALIZED\s+VIEW)\s+(?![\[\"]?\w+[\]\"]?\.)[\[\"]?\w+[\]\"]?`

# Sample Passing Script
``` sql
--changeset asmith:EMPLOYEE
CREATE TABLE EMP.EMPLOYEE (
   EMPLOYEE_ID INT NOT NULL, 
   FIRST_NAME VARCHAR(26),
   LAST_NAME VARCHAR(26)
);
```
# Sample Failing Scripts
``` sql
--changeset asmith:EMPLOYEE
CREATE TABLE EMPLOYEE (
   EMPLOYEE_ID INT NOT NULL, 
   FIRST_NAME VARCHAR(26),
   LAST_NAME VARCHAR(26)
);
```

# Sample Error Message
```
CHANGELOG CHECKS
----------------
Checks completed validation of the changelog and found the following issues:

Check Name:         Check for specific patterns in sql (CreateObjectMustIncludeSchemaName)
Changeset ID:       EMPLOYEE
Changeset Filepath: script1.sql
Check Severity:     MAJOR (Return code: 2)
Message:            CREATE OBJECT statements should be fully qualified and include a schema name.
```

# Step-by-Step
| Prompt | Command or User Input |
| ------ | ----------------------|
| > | `liquibase checks customize --check-name=SqlUserDefinedPatternCheck` |
| Give your check a short name for easier identification (up to 64 alpha-numeric characters only) [SqlUserDefinedPatternCheck1]: | `CreateObjectMustIncludeSchemaName` |
| Set the Severity to return a code of 0-4 when triggered. (options: 'INFO'=0, 'MINOR'=1, 'MAJOR'=2, 'CRITICAL'=3, 'BLOCKER'=4)? [INFO]: | `<Choose a value: 0, 1, 2, 3, 4>` |
| Set 'SEARCH_STRING' (options: a string, or a valid regular expression): | `(?i)\bCREATE\s+(TABLE\|VIEW\|FUNCTION\|PROCEDURE\|INDEX\|TRIGGER\|SEQUENCE\|SYNONYM|PACKAGE\|PACKAGE\s+BODY\|TYPE\|TYPE\s+BODY\|MATERIALIZED\s+VIEW)\s+(?![\[\"]?\w+[\]\"]?\.)[\[\"]?\w+[\]\"]?` |
| Set 'MESSAGE' [A match for regular expression <SEARCH_STRING> was detected in Changeset <CHANGESET>.]: | `CREATE OBJECT statements should be fully qualified and include a schema name.` |
| Set 'STRIP_COMMENTS' (options: true, false) [true]: | `true` |
| Set 'PATH_FILTER_REGEX': | _leave blank_ |
| Set 'SPLIT_STATEMENTS' to split multiple SQL statements on the delimiter, and evaluate each individually (options: true, false) [false]: | false |
