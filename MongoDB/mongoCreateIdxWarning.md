# mongoCreateIdxWarning

Every `db.<collection>.createIndex` Warning that mongosh change inculdes a create index statement

regex: `(?i)(?s)createIndex`

# Sample Passing Script
``` mongosh 
          "changeSet": {
              "id": "create_students-name-index",
              "author": "jennl",
              "labels": "[jira-101],'version 1.0'",
              "runWith": "mongosh",
              "changes": [
                {
                  "mongoFile": {
                    "dbms": "mongodb",
                    "path": "create-idxname-students.js",
                    "relativeToChangelogFile": true
                  }
                }
                ],       
              "rollback": [
                  {
                    "mongo": {
                      "mongo": "db.students.dropIndex( \"IDX-students-uniquename\")"
                    }
                  }
              ]
          }    
      }
--create-idxname-students.js contents
-- current bug in core is not finding QCs violation when this is embedded in JSON changelog so
--it is defined in separate file that contains what is passed to mongosh
db.students.createIndex({
    "name": "text"
},
{
    name: "IDX-students-uniquename",
    unique: true
});

```
# Sample Failing Scripts

--create-collection-students-fails.js contents
-- current bug in core is not finding QCs violation when this is embedded in JSON changelog so
--it is defined in separate file that contains what is passed to mongosh
--The string 'createIndex' would not be present in the javascript file anywhere

```
# Sample Error Message
```
CHANGELOG CHECKS
----------------
Checks completed validation of the changelog and found the following issues:

Check Name:         Check for specific patterns in sql (mongoCreateIdxWarning)
Changeset ID:       create_students-name-index
Changeset Filepath: dbchangelog.json
Check Severity:     INFO (Return code: 0)
Message:            There is a Mongo create Index statement in your changelog
```

# Step-by-Step
| Prompt | Command or User Input |
| ------ | ----------------------|
| > | `liquibase checks customize --check-name=SqlUserDefinedPatternCheck` |
| Give your check a short name for easier identification (up to 64 alpha-numeric characters only) [SqlUserDefinedPatternCheck1]: | `mongoCreateIdxWarning` |
| Set the Severity to return a code of 0-4 when triggered. (options: 'INFO'=0, 'MINOR'=1, 'MAJOR'=2, 'CRITICAL'=3, 'BLOCKER'=4)? [INFO]: | `<Choose a value: 0, 1, 2, 3, 4>` |
| Set 'SEARCH_STRING' (options: a string, or a valid regular expression): | `((?i)(?s)createIndex)` |
| Set 'MESSAGE' [A match for regular expression <SEARCH_STRING> was detected in Changeset <CHANGESET>.]: | ` There is a Mongo create Index statement in your changelog` |
| Set 'STRIP_COMMENTS' (options: true, false) [true]: | `true` |
