# SqlPlusBeginEndSlash

For SqlPlus changesets, BEGIN and END; statements must be followed by a terminating '/' character.

regex: `(?is)\bBEGIN\b[\s\S]*?\bEND;(?!\s*\r?\n\s*\/)`

# Sample Passing Script
``` sql
--changeset asmith:hello_world
CREATE OR REPLACE PROCEDURE hello_world_proc
AS
BEGIN
   DBMS_OUTPUT.PUT_LINE('Hello, world');
END;
/
```
# Sample Failing Script
``` sql
--changeset asmith:hello_world_without_slash
CREATE OR REPLACE PROCEDURE hello_world_proc
AS
BEGIN
   DBMS_OUTPUT.PUT_LINE('Hello, world');
END;
```

# Sample Error Message
```text
CHANGELOG CHECKS
----------------
Checks completed validation of the changelog and found the following issues:

Check Name:         Check for specific patterns in sql (SqlPlusBeginEndSlash)
Changeset ID:       hello_world
Changeset Filepath: script1.sql
Check Severity:     MAJOR (Return code: 2)
Message:            For SqlPlus changesets, BEGIN and END; statements must be followed by a terminating "/" character.
```

# Step-by-Step
| Prompt | Command or User Input |
| ------ | ----------------------|
| > | `liquibase checks customize --check-name=SqlUserDefinedPatternCheck` |
| Give your check a short name for easier identification (up to 64 alpha-numeric characters only) [SqlUserDefinedPatternCheck1]: | `SqlPlusBeginEndSlash` |
| Set the Severity to return a code of 0-4 when triggered. (options: 'INFO'=0, 'MINOR'=1, 'MAJOR'=2, 'CRITICAL'=3, 'BLOCKER'=4)? [INFO]: | `<Choose a value: 0, 1, 2, 3, 4>` |
| Set 'SEARCH_STRING' (options: a string, or a valid regular expression): | `(?is)\bBEGIN\b[\s\S]*?\bEND;(?!\s*\r?\n\s*\/)` |
| Set 'MESSAGE' [A match for regular expression <SEARCH_STRING> was detected in Changeset <CHANGESET>.]: | `For SqlPlus changesets, BEGIN and END; statements must be followed by a terminating "/" character.` |
| Set 'STRIP_COMMENTS' (options: true, false) [true]: | `true` |
| Set 'PATH_FILTER_REGEX': | _leave blank_ |
| Set 'SPLIT_STATEMENTS' to split multiple SQL statements on the delimiter, and evaluate each individually (options: true, false) [false]: | false |
