# TableNamesCannotBeMoreThan26Characters

Table names cannot be more than 26 characters.

regex: `(?is)create\s*table\s*\w+\.[A-Za-z0-9_]{27,}`

# Sample Passing Scripts
``` sql
--changeset asmith:create_table_01
CREATE TABLE DB2T001.TEST_TABLE_01 (
	FIRSTNAME VARCHAR(50),
	LASTNAME VARCHAR(50)
);
```

# Sample Failing Scripts
``` sql
--changeset asmith:create_table_with_long_tablename
CREATE TABLE DB2T001.THIS_TABLE_NAME_IS_27_CHARS (
	FIRSTNAME VARCHAR(50),
	LASTNAME VARCHAR(50)
);
```

# Sample Error Message
``` 
CHANGELOG CHECKS
----------------
Checks completed validation of the changelog and found the following issues:

Check Name:         Check for specific patterns in sql (TableNamesCannotBeMoreThan26Characters)
Changeset ID:       create_table_with_long_tablename
Changeset Filepath: sql_code/Scripts/TABLES_01.sql
Check Severity:     BLOCKER (Return code: 4)
Message:            Error! Table names cannot be more than 26 characters.
```

# Step-by-Step
| Prompt | Command or User Input |
| ------ | ----------------------|
| > | `liquibase checks customize --check-name=SqlUserDefinedPatternCheck` |
| Give your check a short name for easier identification (up to 64 alpha-numeric characters only) [SqlUserDefinedPatternCheck1]: | `TableNamesCannotBeMoreThan26Characters` |
| Set the Severity to return a code of 0-4 when triggered. (options: 'INFO'=0, 'MINOR'=1, 'MAJOR'=2, 'CRITICAL'=3, 'BLOCKER'=4)? [INFO]: | `<Choose a value: 0, 1, 2, 3, 4>` |
| Set 'SEARCH_STRING' (options: a string, or a valid regular expression): | `(?is)create\s*table\s*\w+\.[A-Za-z0-9_]{27,}` |
| Set 'MESSAGE' [A match for regular expression <SEARCH_STRING> was detected in Changeset <CHANGESET>.]: | `Error! Table names cannot be more than 26 characters.` |
| Set 'STRIP_COMMENTS' (options: true, false) [true]: | `true` |
