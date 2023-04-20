# CreateTableMustHaveDataRetention

CREATE TABLE statements must include parameter for DATA_RETENTION_TIME_IN_DAYS.

regex: `(?is)(?=.*\b(create)\b)(?=.*\b(table)\b)(?!.*\b(data_retention_time_in_days)\b)`

# Sample Passing Scripts
``` sql
--changeset asmith:create_order_table_with_tt
create or replace order table (
    orderkey number(38,0),
    custkey number(38,0)
)
data_retention_time_in_days=3
;
```

# Sample Failing Scripts
``` sql
--changeset asmith:create_order_table_without_tt
create or replace order table (
    orderkey number(38,0),
    custkey number(38,0)
)
;
```

# Sample Error Message
``` 
CHANGELOG CHECKS
----------------
Checks completed validation of the changelog and found the following issues:

Check Name:         Check for specific patterns in sql (CreateTableMustHaveDataRetention)
Changeset ID:       create_order_table_without_tt
Changeset Filepath: changeLogs/2_objects/01_ddl/create_order_table_without_tt.sql
Check Severity:     BLOCKER (Return code: 4)
Message:            Error! CREATE TABLE statement must have DATA_RETENTION_TIME_IN_DAYS parameter.
```

# Step-by-Step
| Prompt | Command or User Input |
| ------ | ----------------------|
| > | `liquibase checks customize --check-name=SqlUserDefinedPatternCheck` |
| Give your check a short name for easier identification (up to 64 alpha-numeric characters only) [SqlUserDefinedPatternCheck1]: | `CreateTableMustHaveDataRetention` |
| Set the Severity to return a code of 0-4 when triggered. (options: 'INFO'=0, 'MINOR'=1, 'MAJOR'=2, 'CRITICAL'=3, 'BLOCKER'=4)? [INFO]: | `<Choose a value: 0, 1, 2, 3, 4>` |
| Set 'SEARCH_STRING' (options: a string, or a valid regular expression): | `(?is)(?=.*\b(create)\b)(?=.*\b(table)\b)(?!.*\b(data_retention_time_in_days)\b)` |
| Set 'MESSAGE' [A match for regular expression <SEARCH_STRING> was detected in Changeset <CHANGESET>.]: | `Error! CREATE TABLE statement must have DATA_RETENTION_TIME_IN_DAYS parameter.` |
| Set 'STRIP_COMMENTS' (options: true, false) [true]: | `true` |
