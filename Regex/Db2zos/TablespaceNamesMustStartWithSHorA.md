# TablespaceNamesMustStartWithSHorA

TABLESPACE NAMES must start with S, H, or A and have 8 chars or less.


regex: `(?is)create\s+tablespace\s+(?![sha])[A-Za-z0-9_]{1,8}\b|create\s+tablespace\s+\w{9,}`

# Sample Passing Scripts
``` sql
--changeset asmith:create_database_01
  CREATE TABLESPACE SCH10001
    IN DBA0001
    USING STOGROUP SYSPOOL1;
```

# Sample Failing Scripts
``` sql
--changeset asmith:create_tablespace_with_incorrect_name
  CREATE TABLESPACE GCH10001
    IN DBA0001
    USING STOGROUP SYSPOOL1;
```

# Sample Error Message
``` 
CHANGELOG CHECKS
----------------
Checks completed validation of the changelog and found the following issues:

Check Name:         Check for specific patterns in sql (TablespaceNamesMustStartWithSHorA)
Changeset ID:       create_tablespace_with_incorrect_name
Changeset Filepath: sql_code/Scripts/TABLESPACES.sql
Check Severity:     BLOCKER (Return code: 4)
Message:            Error! TABLESPACE NAMES must start with S, H, or A and have 8 chars or less.
```

# Step-by-Step
| Prompt | Command or User Input |
| ------ | ----------------------|
| > | `liquibase checks customize --check-name=SqlUserDefinedPatternCheck` |
| Give your check a short name for easier identification (up to 64 alpha-numeric characters only) [SqlUserDefinedPatternCheck1]: | `TablespaceNamesMustStartWithSHorA` |
| Set the Severity to return a code of 0-4 when triggered. (options: 'INFO'=0, 'MINOR'=1, 'MAJOR'=2, 'CRITICAL'=3, 'BLOCKER'=4)? [INFO]: | `<Choose a value: 0, 1, 2, 3, 4>` |
| Set 'SEARCH_STRING' (options: a string, or a valid regular expression): | `(?is)create\s+tablespace\s+(?![sha])[A-Za-z0-9_]{1,8}\b|create\s+tablespace\s+\w{9,}` |
| Set 'MESSAGE' [A match for regular expression <SEARCH_STRING> was detected in Changeset <CHANGESET>.]: | `Error! TABLESPACE NAMES must start with S, H, or A and have 8 chars or less.` |
| Set 'STRIP_COMMENTS' (options: true, false) [true]: | `true` |
