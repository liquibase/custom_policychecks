# MultipleCreateTablesNotAllowed

No `CREATE TABLE` statements allowed except for creating temporary tables.

regex: `(?is)[\t\r\n\s]*\bcreate\b[\t\r\n\s]+\btable\b[\t\r\n\s]+.*[\t\r\n\s]+\bcreate\b[\t\r\n\s]+\btable\b[\t\r\n\s]+`

# Sample Passing Script
``` sql
--changeset amalik:sales1
CREATE TABLE sales1 (
   ID int NOT NULL PRIMARY KEY,
   NAME varchar(20),
   REGION varchar(20),
   MARKET varchar(20)
)
```
# Sample Failing Scripts
``` sql
--changeset amalik:sales2
CREATE TABLE sales2 (
   ID int NOT NULL,
   NAME varchar(20),
   REGION varchar(20),
   MARKET varchar(20)
)
CREATE TABLE dbo.#sales22 (
   ID int NOT NULL,
   NAME varchar(20),
   REGION varchar(20),
   MARKET varchar(20)
)
```

# Sample Error Message
```
CHANGELOG CHECKS
----------------
Checks completed validation of the changelog and found the following issues:

Check Name:         Check for specific patterns in sql (MultipleCreateTablesNotAllowed)
Changeset ID:       sales2
Changeset Filepath: changeLogs/1_tables/01_createTable1.sql
Check Severity:     BLOCKER (Return code: 4)
Message:            Error! Multiple CREATE TABLE statements not allowed in a
                    single script. Only a single CREATE TABLE statement is allowed.
```

# Step-by-Step
| Prompt | Command or User Input |
| ------ | ----------------------|
| > | `liquibase checks customize --check-name=SqlUserDefinedPatternCheck` |
| Give your check a short name for easier identification (up to 64 alpha-numeric characters only) [SqlUserDefinedPatternCheck1]: | `MultipleCreateTablesNotAllowed` |
| Set the Severity to return a code of 0-4 when triggered. (options: 'INFO'=0, 'MINOR'=1, 'MAJOR'=2, 'CRITICAL'=3, 'BLOCKER'=4)? [INFO]: | `<Choose a value: 0, 1, 2, 3, 4>` |
| Set 'SEARCH_STRING' (options: a string, or a valid regular expression): | `(?is)[\t\r\n\s]*\bcreate\b[\t\r\n\s]+\btable\b[\t\r\n\s]+.*[\t\r\n\s]+\bcreate\b[\t\r\n\s]+\btable\b[\t\r\n\s]+` |
| Set 'MESSAGE' [A match for regular expression <SEARCH_STRING> was detected in Changeset <CHANGESET>.]: | `Error! Multiple CREATE TABLE statements not allowed in a single script. Only a single CREATE TABLE statement is allowed.` |
| Set 'STRIP_COMMENTS' (options: true, false) [true]: | `true` |
