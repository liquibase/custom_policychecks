# DatabaseNamesMustStartWithDAorC

DATABASE NAMES must start with D, A, or C.

regex: `(?is)create\s+database\s+(?![dac])[A-Za-z0-9_]+\s+`

# Sample Passing Scripts
``` sql
--changeset asmith:create_database_01
  CREATE DATABASE DBA0001
    BUFFERPOOL BP1
    INDEXBP    BP1
    CCSID      EBCDIC
    STOGROUP   SYSPOOL1;
```

# Sample Failing Scripts
``` sql
--changeset asmith:create_database_with_incorrect_db_name
  CREATE DATABASE GGG0001
    BUFFERPOOL BP1
    INDEXBP    BP1
    CCSID      EBCDIC
    STOGROUP   SYSPOOL1;
```

# Sample Error Message
``` 
CHANGELOG CHECKS
----------------
Checks completed validation of the changelog and found the following issues:

Check Name:         Check for specific patterns in sql (DatabaseNamesMustStartWithDAorC)
Changeset ID:       create_database_with_incorrect_db_name
Changeset Filepath: sql_code/Scripts/DATABASES.sql
Check Severity:     BLOCKER (Return code: 4)
Message:            Error! DATABASE NAMES must start with D, A, or C.
```

# Step-by-Step
| Prompt | Command or User Input |
| ------ | ----------------------|
| > | `liquibase checks customize --check-name=SqlUserDefinedPatternCheck` |
| Give your check a short name for easier identification (up to 64 alpha-numeric characters only) [SqlUserDefinedPatternCheck1]: | `DatabaseNamesMustStartWithDAorC` |
| Set the Severity to return a code of 0-4 when triggered. (options: 'INFO'=0, 'MINOR'=1, 'MAJOR'=2, 'CRITICAL'=3, 'BLOCKER'=4)? [INFO]: | `<Choose a value: 0, 1, 2, 3, 4>` |
| Set 'SEARCH_STRING' (options: a string, or a valid regular expression): | `(?is)create\s+database\s+(?![dac])[A-Za-z0-9_]+\s+` |
| Set 'MESSAGE' [A match for regular expression <SEARCH_STRING> was detected in Changeset <CHANGESET>.]: | `Error! DATABASE NAMES must start with D, A, or C.` |
| Set 'STRIP_COMMENTS' (options: true, false) [true]: | `true` |
