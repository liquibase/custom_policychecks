# CreateTableMustHavePartition

Every `CREATE TABLE` statement must also have a `PARTITION` included.

regex: `(?is)(?=.*\b(create)\b)(?=.*\b(table)\b)(?!.*\b(partition)\b).*`

# Sample Passing Script
``` sql
--changeset amalik:employee
CREATE TABLE employee (
   id  NUMBER(5), 
   name VARCHAR2(30), 
   week_no NUMBER(2)) 
   PARTITION BY HASH(id) 
   PARTITIONS 4 
   STORE IN (data1, data2, data3, data4
);
```
# Sample Failing Scripts
``` sql
--changeset amalik:sales
CREATE TABLE sales (
   salesman_id  NUMBER(5), 
   salesman_name VARCHAR2(30), 
   sales_amount  NUMBER(10), 
   week_no       NUMBER(2)
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
Message:            Error! CREATE TABLE statement include PARTITION information.
```

# Step-by-Step
| Prompt | Command or User Input |
| ------ | ----------------------|
| > | `liquibase checks customize --check-name=SqlUserDefinedPatternCheck` |
| Give your check a short name for easier identification (up to 64 alpha-numeric characters only) [SqlUserDefinedPatternCheck1]: | `CreateTableMustHavePartition` |
| Set the Severity to return a code of 0-4 when triggered. (options: 'INFO'=0, 'MINOR'=1, 'MAJOR'=2, 'CRITICAL'=3, 'BLOCKER'=4)? [INFO]: | `<Choose a value: 0, 1, 2, 3, 4>` |
| Set 'SEARCH_STRING' (options: a string, or a valid regular expression): | `(?is)(?=.*\b(create)\b)(?=.*\b(table)\b)(?!.*\b(partition)\b).*` |
| Set 'MESSAGE' [A match for regular expression <SEARCH_STRING> was detected in Changeset <CHANGESET>.]: | `Error! CREATE TABLE statement include PARTITION information.` |
| Set 'STRIP_COMMENTS' (options: true, false) [true]: | `true` |
