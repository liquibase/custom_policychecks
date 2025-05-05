# WarnOnDropIndex

`DROP INDEX` not allowed.

regex: `(?is)DROP\s*INDEX`

# Sample Passing Script
``` sql
--changeset dev01:drop_index_test_pass
DROP TABLE INDEX;
 ```
# Sample Failing Script
``` sql
--changeset dev01:drop_index_test_fail
DROP INDEX IX_ProductVendor_BusinessEntityID
    ON Purchasing.ProductVendor;
```

# Sample Error Message
``` 
CHANGELOG CHECKS
----------------
Checks completed validation of the changelog and found the following issues:

Check Name:         Check for specific patterns in sql (WarnOnDropIndex)
Changeset ID:       drop_index_test_fail
Changeset Filepath: sqlcode/1.0/schema1/changelog.yaml :: drop_index_test_fail.sql: Line 1
Match:              DROP INDEX IX_ProductVendor_BusinessEntityID
Check Severity:     INFO (Return code: 0)
Message:            WARNING: Index dropped in Changeset drop_index_test_fail.
```

# Step-by-Step
| Prompt | Command or User Input |
| ------ | ----------------------|
| > | `liquibase checks customize --check-name=SqlUserDefinedPatternCheck` |
| Give your check a short name for easier identification (up to 64 alpha-numeric characters only) [SqlUserDefinedPatternCheck1]: | `WarnOnDropIndex` |
| Set the Severity to return a code of 0-4 when triggered. (options: 'INFO'=0, 'MINOR'=1, 'MAJOR'=2, 'CRITICAL'=3, 'BLOCKER'=4)? [INFO]: | `<Choose a value: 0, 1, 2, 3, 4>` |
| Set 'SEARCH_STRING' (options: a string, or a valid regular expression): | `(?is)DROP\s*INDEX` |
| Set 'MESSAGE' [A match for regular expression <SEARCH_STRING> was detected in Changeset <CHANGESET>.]: | `WARNING: Index dropped in Changeset <CHANGESET>.` |
| Set 'STRIP_COMMENTS' (options: true, false) [true]: | `true` |
| Set 'PATH_FILTER_REGEX': |  |
| Set 'STRIP_COMMENTS' (options: true, false) [true]: | `true` |
