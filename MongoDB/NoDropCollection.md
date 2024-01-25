# NoDropCollection

No `drop()` statements allowed.

regex: `(?i:drop)`

# Sample Failing Scripts
``` javascript
db.restaurant.drop();
 ```

# Sample Error Message
```
CHANGELOG CHECKS
----------------
Checks completed validation of the changelog and found the following issues:

Check Name:         Check for specific patterns in sql (NoDropCollection)
Changeset ID:       drop_restaurant
Changeset Filepath: DBScripts/MongoDB/mongochangelog.js
Check Severity:     BLOCKER (Return code: 4)
Message:            Error! DROP COLLECTION not allowed.
```

# Step-by-Step
| Prompt | Command or User Input |
| ------ | ----------------------|
| > | `liquibase checks customize --check-name=SqlUserDefinedPatternCheck` |
| Give your check a short name for easier identification (up to 64 alpha-numeric characters only) [SqlUserDefinedPatternCheck1]: | `NoDropCollection` |
| Set the Severity to return a code of 0-4 when triggered. (options: 'INFO'=0, 'MINOR'=1, 'MAJOR'=2, 'CRITICAL'=3, 'BLOCKER'=4)? [INFO]: | `<Choose a value: 0, 1, 2, 3, 4>` |
| Set 'SEARCH_STRING' (options: a string, or a valid regular expression): | `(?i:drop)` |
| Set 'MESSAGE' [A match for regular expression <SEARCH_STRING> was detected in Changeset <CHANGESET>.]: | `Error! DROP COLLECTION not allowed.` |
| Set 'STRIP_COMMENTS' (options: true, false) [true]: | `true` |

