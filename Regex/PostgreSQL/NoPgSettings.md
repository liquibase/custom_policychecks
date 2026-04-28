# NoPgSettings

Do not allow `pg_settings` statements.

regex: `(?i)\bpg_settings\b`

# Sample Failing Scripts
``` sql
--changeset asmith:get_pgsettings
SELECT name, setting, unit 
FROM pg_settings 
WHERE name = 'work_mem';
```

# Sample Error Message
```
CHANGELOG CHECKS
----------------
Checks completed validation of the changelog and found the following issues:

Check Name:         Check for specific patterns in sql (NoPgSettings)
Changeset ID:       get_pgsettings
Changeset Filepath: changeLogs/selects/01_get_pgsettings.sql
Check Severity:     INFO (Return code: 0)
Message:            Error! pg_settings statements not allowed.
```

# Step-by-Step
| Prompt | Command or User Input |
| ------ | ----------------------|
| > | `liquibase checks customize --check-name=SqlUserDefinedPatternCheck` |
| Give your check a short name for easier identification (up to 64 alpha-numeric characters only) [SqlUserDefinedPatternCheck1]: | `NoPgSettings` |
| Set the Severity to return a code of 0-4 when triggered. (options: 'INFO'=0, 'MINOR'=1, 'MAJOR'=2, 'CRITICAL'=3, 'BLOCKER'=4)? [INFO]: | `<Choose a value: 0, 1, 2, 3, 4>` |
| Set 'SEARCH_STRING' (options: a string, or a valid regular expression): | `(?i)\bpg_settings\b` |
| Set 'MESSAGE' [A match for regular expression <SEARCH_STRING> was detected in Changeset <CHANGESET>.]: | `Error! pg_settings statements not allowed.` |
| Set 'STRIP_COMMENTS' (options: true, false) [true]: | `true` |
