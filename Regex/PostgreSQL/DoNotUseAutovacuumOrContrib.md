# DoNotUseAutovacuumOrContrib

Catches PostgreSQL maintenance internals and extension infrastructure.

regex: `(?i)\b(autovacuum|pg_autovacuum|vacuum_cost_delay|vacuum_cost_limit|contrib|pg_available_extensions|pg_extension)\b`

# Sample Failing Scripts
``` sql
ALTER TABLE users SET (autovacuum_enabled = false);
```
``` sql
SELECT * FROM pg_available_extensions WHERE name LIKE '%contrib%';
```

# Sample Error Message
```
CHANGELOG CHECKS
----------------
Checks completed validation of the changelog and found the following issues:

Check Name:         Check for specific patterns in sql (DoNotUseAutovacuumOrContrib)
Changeset ID:       autovacuum
Changeset Filepath: changeLogs/tools/autovacuum.sql
Check Severity:     INFO (Return code: 0)
Message:            Do not use vacuum or contrib or other commands related to maintenance internals. 
```
# Step-by-Step

| Prompt | Command or User Input |
| ------ | ----------------------|
| > | `liquibase checks customize --check-name=SqlUserDefinedPatternCheck` |
| Give your check a short name for easier identification (up to 64 alpha-numeric characters only) [SqlUserDefinedPatternCheck1]: | `DoNotUseAutovacuumOrContrib` |
| Set the Severity to return a code of 0-4 when triggered. (options: 'INFO'=0, 'MINOR'=1, 'MAJOR'=2, 'CRITICAL'=3, 'BLOCKER'=4)? [INFO]: | `<Choose a value: 0, 1, 2, 3, 4>` |
| Set 'SEARCH_STRING' (options: a string, or a valid regular expression): | `(?i)\b(autovacuum\|pg_autovacuum\|vacuum_cost_delay\|vacuum_cost_limit\|contrib\|pg_available_extensions\|pg_extension)\b` |
| Set 'MESSAGE' [A match for regular expression <SEARCH_STRING> was detected in Changeset <CHANGESET>.]: | `Do not use vacuum or contrib or other commands related to maintenance internals.` |
| Set 'STRIP_COMMENTS' (options: true, false) [true]: | `true` |

