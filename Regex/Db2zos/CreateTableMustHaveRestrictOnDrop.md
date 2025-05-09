# CreateTableMustHaveRestrictOnDrop

CREATE TABLE statements must include WITH RESTRICT ON DROP.

regex: `(?is)(?=.*\b(create)\b)(?=.*\b(table)\b)(?!.*\b(with\s*restrict\s*on\s*drop)\b)`

# Sample Passing Scripts
``` sql
--changeset asmith:create_table_01
CREATE TABLE TEST_TABLE_01 (
	ID INT GENERATED BY DEFAULT AS IDENTITY 
		(START WITH 10 INCREMENT BY 10),
	FIRSTNAME VARCHAR(50),
	LASTNAME VARCHAR(50) NOT NULL
)
  WITH RESTRICT ON DROP;
```

# Sample Failing Scripts
``` sql
--changeset asmith:create_table_without_restrict_on_drop
CREATE TABLE TEST_TABLE_02 (
	ID INT GENERATED BY DEFAULT AS IDENTITY 
		(START WITH 10 INCREMENT BY 10),
	FIRSTNAME VARCHAR(50),
	LASTNAME VARCHAR(50) NOT NULL
);
```

# Sample Error Message
``` 
CHANGELOG CHECKS
----------------
Checks completed validation of the changelog and found the following issues:

Check Name:         Check for specific patterns in sql (CreateTableMustHaveRestrictOnDrop)
Changeset ID:       create_table_without_restrict_on_drop
Changeset Filepath: sql_code/Scripts/TABLES_01.sql
Check Severity:     BLOCKER (Return code: 4)
Message:            Error! CREATE TABLE must include WITH RESTRICT ON DROP.
```

# Step-by-Step
| Prompt | Command or User Input |
| ------ | ----------------------|
| > | `liquibase checks customize --check-name=SqlUserDefinedPatternCheck` |
| Give your check a short name for easier identification (up to 64 alpha-numeric characters only) [SqlUserDefinedPatternCheck1]: | `CreateTableMustHaveRestrictOnDrop` |
| Set the Severity to return a code of 0-4 when triggered. (options: 'INFO'=0, 'MINOR'=1, 'MAJOR'=2, 'CRITICAL'=3, 'BLOCKER'=4)? [INFO]: | `<Choose a value: 0, 1, 2, 3, 4>` |
| Set 'SEARCH_STRING' (options: a string, or a valid regular expression): | `(?is)(?=.*\b(create)\b)(?=.*\b(table)\b)(?!.*\b(with\s*restrict\s*on\s*drop)\b)` |
| Set 'MESSAGE' [A match for regular expression <SEARCH_STRING> was detected in Changeset <CHANGESET>.]: | `Error! CREATE TABLE must include WITH RESTRICT ON DROP.` |
| Set 'STRIP_COMMENTS' (options: true, false) [true]: | `true` |
