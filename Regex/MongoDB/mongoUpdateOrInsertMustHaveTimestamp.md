# mongoUpdateOrInsertMustHaveTimestamp

`updateOne(), updateMany() or insertOne` statements must have a timestamp - use `new Date()`.

regex: `(?is)(?=.*\b(updateOne|updateMany|insertOne)\b)(?!.*\:\s+new\s+Date\(\)).*`

# Sample Failing Script
``` javascript
// changeset amalik:changeset-1 runWith:mongosh
db.collection.insertOne({
      name: "example"
    })
 ```

 # Sample Passing Script
``` javascript
// changeset amalik:changeset-2 runWith:mongosh
db.collection.insertOne({
      name: "example",
      createdAt: new Date()
    })

// changeset amalik:changeset-3 runWith:mongosh
db.collection.updateOne(
      { _id: ObjectId("someId") },
      { $set: { updatedAt: new Date() } }
    )
 ```

# Sample Error Message
```
CHANGELOG CHECKS
----------------
Checks completed validation of the changelog and found the following issues:

Check Name:         Check for specific patterns in sql (mongoUpdateOrInsertMustHaveTimestamp)
Changeset ID:       changeset-1
Changeset Filepath: mongosh.js
Check Severity:     CRITICAL (Return code: 3)
Message:            Error! updateOne, updateMany or insertOne statements must have a timestamp - use "new Date()".
```

# Step-by-Step
| Prompt | Command or User Input |
| ------ | ----------------------|
| > | `liquibase checks customize --check-name=SqlUserDefinedPatternCheck` |
| Give your check a short name for easier identification (up to 64 alpha-numeric characters only) [SqlUserDefinedPatternCheck1]: | `mongoUpdateOrInsertMustHaveTimestamp` |
| Set the Severity to return a code of 0-4 when triggered. (options: 'INFO'=0, 'MINOR'=1, 'MAJOR'=2, 'CRITICAL'=3, 'BLOCKER'=4)? [INFO]: | `<Choose a value: 0, 1, 2, 3, 4>` |
| Set 'SEARCH_STRING' (options: a string, or a valid regular expression): | `(?is)(?=.*\b(updateOne\|updateMany\|insertOne)\b)(?!.*\:\s+new\s+Date\(\)).*` |
| Set 'MESSAGE' [A match for regular expression <SEARCH_STRING> was detected in Changeset <CHANGESET>.]: | `Error! updateOne, updateMany or insertOne statements must have a timestamp - use "new Date()".` |
| Set 'STRIP_COMMENTS' (options: true, false) [true]: | `true` |
| Set 'PATH_FILTER_REGEX': | <empty> |
| Set 'SPLIT_STATEMENTS' to split multiple SQL statements on a delimiter, and evaluate each individually (options: true, false) [false]: | <empty> |

