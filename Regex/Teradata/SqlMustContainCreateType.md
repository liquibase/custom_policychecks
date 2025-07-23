# SqlMustContainCreateType

All changesets in the named folder must have CREATE TYPE statement only. For the example, the named folder is "0_type".

regex: `(?is)^((?!create\s*type).)*$`

# Sample Passing Script
``` sql
CREATE TYPE euro 
    AS DECIMAL(8, 2) 
    FINAL
    METHOD toUS()
    RETURNS us_dollar CAST FROM DECIMAL(8,2)
    LANGUAGE C
    DETERMINISTIC
    NO SQL
    RETURNS NULL ON NULL INPUT;
```

# Sample Error Message
```
CHANGELOG CHECKS
----------------
Checks completed validation of the changelog and found the following issues:

Check Name:         Check for specific patterns in sql (SqlMustContainCreateType)
Changeset ID:       create_type_euro
Changeset Filepath: sql_code/0_type/create_type_euro.sql
Check Severity:     MAJOR (Return code: 2)
Message:            All changesets in the "0_type" folder must have CREATE TYPE statement only.
```
# Step-by-Step

| Prompt | Command or User Input |
| ------ | ----------------------|
| > | `liquibase checks copy --check-name=SqlUserDefinedPatternCheck` |
| Give your check a short name for easier identification (up to 64 alpha-numeric characters only) [SqlUserDefinedPatternCheck1]: | `SqlMustContainCreateType` |
| Set the Severity to return a code of 0-4 when triggered. (options: 'INFO'=0, 'MINOR'=1, 'MAJOR'=2, 'CRITICAL'=3, 'BLOCKER'=4)? [INFO]: | `<Choose a value: 0, 1, 2, 3, 4>` |
| Set 'SEARCH_STRING' (options: a string, or a valid regular expression): | `(?is)^((?!create\s*type).)*$` |
| Set 'MESSAGE' [A match for regular expression <SEARCH_STRING> was detected in Changeset <CHANGESET>.]: | `All changesets in the "0_type" folder must have CREATE TYPE statement only.` |
| Set 'STRIP_COMMENTS' (options: true, false) [true]: | `true` |
| Set 'PATH_FILTER_REGEX': | `.*/0_type\/.*` |
| Set 'SPLIT_STATEMENTS' to split multiple SQL statements on the delimiter, and evaluate each individually (options: true, false) [false]: | `true` |
