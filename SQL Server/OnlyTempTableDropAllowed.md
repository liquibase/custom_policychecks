# OnlyTempTableDropAllowed

`DROP TABLE` statements only allowed when dropping temporary tables.

regex: `(?i:drop)[\t\r\n\s]+(?i:table)[\t\r\n\s]+[^#]+\s`

# Sample Passing Scripts
``` sql
--changeset amalik:drop_temp_sales
DROP TABLE #sales;

--changeset amalik:drop_temp_dbo.sales
DROP TABLE dbo.#sales;
```

# Sample Failing Scripts
``` sql
--changeset amalik:drop_sales
DROP TABLE sales;

--changeset amalik:drop_dbo.sales
DROP TABLE dbo.sales;
```

# Sample Error Message
```
CHANGELOG CHECKS
----------------
Checks completed validation of the changelog and found the following issues:

Check Name:         Check for specific patterns in sql (OnlyTempTableDropAllowed)
Changeset ID:       DB-1011
Changeset Filepath: changelog.xml
Check Severity:     BLOCKER (Return code: 4)
Message:            ERROR! Drop tables not allowed. Only allowed to drop temporary tables.
```

# Step-by-Step
| Prompt | Command or User Input |
| ------ | ----------------------|
| > | `liquibase checks customize --check-name=SqlUserDefinedPatternCheck` |
| Give your check a short name for easier identification (up to 64 alpha-numeric characters only) [SqlUserDefinedPatternCheck1]: | `OnlyTempTableDropAllowed` |
| Set the Severity to return a code of 0-4 when triggered. (options: 'INFO'=0, 'MINOR'=1, 'MAJOR'=2, 'CRITICAL'=3, 'BLOCKER'=4)? [INFO]: | `<Choose a value: 0, 1, 2, 3, 4>` |
| Set 'SEARCH_STRING' (options: a string, or a valid regular expression): | `(?i:drop)[\t\r\n\s]+(?i:table)[\t\r\n\s]+[^#]+\s` |
| Set 'MESSAGE' [A match for regular expression <SEARCH_STRING> was detected in Changeset <CHANGESET>.]: | `ERROR! Drop tables not allowed. Only allowed to drop temporary tables.` |
| Set 'STRIP_COMMENTS' (options: true, false) [true]: | `true` |
