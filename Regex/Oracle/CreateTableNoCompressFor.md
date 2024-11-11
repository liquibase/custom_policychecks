# CreateTableNoCompressFor

Disallow the use of `COMPRESS FOR` in `CREATE TABLE` statements (only allow compress or compress basic).

regex: `(?is)(?=.*\b(create)\b)(?=.*\b(table)\b)(?=.*\b(compress)\b)(?=.*\b(for)\b).*`

# Sample Passing Script
``` sql
--changeset amalik:employee
CREATE TABLE EMPLOYEE (
   EMPLOYEE_ID INT NOT NULL GENERATED ALWAYS AS IDENTITY	CONSTRAINT PEOPLE_PK PRIMARY KEY, 
   FIRST_NAME VARCHAR(26),
   LAST_NAME VARCHAR(26)
)
NOLOGGING
COMPRESS BASIC
NOCACHE
MONITORING;

--changeset amalik:company
CREATE TABLE COMPANY (
   COMPANY_ID INT NOT NULL, 
   BOOKING_DATE DATE NOT NULL,
	ROOMS_TAKEN INT DEFAULT 0, 
   PRIMARY KEY (COMPANY_ID, BOOKING_DATE)
)
NOLOGGING
COMPRESS
NOCACHE
MONITORING;
```

# Sample Failing Scripts
``` sql
--changeset amalik:employee
CREATE TABLE EMPLOYEE (
   EMPLOYEE_ID INT NOT NULL GENERATED ALWAYS AS IDENTITY	CONSTRAINT PEOPLE_PK, 
   FIRST_NAME VARCHAR(26),
   LAST_NAME VARCHAR(26)
)
NOLOGGING
COMPRESS FOR OLTP
NOCACHE
MONITORING;

--changeset amalik:company
CREATE TABLE COMPANY (
   COMPANY_ID INT NOT NULL, 
   BOOKING_DATE DATE NOT NULL,
	ROOMS_TAKEN INT DEFAULT 0, 
)
NOLOGGING
COMPRESS FOR QUERY HIGH
NOCACHE
MONITORING;
```

# Sample Error Message
```
CHANGELOG CHECKS
----------------
Checks completed validation of the changelog and found the following issues:

Check Name:         Check for specific patterns in sql (CreateTableNoCompressFor)
Changeset ID:       employee
Changeset Filepath: main/100_ddl/07_compressionDDL.sql
Check Severity:     BLOCKER (Return code: 4)
Message:            Error! COMPRESS FOR is not allowed in a CREATE TABLE statement.
```

# Step-by-Step
| Prompt | Command or User Input |
| ------ | ----------------------|
| > | `liquibase checks customize --check-name=SqlUserDefinedPatternCheck` |
| Give your check a short name for easier identification (up to 64 alpha-numeric characters only) [SqlUserDefinedPatternCheck1]: | `CreateTableNoCompressFor` |
| Set the Severity to return a code of 0-4 when triggered. (options: 'INFO'=0, 'MINOR'=1, 'MAJOR'=2, 'CRITICAL'=3, 'BLOCKER'=4)? [INFO]: | `<Choose a value: 0, 1, 2, 3, 4>` |
| Set 'SEARCH_STRING' (options: a string, or a valid regular expression): | `(?is)(?=.*\b(create)\b)(?=.*\b(table)\b)(?=.*\b(compress)\b)(?=.*\b(for)\b).*` |
| Set 'MESSAGE' [A match for regular expression <SEARCH_STRING> was detected in Changeset <CHANGESET>.]: | `Error! COMPRESS FOR is not allowed in a CREATE TABLE statement.` |
| Set 'STRIP_COMMENTS' (options: true, false) [true]: | `true` |
