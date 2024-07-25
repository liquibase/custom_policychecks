# CreateTableMustHaveIFNOTEXIST

Every `CREATE TABLE` statement must use `IF NOT EXISTS` syntax.

regex: `(?is)(?=.*\b(create)\b)(?=.*\b(table)\b)(?!.*\b(if)\b)(?!.*\b(not)\b)(?!.*\b(exists)\b).*`

# Sample Passing Script
``` sql
--changeset amalik:employee
CREATE TABLE EMPLOYEE (
   EMPLOYEE_ID INT NOT NULL GENERATED ALWAYS AS IDENTITY	CONSTRAINT PEOPLE_PK PRIMARY KEY, 
   FIRST_NAME VARCHAR(26),
   LAST_NAME VARCHAR(26)
);

--changeset amalik:cyclist_name
CREATE TABLE IF NOT EXISTS cycling.cyclist_name (
  id UUID PRIMARY KEY,
  lastname text,
  firstname text
);
```
# Sample Failing Scripts
``` sql
--changeset amalik:cyclist_name
CREATE TABLE cycling.cyclist_name (
  id UUID PRIMARY KEY,
  lastname text,
  firstname text
);
```

# Sample Error Message
```
CHANGELOG CHECKS
----------------
Checks completed validation of the changelog and found the following issues:

Check Name:         Check for specific patterns in sql (CreateTableMustHaveIFNOTEXIST)
Changeset ID:       cyclist_name
Changeset Filepath: main/100_ddl/06_CassandraDDL.sql
Check Severity:     BLOCKER (Return code: 4)
Message:            Error! CREATE TABLE statement must use "IF NOT EXISTS" syntax.
```

# Step-by-Step
| Prompt | Command or User Input |
| ------ | ----------------------|
| > | `liquibase checks customize --check-name=SqlUserDefinedPatternCheck` |
| Give your check a short name for easier identification (up to 64 alpha-numeric characters only) [SqlUserDefinedPatternCheck1]: | `CreateTableMustHaveIFNOTEXIST` |
| Set the Severity to return a code of 0-4 when triggered. (options: 'INFO'=0, 'MINOR'=1, 'MAJOR'=2, 'CRITICAL'=3, 'BLOCKER'=4)? [INFO]: | `<Choose a value: 0, 1, 2, 3, 4>` |
| Set 'SEARCH_STRING' (options: a string, or a valid regular expression): | `(?is)(?=.*\b(create)\b)(?=.*\b(table)\b)(?!.*\b(if)\b)(?!.*\b(not)\b)(?!.*\b(exists)\b).*` |
| Set 'MESSAGE' [A match for regular expression <SEARCH_STRING> was detected in Changeset <CHANGESET>.]: | `Error! CREATE TABLE statement must use "IF NOT EXISTS" syntax.` |
| Set 'STRIP_COMMENTS' (options: true, false) [true]: | `true` |
