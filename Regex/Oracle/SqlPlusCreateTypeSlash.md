# SqlPlusCreateTypeSlash

For SqlPlus changesets, CREATE TYPE statements must be following by a terminating '/' character.

regex: `(?is)\bCREATE\s+TYPE\b[\s\S]*?;(?!\s*\r?\n\s*\/)`

# Sample Passing Script
``` sql
--changeset asmith:create_type
CREATE TYPE my_object_type AS OBJECT (
   id        NUMBER,
   name      VARCHAR2(100),
   created_dtm DATE
);
/
```
# Sample Failing Scripts
``` sql
--changeset asmith:create_type_without_slash
CREATE TYPE my_object_type AS OBJECT (
   id        NUMBER,
   name      VARCHAR2(100),
   created_dtm DATE
);
```

# Sample Error Message
```
CHANGELOG CHECKS
----------------
Checks completed validation of the changelog and found the following issues:

Check Name:         Check for specific patterns in sql (SqlPlusCreateTypeSlash)
Changeset ID:       create_type
Changeset Filepath: script1.sql
Check Severity:     MAJOR (Return code: 2)
Message:            For SqlPlus changesets, CREATE TYPE statements must be following by a terminating '/' character.
```

# Step-by-Step
| Prompt | Command or User Input |
| ------ | ----------------------|
| > | `liquibase checks customize --check-name=SqlUserDefinedPatternCheck` |
| Give your check a short name for easier identification (up to 64 alpha-numeric characters only) [SqlUserDefinedPatternCheck1]: | `SqlPlusCreateTypeSlash` |
| Set the Severity to return a code of 0-4 when triggered. (options: 'INFO'=0, 'MINOR'=1, 'MAJOR'=2, 'CRITICAL'=3, 'BLOCKER'=4)? [INFO]: | `<Choose a value: 0, 1, 2, 3, 4>` |
| Set 'SEARCH_STRING' (options: a string, or a valid regular expression): | `(?is)\bCREATE\s+TYPE\b[\s\S]*?;(?!\s*\r?\n\s*\/)` |
| Set 'MESSAGE' [A match for regular expression <SEARCH_STRING> was detected in Changeset <CHANGESET>.]: | `For SqlPlus changesets, CREATE TYPE statements must be following by a terminating "/" character.` |
| Set 'STRIP_COMMENTS' (options: true, false) [true]: | `true` |
| Set 'PATH_FILTER_REGEX': | _leave blank_ |
| Set 'SPLIT_STATEMENTS' to split multiple SQL statements on the delimiter, and evaluate each individually (options: true, false) [false]: | false |
