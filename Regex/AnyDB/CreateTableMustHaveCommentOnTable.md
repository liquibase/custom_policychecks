# CreateTableMustHaveCommentOnTable

CREATE TABLE statements must include COMMENT ON TABLE statement.

regex: `(?is)(?=.*\b(create\s*table)\b)(?!.*\b(comment\s*on\s*table)\b)`

# Sample Passing Scripts
``` sql
--changeset asmith:create_table_01
CREATE TABLE TEST_TABLE_01 (
	ID,
	FIRSTNAME VARCHAR(50),
	LASTNAME VARCHAR(50) NOT NULL
);

COMMENT ON TABLE create_table_01 IS 'Table description goes here.';
```

# Sample Failing Scripts
``` sql
--changeset asmith:create_table_01_without_comment
CREATE TABLE TEST_TABLE_01 (
	ID,
	FIRSTNAME VARCHAR(50),
	LASTNAME VARCHAR(50) NOT NULL
);
```

# Sample Error Message
``` 
CHANGELOG CHECKS
----------------
Checks completed validation of the changelog and found the following issues:

Check Name:         Check for specific patterns in sql (CreateTableMustHaveCommentOnTable)
Changeset ID:       create_table_01_without_comment
Changeset Filepath: sql_code/Scripts/TABLES_01.sql
Check Severity:     BLOCKER (Return code: 4)
Message:            Error! CREATE TABLE must include COMMENT ON TABLE for table description.
```

# Step-by-Step
| Prompt | Command or User Input |
| ------ | ----------------------|
| > | `liquibase checks customize --check-name=SqlUserDefinedPatternCheck` |
| Give your check a short name for easier identification (up to 64 alpha-numeric characters only) [SqlUserDefinedPatternCheck1]: | `CreateTableMustHaveCommentOnTable` |
| Set the Severity to return a code of 0-4 when triggered. (options: 'INFO'=0, 'MINOR'=1, 'MAJOR'=2, 'CRITICAL'=3, 'BLOCKER'=4)? [INFO]: | `<Choose a value: 0, 1, 2, 3, 4>` |
| Set 'SEARCH_STRING' (options: a string, or a valid regular expression): | `(?is)(?=.*\b(create\s*table)\b)(?!.*\b(comment\s*on\s*table)\b)` |
| Set 'MESSAGE' [A match for regular expression <SEARCH_STRING> was detected in Changeset <CHANGESET>.]: | `Error! CREATE TABLE must include COMMENT ON TABLE for table description.` |
| Set 'STRIP_COMMENTS' (options: true, false) [true]: | `true` |
