# NoGrantRevokeUsage

Do not allow `GRANT USAGE` or `REVOKE USAGE` statements.

regex: `(?i)\b(GRANT|REVOKE)\s+USAGE\b`

# Sample Failing Scripts
``` sql
--changeset asmith:set_usage
GRANT USAGE ON SCHEMA public TO my_role;
```

# Sample Error Message
```
CHANGELOG CHECKS
----------------
Checks completed validation of the changelog and found the following issues:

Check Name:         Check for specific patterns in sql (NoGrantRevokeUsage)
Changeset ID:       set_usage
Changeset Filepath: changeLogs/logins/01_set_usage.sql
Check Severity:     INFO (Return code: 0)
Message:            Error! GRANT and REVOKE USAGE statements not allowed.
```

# Step-by-Step
| Prompt | Command or User Input |
| ------ | ----------------------|
| > | `liquibase checks customize --check-name=SqlUserDefinedPatternCheck` |
| Give your check a short name for easier identification (up to 64 alpha-numeric characters only) [SqlUserDefinedPatternCheck1]: | `NoGrantRevokeUsage` |
| Set the Severity to return a code of 0-4 when triggered. (options: 'INFO'=0, 'MINOR'=1, 'MAJOR'=2, 'CRITICAL'=3, 'BLOCKER'=4)? [INFO]: | `<Choose a value: 0, 1, 2, 3, 4>` |
| Set 'SEARCH_STRING' (options: a string, or a valid regular expression): | `(?i)\b(GRANT\|REVOKE)\s+USAGE\b` |
| Set 'MESSAGE' [A match for regular expression <SEARCH_STRING> was detected in Changeset <CHANGESET>.]: | `Error! GRANT and REVOKE USAGE statements not allowed.` |
| Set 'STRIP_COMMENTS' (options: true, false) [true]: | `true` |
