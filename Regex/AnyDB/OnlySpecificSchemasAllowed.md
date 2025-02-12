# OnlySpecificSchemasAllowed

Only specific schemas are allowed, e.g., `lion` and `eagle`

PATTERN_A regex: `(?is)(?=create|drop|alter|insert|select|delete)`

PATTERN_B regex: `(?is)(?:lion|eagle)\.`

# Sample Passing Scripts
```sql
CREATE TABLE CMS_DEV.eagle.table1 (val1 number, val2 date);
```
```sql
--changeset amalik:2
CREATE TABLE CMS_DEV.lion.table2 (val1 number, val2 date);
```

# Sample Failing Scripts
``` sql
CREATE TABLE CMS_DEV.myschema.table1 (val1 number, val2 date);
```

# Sample Error Message
```
CHANGELOG CHECKS
----------------
Checks completed validation of the changelog and found the following issues:

Check Name:         Pattern a not followed by pattern b (OnlySpecificSchemasAllowed)
Changeset ID:       3
Changeset Filepath: Changelogs/adeel1.sql
Check Severity:     BLOCKER (Return code: 4)
Message:            Error! Only "lion" and "eagle" schemas are allowed in this database.
```
# Step-by-Step

| Prompt | Command or User Input |
| ------ | ----------------------|
| > | `liquibase checks customize --check-name=PatternANotFollowedByPatternB` |
| Give your check a short name for easier identification (up to 64 alpha-numeric characters only) [PatternANotFollowedByPatternB1]: | `OnlySpecificSchemasAllowed` |
| Set the Severity to return a code of 0-4 when triggered. (options: 'INFO'=0, 'MINOR'=1, 'MAJOR'=2, 'CRITICAL'=3, 'BLOCKER'=4)? [INFO]: | `<Choose a value: 0, 1, 2, 3, 4>` |
| Set 'PATTERN_A' (options: a string, or a valid regular expression): | `(?is)(?=create\|drop\|alter\|insert\|select\|delete)` |
| Set 'PATTERN_B' (options: a string, or a valid regular expression): | `(?is)(?:lion\|eagle)\.`
| Set 'CASE_SENSITIVE' (options: true, false) [true]: | `false`
| Set 'MESSAGE' [A match for regular expression <SEARCH_STRING> was detected in Changeset <CHANGESET>.]: | `Error! Only "lion" and "eagle" schemas are allowed in this database.` |
| Set 'STRIP_COMMENTS' (options: true, false) [true]: | `true` |

