# CreateTableWithCertainColumnRequiresSequence

CREATE TABLE statement with a certain column (e.g., `SQLKEY`) requires that there must also be a CREATE SEQUENCE included.

regex: `(?is)(?=.*\b(create.*table.*sqlkey\s+number)\b)(?!.*\b(create\s+sequence)\b).*`

# Sample Passing Script
``` sql
--changeset amalik:employee
CREATE TABLE EMPLOYEE (
   SQLKEY NUMBER(15,0),
   EMPLOYEE_ID INT NOT NULL GENERATED ALWAYS AS IDENTITY	CONSTRAINT PEOPLE_PK PRIMARY KEY, 
   FIRST_NAME VARCHAR(26),
   LAST_NAME VARCHAR(26)
);
CREATE SEQUENCE SEQ_EMPLOYEE MINVALUE 1 MAXVALUE 999999999999 INCREMENT BY 1 START WITH 1 CACHE NOORDER NOCYCLE;
```
# Sample Failing Scripts
``` sql
--changeset amalik:employee
CREATE TABLE EMPLOYEE (
   SQLKEY NUMBER(15,0),
   EMPLOYEE_ID INT NOT NULL GENERATED ALWAYS AS IDENTITY	CONSTRAINT PEOPLE_PK PRIMARY KEY, 
   FIRST_NAME VARCHAR(26),
   LAST_NAME VARCHAR(26)
);
```

# Sample Error Message
```
CHANGELOG CHECKS
----------------
Checks completed validation of the changelog and found the following issues:

Check Name:         Check for specific patterns in sql (CreateTableWithCertainColumnRequiresSequence)
Changeset ID:       PMA0087
Changeset Filepath: script1.sql
Check Severity:     MAJOR (Return code: 2)
Message:            Error! SQLKEY column requires creation of a SEQUENCE. Ensure that you have a CREATE SEQUENCE in your changeset.
```

# Step-by-Step
| Prompt | Command or User Input |
| ------ | ----------------------|
| > | `liquibase checks customize --check-name=SqlUserDefinedPatternCheck` |
| Give your check a short name for easier identification (up to 64 alpha-numeric characters only) [SqlUserDefinedPatternCheck1]: | `CreateTableWithCertainColumnRequiresSequence` |
| Set the Severity to return a code of 0-4 when triggered. (options: 'INFO'=0, 'MINOR'=1, 'MAJOR'=2, 'CRITICAL'=3, 'BLOCKER'=4)? [INFO]: | `<Choose a value: 0, 1, 2, 3, 4>` |
| Set 'SEARCH_STRING' (options: a string, or a valid regular expression): | `(?is)(?=.*\b(create.*table.*sqlkey\s+number)\b)(?!.*\b(create\s+sequence)\b).*` |
| Set 'MESSAGE' [A match for regular expression <SEARCH_STRING> was detected in Changeset <CHANGESET>.]: | `Error! SQLKEY column requires creation of a SEQUENCE. Ensure that you have a CREATE SEQUENCE in your changeset.` |
| Set 'STRIP_COMMENTS' (options: true, false) [true]: | `true` |
| Set 'PATH_FILTER_REGEX': | _leave blank_ |
| Set 'SPLIT_STATEMENTS' to split multiple SQL statements on the delimiter, and evaluate each individually (options: true, false) [false]: | false |
