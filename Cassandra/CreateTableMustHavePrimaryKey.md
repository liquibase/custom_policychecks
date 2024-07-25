# CreateTableMustHavePrimaryKey

Every `CREATE TABLE` statement must also have a `PRIMARY KEY` included.

regex: `(?is)(?=.*\b(create)\b)(?=.*\b(table)\b)(?!.*\b(primary)\b)(?!.*\b(key)\b).*`

# Sample Passing Script
``` sql
--changeset amalik:employee
CREATE TABLE EMPLOYEE (
   EMPLOYEE_ID INT NOT NULL GENERATED ALWAYS AS IDENTITY	CONSTRAINT PEOPLE_PK PRIMARY KEY, 
   FIRST_NAME VARCHAR(26),
   LAST_NAME VARCHAR(26)
);

--changeset amalik:company
CREATE TABLE COMPANY (
   COMPANY_ID INT NOT NULL, 
   BOOKING_DATE DATE NOT NULL,
	ROOMS_TAKEN INT DEFAULT 0, 
   PRIMARY KEY (COMPANY_ID, BOOKING_DATE)
);
```
# Sample Failing Scripts
``` sql
--changeset amalik:employee
CREATE TABLE EMPLOYEE (
   EMPLOYEE_ID INT NOT NULL GENERATED ALWAYS AS IDENTITY	CONSTRAINT PEOPLE_PK, 
   FIRST_NAME VARCHAR(26),
   LAST_NAME VARCHAR(26)
);

--changeset amalik:company
CREATE TABLE COMPANY (
   COMPANY_ID INT NOT NULL, 
   BOOKING_DATE DATE NOT NULL,
	ROOMS_TAKEN INT DEFAULT 0, 
;
```

# Sample Error Message
```
CHANGELOG CHECKS
----------------
Checks completed validation of the changelog and found the following issues:

Check Name:         Check for specific patterns in sql (CreateTableMustHavePrimaryKey)
Changeset ID:       employee
Changeset Filepath: changeLogs/1_tables/01_createTable1.sql
Check Severity:     INFO (Return code: 0)
Message:            Error! CREATE TABLE statement must have a primary key
                    included.
```

# Step-by-Step
| Prompt | Command or User Input |
| ------ | ----------------------|
| > | `liquibase checks customize --check-name=SqlUserDefinedPatternCheck` |
| Give your check a short name for easier identification (up to 64 alpha-numeric characters only) [SqlUserDefinedPatternCheck1]: | `CreateTableMustHavePrimaryKey` |
| Set the Severity to return a code of 0-4 when triggered. (options: 'INFO'=0, 'MINOR'=1, 'MAJOR'=2, 'CRITICAL'=3, 'BLOCKER'=4)? [INFO]: | `<Choose a value: 0, 1, 2, 3, 4>` |
| Set 'SEARCH_STRING' (options: a string, or a valid regular expression): | `(?is)(?=.*\b(create)\b)(?=.*\b(table)\b)(?!.*\b(primary)\b)(?!.*\b(key)\b).*` |
| Set 'MESSAGE' [A match for regular expression <SEARCH_STRING> was detected in Changeset <CHANGESET>.]: | `Error! CREATE TABLE statement must have a primary key included.` |
| Set 'STRIP_COMMENTS' (options: true, false) [true]: | `true` |
