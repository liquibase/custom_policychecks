# mongoCrCollectionValidatorChk

Every `db.createCollection` statement must include a validator definition statement

regex: `(?is)(?=.*createCollection)^(?!.*validator\s)`

# Sample Passing Script
``` mongosh 
{
            "changeSet": {
                "id": "create_students-collection",
                "author": "jennl",
                "labels": "[jira-101],'version 1.0'",
                "runWith": "mongosh",
                "changes": [
                  {
                    "mongoFile": {
                      "dbms": "mongodb",
                      "path": "create-collection-students.js",
                      "relativeToChangelogFile": true
                    }
                  }
                  ],       
                "rollback": [
                    {
                      "mongo": {
                        "mongo": "db.students.drop()"
                      }
                    }
                ]
            }    
        }
--create-collection-students.js contents
-- current bug in core is not finding QCs violation when this is embedded in changelog so
--it is defined in separate file that contains what is passed to mongosh
db.createCollection("students", {
        validator: {
                $jsonSchema: {
                      bsonType: "object",
                      title: "Student Document Validation",
                      required: [ "name", "year", "major" ],
                      properties: {
                        name: {
                            bsonType: "string",
                            description: "name must be a string and is required"
                        },
                        year: {
                            bsonType: "int",
                            minimum: 2017,
                            maximum: 3017,
                            description: "year must be an integer between 2017 and 3017 and is required"
                        },
                        major: {
                            enum: [ "Math", "English", "Computer Science", "History" ],
                            description: "can only be one of the enum values and is required"
                        }
                    }
                }
        }
    });

```
# Sample Failing Scripts
``` mongosh 
{
            "changeSet": {
                "id": "create_students-collection",
                "author": "jennl",
                "labels": "[jira-101],'version 1.0'",
                "runWith": "mongosh",
                "changes": [
                  {
                    "mongoFile": {
                      "dbms": "mongodb",
                      "path": "create-collection-students-fails.js",
                      "relativeToChangelogFile": true
                    }
                  }
                  ],       
                "rollback": [
                    {
                      "mongo": {
                        "mongo": "db.students.drop()"
                      }
                    }
                ]
            }    
        }
--create-collection-students-fails.js contents
-- current bug in core is not finding QCs violation when this is embedded in changelog so
--it is defined in separate file that contains what is passed to mongosh
db.createCollection("students");

```
# Sample Error Message
```
CHANGELOG CHECKS
----------------
Checks completed validation of the changelog and found the following issues:

Check Name:         Check for specific patterns in sql (mongoCrCollectionValidatorChk)
Changeset ID:       create_students-collection
Changeset Filepath: dbchangelog.json
Check Severity:     MINOR (Return code: 1)
Message:            A validator is not defined for the Collection that is being
                    created in Mongo. Please add validator statement.
```

# Step-by-Step
| Prompt | Command or User Input |
| ------ | ----------------------|
| > | `liquibase checks customize --check-name=SqlUserDefinedPatternCheck` |
| Give your check a short name for easier identification (up to 64 alpha-numeric characters only) [SqlUserDefinedPatternCheck1]: | `mongoCrCollectionValidatorChk` |
| Set the Severity to return a code of 0-4 when triggered. (options: 'INFO'=0, 'MINOR'=1, 'MAJOR'=2, 'CRITICAL'=3, 'BLOCKER'=4)? [INFO]: | `<Choose a value: 0, 1, 2, 3, 4>` |
| Set 'SEARCH_STRING' (options: a string, or a valid regular expression): | `(?is)(?=.*createCollection)^(?!.*validator\s)` |
| Set 'MESSAGE' [A match for regular expression <SEARCH_STRING> was detected in Changeset <CHANGESET>.]: | `A validator is not defined for the Collection that is being created in Mongo. Please add validator statement.` |
| Set 'STRIP_COMMENTS' (options: true, false) [true]: | `true` |
