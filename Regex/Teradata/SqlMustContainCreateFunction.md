# SqlMustContainCreateFunction

All changesets in the "3_function" folder must have CREATE (OR REPLACE) FUNCTION statement only.

regex: `(?is)^((?!(create\s*function|replace\s*function)).)*$`

# Sample Passing Script
``` sql
CREATE FUNCTION xml_extract( xml_text VARCHAR(64000))
    RETURNS TABLE (cust_id INTEGER,
                     store   INTEGER,
                     item    INTEGER)
    LANGUAGE C
    NO SQL
    EXTERNAL;
```

# Sample Error Message
```
CHANGELOG CHECKS
----------------
Checks completed validation of the changelog and found the following issues:

Check Name:         Check for specific patterns in sql (SqlMustContainCreateFunction)
Changeset ID:       create_function_xml_extract
Changeset Filepath: sql_code/3_function/create_function_xml_extract.sql
Check Severity:     MAJOR (Return code: 2)
Message:            All changesets in the "3_function" folder must have CREATE FUNCTION statement only.
```
# Step-by-Step

| Prompt | Command or User Input |
| ------ | ----------------------|
| > | `liquibase checks copy --check-name=SqlUserDefinedPatternCheck` |
| Give your check a short name for easier identification (up to 64 alpha-numeric characters only) [SqlUserDefinedPatternCheck1]: | `SqlMustContainCreateFunction` |
| Set the Severity to return a code of 0-4 when triggered. (options: 'INFO'=0, 'MINOR'=1, 'MAJOR'=2, 'CRITICAL'=3, 'BLOCKER'=4)? [INFO]: | `<Choose a value: 0, 1, 2, 3, 4>` |
| Set 'SEARCH_STRING' (options: a string, or a valid regular expression): | `(?is)^((?!(create\s*function\|replace\s*function)).)*$` |
| Set 'MESSAGE' [A match for regular expression <SEARCH_STRING> was detected in Changeset <CHANGESET>.]: | `All changesets in the "3_function" folder must have CREATE (OR REPLACE) FUNCTION statement only.` |
| Set 'STRIP_COMMENTS' (options: true, false) [true]: | `true` |
| Set 'PATH_FILTER_REGEX': | `.*/3_function\/.*` |
| Set 'SPLIT_STATEMENTS' to split multiple SQL statements on the delimiter, and evaluate each individually (options: true, false) [false]: | `true` |