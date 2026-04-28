# DoNotUseReltime

Error when column type is timespan data type.

regex: `(?is)\b(CREATE\s+TABLE|ALTER\s+TABLE)\b.*?\bTIMESPAN\b`

# Sample Failing Scripts
``` sql
CREATE TABLE legacy_table (
    id serial PRIMARY KEY,
    duration timespan
);
```
``` sql
ALTER TABLE my_table ADD COLUMN duration timespan;
```

# Sample Error Message
```
CHANGELOG CHECKS
----------------
Checks completed validation of the changelog and found the following issues:

Check Name:         Check for specific patterns in sql (DoNotUseTimespan)
Changeset ID:       legacy_table
Changeset Filepath: changeLogs/tables/legacy_table.sql
Check Severity:     INFO (Return code: 4)
Message:            Do not use invalid column type TIMESPAN.
```
# Step-by-Step

| Prompt | Command or User Input |
| ------ | ----------------------|
| > | `liquibase checks customize --check-name=SqlUserDefinedPatternCheck` |
| Give your check a short name for easier identification (up to 64 alpha-numeric characters only) [SqlUserDefinedPatternCheck1]: | `DoNotUseTimespan` |
| Set the Severity to return a code of 0-4 when triggered. (options: 'INFO'=0, 'MINOR'=1, 'MAJOR'=2, 'CRITICAL'=3, 'BLOCKER'=4)? [INFO]: | `<Choose a value: 0, 1, 2, 3, 4>` |
| Set 'SEARCH_STRING' (options: a string, or a valid regular expression): | `(?is)\b(CREATE\s+TABLE\|ALTER\s+TABLE)\b.*?\bTIMESPAN\b` |
| Set 'MESSAGE' [A match for regular expression <SEARCH_STRING> was detected in Changeset <CHANGESET>.]: | `Do not use invalid column type TIMESPAN.` |
| Set 'STRIP_COMMENTS' (options: true, false) [true]: | `true` |

