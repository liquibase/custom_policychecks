# mongoCrIndexNameStdChk

Every `db.<collection>.createIndex` call should name the index starting with 'IDX' this is a suggested nameing standard but can be tailored to look for any string that fits the naming standard

regex: `(?i)(?s)createIndex(?!.*IDX-)`

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
                      "mongo": "db.students.dropIndex( \"ID-students-uniquename\")"
                    }
                  }
              ]
          }    
      }
--create-idxname-students-fails.js contents
-- current bug in core is not finding QCs violation when this is embedded in JSON changelog so
--it is defined in separate file that contains what is passed to mongosh
db.students.createIndex({
    "name": "text"
},
{
    name: "ID-students-uniquename",
    unique: true
});

```
# Sample Error Message
```
CHANGELOG CHECKS
----------------
Checks completed validation of the changelog and found the following issues:

Check Name:         Check for specific patterns in sql (mongoCrIndexNameStdChk)
Changeset ID:       create_students-name-index
Changeset Filepath: dbchangelog.json
Check Severity:     MINOR (Return code: 1)
Message:            The createIndex you are running in Mongo does not meet
                    naming standards
```

# Step-by-Step
| Prompt | Command or User Input |
| ------ | ----------------------|
| > | `liquibase checks customize --check-name=SqlUserDefinedPatternCheck` |
| Give your check a short name for easier identification (up to 64 alpha-numeric characters only) [SqlUserDefinedPatternCheck1]: | `mongoCrIndexNameStdChk` |
| Set the Severity to return a code of 0-4 when triggered. (options: 'INFO'=0, 'MINOR'=1, 'MAJOR'=2, 'CRITICAL'=3, 'BLOCKER'=4)? [INFO]: | `<Choose a value: 0, 1, 2, 3, 4>` |
| Set 'SEARCH_STRING' (options: a string, or a valid regular expression): | `(?i)(?s)createIndex(?!.*IDX-)` |
| Set 'MESSAGE' [A match for regular expression <SEARCH_STRING> was detected in Changeset <CHANGESET>.]: |  `The createIndex you are running in Mongo does not meet naming standards` |
| Set 'STRIP_COMMENTS' (options: true, false) [true]: | `true` |
