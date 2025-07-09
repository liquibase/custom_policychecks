# DoNotUseChar2Types

Error when column type is specified as char2, char4, char8, or char16.

regex: `(?i)\bchar(?:2|4|8|16)\b`

# Sample Failing Scripts
``` sql
CREATE TABLE new_table (
    id serial PRIMARY KEY,
    name char16[16]
);
```

# Sample Error Message
```
CHANGELOG CHECKS
----------------
Checks completed validation of the changelog and found the following issues:

Check Name:         Check for specific patterns in sql (DoNotUseChar2Types)
Changeset ID:       new_table
Changeset Filepath: changeLogs/tables/new_table.sql
Check Severity:     INFO (Return code: 4)
Message:            Do not use internal types char2, char4, char8, or char16 for DDL.
```
# Step-by-Step

| Prompt | Command or User Input |
| ------ | ----------------------|
| > | `liquibase checks customize --check-name=SqlUserDefinedPatternCheck` |
| Give your check a short name for easier identification (up to 64 alpha-numeric characters only) [SqlUserDefinedPatternCheck1]: | `DoNotUseChar2Types` |
| Set the Severity to return a code of 0-4 when triggered. (options: 'INFO'=0, 'MINOR'=1, 'MAJOR'=2, 'CRITICAL'=3, 'BLOCKER'=4)? [INFO]: | `<Choose a value: 0, 1, 2, 3, 4>` |
| Set 'SEARCH_STRING' (options: a string, or a valid regular expression): | `(?i)\bchar(?:2\|4\|8\|16)\b` |
| Set 'MESSAGE' [A match for regular expression <SEARCH_STRING> was detected in Changeset <CHANGESET>.]: | `Do not use internal types char2, char4, char8, or char16 for DDL.` |
| Set 'STRIP_COMMENTS' (options: true, false) [true]: | `true` |

