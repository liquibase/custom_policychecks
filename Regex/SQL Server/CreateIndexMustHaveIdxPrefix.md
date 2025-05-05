# IndexMustHaveIdxPrefix

When using `CREATE INDEX`, the index names must be prefixed with `idx_`.

regex: `(?is)CREATE\s+INDEX\s+[\'\"]+(?!idx)`

# Sample Passing Script
``` sql
--changeset dev01:film_idx
CREATE UNIQUE INDEX IDX_Index ON #Test (C2)
  WITH (IGNORE_DUP_KEY = OFF);
```
# Sample Failing Scripts
``` sql
--changeset dev01:film_idx
CREATE UNIQUE INDEX AK_Index ON #Test (C2)
  WITH (IGNORE_DUP_KEY = OFF);
```

# Sample Error Message
```
CHANGELOG CHECKS
----------------
Checks completed validation of the changelog and found the following issues:

Check Name:         Pattern a not followed by pattern b (IndexMustHaveIdxPrefix)
Changeset ID:       index_prefix_test_fail
Changeset Filepath: sqlcode/1.0/schema1/changelog.yaml :: index_prefix_test_fail.sql
Check Severity:     INFO (Return code: 0)
Message:            Index names must be prefixed with idx_ in Changeset index_prefix_test_fail.
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

