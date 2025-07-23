# SqlMustContainCreateTrigger

All changesets in the "7_trigger" folder must have CREATE (OR ALTER OR REPLACE) TRIGGER statement only.

regex: `(?is)^((?!(create\s*trigger|replace\s*trigger|alter\s*trigger)).)*$`

# Sample Passing Script
``` sql
     CREATE TRIGGER set_trig
       BEFORE INSERT ON subject_table 
       REFERENCING NEW AS curr_value 
       FOR EACH ROW 
       SET curr_value.entry_date = DATE;
```

# Sample Error Message
```
CHANGELOG CHECKS
----------------
Checks completed validation of the changelog and found the following issues:

Check Name:         Check for specific patterns in sql (SqlMustContainCreateTrigger)
Changeset ID:       create_trigger
Changeset Filepath: sql_code/7_trigger/create_trigger.sql
Check Severity:     MAJOR (Return code: 2)
Message:            All changesets in the "7_trigger" folder must have CREATE TRIGGER statement only.
```
# Step-by-Step

| Prompt | Command or User Input |
| ------ | ----------------------|
| > | `liquibase checks copy --check-name=SqlUserDefinedPatternCheck` |
| Give your check a short name for easier identification (up to 64 alpha-numeric characters only) [SqlUserDefinedPatternCheck1]: | `SqlMustContainCreateTrigger` |
| Set the Severity to return a code of 0-4 when triggered. (options: 'INFO'=0, 'MINOR'=1, 'MAJOR'=2, 'CRITICAL'=3, 'BLOCKER'=4)? [INFO]: | `<Choose a value: 0, 1, 2, 3, 4>` |
| Set 'SEARCH_STRING' (options: a string, or a valid regular expression): | `(?is)^((?!(create\s*trigger\|replace\s*trigger\|alter\s*trigger)).)*$` |
| Set 'MESSAGE' [A match for regular expression <SEARCH_STRING> was detected in Changeset <CHANGESET>.]: | `All changesets in the "7_trigger" folder must have CREATE (OR ALTER OR REPLACE) TRIGGER statement only.` |
| Set 'STRIP_COMMENTS' (options: true, false) [true]: | `true` |
| Set 'PATH_FILTER_REGEX': | `.*/7_trigger\/.*` |
| Set 'SPLIT_STATEMENTS' to split multiple SQL statements on the delimiter, and evaluate each individually (options: true, false) [false]: | `true` |