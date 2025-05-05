# IndexMustHaveIdxPrefix

When using `CREATE INDEX`, the index names must be prefixed with `idx_`.

regex: `(?is)CREATE\s+INDEX\s+[\'\"]+(?!idx)`

# Sample Passing Script
``` sql
--changeset dev01:film_idx
CREATE INDEX 'idx_film_fulltext_idx' 
  ON "film"("fulltext");
```
# Sample Failing Scripts
``` sql
--changeset dev01:film_idx
CREATE INDEX 'index_film_fulltext_idx' 
  ON "film"("fulltext");
```

# Sample Error Message
```
CHANGELOG CHECKS
----------------
Checks completed validation of the changelog and found the following issues:

Check Name:         Check for specific patterns in sql (CreateTableMustHavePrimaryKey)
Changeset ID:       sales2
Changeset Filepath: changeLogs/1_tables/01_createTable1.sql
Check Severity:     INFO (Return code: 4)
Message:            Error! CREATE TABLE statement must have a primary key
                    included.
```

# Step-by-Step
| Prompt                                                                                                                                         | Command or User Input                                                                                        |
|------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------|
| >                                                                                                                                              | `liquibase checks customize --check-name=liquibase checks customize --check-name=PatternANotFollowedByPatternB` |
| Give your check a short name for easier identification (up to 64 alpha-numeric characters only) [--check-name=PatternANotFollowedByPatternB1]: | `IndexMustHaveIdxPrefix`                                                                                     |
| Set the Severity to return a code of 0-4 when triggered. (options: 'INFO'=0, 'MINOR'=1, 'MAJOR'=2, 'CRITICAL'=3, 'BLOCKER'=4)? [INFO]:         | `<Choose a value: 0, 1, 2, 3, 4>`                                                                            |
| Set 'PATTERN_A' (options: a string, or a valid regular expression):                                                                            | `(?is)CREATE\s+(?:NONCLUSTERED\|UNIQUE\|)?\s*INDEX\s*['\"]*`                                                                            |
| Set 'PATTERN_B' (options: a string, or a valid regular expression):                                                                            | `idx_`|
| Set 'CASE_SENSITIVE' (options: true, false) [true]:                                                                                            | `false`|
| Set 'MESSAGE' [A match for regular expression <SEARCH_STRING> was detected in Changeset <CHANGESET>.]:                                         | `Index names must be prefixed with idx_ in Changeset <CHANGESET>.`                                           |
| Set 'STRIP_COMMENTS' (options: true, false) [true]:                                                                                            | `true` |        

