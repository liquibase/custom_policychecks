# CreateTableMustHaveOneGrant

Every `CREATE TABLE` statement must also have at least one `GRANT` included.

regex: `(?is)(?=.*\b(create\s+table)\b)(?!.*\b(grant)\b).*`

# Sample Passing Script
``` sql
--changeset amalik:employee
CREATE TABLE EMPLOYEE (
   EMPLOYEE_ID INT NOT NULL GENERATED ALWAYS AS IDENTITY	CONSTRAINT PEOPLE_PK PRIMARY KEY, 
   FIRST_NAME VARCHAR(26),
   LAST_NAME VARCHAR(26)
);
GRANT select ON EMPLOYEE to APPUSER;
```
# Sample Failing Scripts
``` sql
--changeset amalik:employee
CREATE TABLE EMPLOYEE (
   EMPLOYEE_ID INT NOT NULL GENERATED ALWAYS AS IDENTITY	CONSTRAINT PEOPLE_PK, 
   FIRST_NAME VARCHAR(26),
   LAST_NAME VARCHAR(26)
);
```

# Sample Error Message
```
CHANGELOG CHECKS
----------------
Checks completed validation of the changelog and found the following issues:

Check Name:         Check for specific patterns in sql (CreateTableMustHaveOneGrant)
Changeset ID:       EMPLOYEE
Changeset Filepath: script1.sql
Check Severity:     MAJOR (Return code: 2)
Message:            Error! CREATE TABLE statement found but there was no GRANT found. Every CREATE TABLE must have at least one GRANT statement.
```

# Step-by-Step
| Prompt | Command or User Input |
| ------ | ----------------------|
| > | `liquibase checks customize --check-name=SqlUserDefinedPatternCheck` |
| Give your check a short name for easier identification (up to 64 alpha-numeric characters only) [SqlUserDefinedPatternCheck1]: | `CreateTableMustHaveOneGrant` |
| Set the Severity to return a code of 0-4 when triggered. (options: 'INFO'=0, 'MINOR'=1, 'MAJOR'=2, 'CRITICAL'=3, 'BLOCKER'=4)? [INFO]: | `<Choose a value: 0, 1, 2, 3, 4>` |
| Set 'SEARCH_STRING' (options: a string, or a valid regular expression): | `(?is)(?=.*\b(create\s+table)\b)(?!.*\b(grant)\b).*` |
| Set 'MESSAGE' [A match for regular expression <SEARCH_STRING> was detected in Changeset <CHANGESET>.]: | `Error! CREATE TABLE statement found but there was no GRANT found. Every CREATE TABLE must have at least one GRANT statement.` |
| Set 'STRIP_COMMENTS' (options: true, false) [true]: | `true` |
| Set 'PATH_FILTER_REGEX': | _leave blank_ |
| Set 'SPLIT_STATEMENTS' to split multiple SQL statements on the delimiter, and evaluate each individually (options: true, false) [false]: | false |
