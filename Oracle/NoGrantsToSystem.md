# NoGrantsToSystem

Do not allow `GRANT <Privilege Type> TO SYSTEM` statements.

regex: `(?i:grant)[\t\n\r\s\S]*(?i:to system)`

# Sample Failing Scripts
```
GRANT EXECUTE TO SYSTEM;
```
```
GRANT SELECT ON TABLE sales TO SYSTEM;
```
```
GRANT UPDATE, TRIGGER ON TABLE sales TO SYSTEM;
```

# Sample Error Message
```
CHANGELOG CHECKS
----------------
Checks completed validation of the changelog and found the following issues:

Check Name:         Check for specific patterns in sql (NoGrantsToSystem)
Changeset ID:       grant_execute
Changeset Filepath: changeLogs/1_tables/03_grants.sql
Check Severity:     BLOCKER (Return code: 4)
Message:            Error! GRANT to SYSTEM not allowed.
```
# Step-by-Step

| Prompt | Command or User Input |
| ------ | ----------------------|
| > | `liquibase checks customize --check-name=SqlUserDefinedPatternCheck` |
| Give your check a short name for easier identification (up to 64 alpha-numeric characters only) [SqlUserDefinedPatternCheck1]: | `NoGrantsToSystem` |
| Set the Severity to return a code of 0-4 when triggered. (options: 'INFO'=0, 'MINOR'=1, 'MAJOR'=2, 'CRITICAL'=3, 'BLOCKER'=4)? [INFO]: | `<Choose a value: 0, 1, 2, 3, 4>` |
| Set 'SEARCH_STRING' (options: a string, or a valid regular expression): | `(?i:grant)[\t\n\r\s\S]*(?i:to system)` |
| Set 'MESSAGE' [A match for regular expression <SEARCH_STRING> was detected in Changeset <CHANGESET>.]: | `Error! GRANT to SYSTEM not allowed.` |
| Set 'STRIP_COMMENTS' (options: true, false) [true]: | `true` |

