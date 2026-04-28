# DoNotUseCreateDropLanguage

Do not use CREATE or DROP language.

regex: `(?i)\b(create|drop)\s+(or\s+replace\s+)?(trusted\s+)?(procedural\s+)?language\b`

# Sample Failing Scripts
``` sql
CREATE LANGUAGE plpython3u;
```
``` sql
DROP LANGUAGE plpython3u CASCADE;
```

# Sample Error Message
```
CHANGELOG CHECKS
----------------
Checks completed validation of the changelog and found the following issues:

Check Name:         Check for specific patterns in sql (DoNotUseCreateDropLanguage)
Changeset ID:       create_language
Changeset Filepath: changeLogs/tools/create_language.sql
Check Severity:     INFO (Return code: 0)
Message:            Do not use CREATE or DROP language. 
```
# Step-by-Step

| Prompt | Command or User Input |
| ------ | ----------------------|
| > | `liquibase checks customize --check-name=SqlUserDefinedPatternCheck` |
| Give your check a short name for easier identification (up to 64 alpha-numeric characters only) [SqlUserDefinedPatternCheck1]: | `DoNotUseCreateDropLanguage` |
| Set the Severity to return a code of 0-4 when triggered. (options: 'INFO'=0, 'MINOR'=1, 'MAJOR'=2, 'CRITICAL'=3, 'BLOCKER'=4)? [INFO]: | `<Choose a value: 0, 1, 2, 3, 4>` |
| Set 'SEARCH_STRING' (options: a string, or a valid regular expression): | `(?i)\b(create\|drop)\s+(or\s+replace\s+)?(trusted\s+)?(procedural\s+)?language\b` |
| Set 'MESSAGE' [A match for regular expression <SEARCH_STRING> was detected in Changeset <CHANGESET>.]: | `Do not use CREATE or DROP language.` |
| Set 'STRIP_COMMENTS' (options: true, false) [true]: | `true` |

