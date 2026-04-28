# DoNotUseAddDependOrDbase

Catches PostgreSQL internal/system functions and legacy database references.

regex: `(?i)\b(adddepend(ency)?|pg_adddepend|pg_depend|dbase)\b`

# Sample Failing Scripts
``` sql
SELECT pg_adddepend('pg_class', 1259, 0, 'pg_class', 1259, 0, 'n');
```
``` sql
SELECT * FROM DBASE.public.users;
```

# Sample Error Message
```
CHANGELOG CHECKS
----------------
Checks completed validation of the changelog and found the following issues:

Check Name:         Check for specific patterns in sql (DoNotUseAddDependOrDbase)
Changeset ID:       legacy_dbase
Changeset Filepath: changeLogs/tables/legacy_dbase.sql
Check Severity:     INFO (Return code: 0)
Message:            Do not use pg_adddepend, pg_depend, or dbase references.
```
# Step-by-Step

| Prompt | Command or User Input |
| ------ | ----------------------|
| > | `liquibase checks customize --check-name=SqlUserDefinedPatternCheck` |
| Give your check a short name for easier identification (up to 64 alpha-numeric characters only) [SqlUserDefinedPatternCheck1]: | `DoNotUseAddDependOrDbase` |
| Set the Severity to return a code of 0-4 when triggered. (options: 'INFO'=0, 'MINOR'=1, 'MAJOR'=2, 'CRITICAL'=3, 'BLOCKER'=4)? [INFO]: | `<Choose a value: 0, 1, 2, 3, 4>` |
| Set 'SEARCH_STRING' (options: a string, or a valid regular expression): | `(?i)\b(adddepend(ency)?\|pg_adddepend\|pg_depend\|dbase)\b` |
| Set 'MESSAGE' [A match for regular expression <SEARCH_STRING> was detected in Changeset <CHANGESET>.]: | `Do not use pg_adddepend, pg_depend, or dbase references.` |
| Set 'STRIP_COMMENTS' (options: true, false) [true]: | `true` |

