# NoAlterUser

Do not allow `ALTER USER` statements.

regex: `(?is)(?=.*\b(alter)\b)(?=.*\b(user)\b).*`

# Sample Failing Scripts
``` sql
ALTER USER lb_user 
    IDENTIFIED BY L1QU1B@&3
    DEFAULT TABLESPACE lb_tbsp;
```

# Sample Error Message
```
CHANGELOG CHECKS
----------------
Checks completed validation of the changelog and found the following issues:

Check Name:         Check for specific patterns in sql (NoAlterUser)
Changeset ID:       01
Changeset Filepath: sql/main/100_ddl/97_alter_user.sql
Check Severity:     CRITICAL (Return code: 3)
Message:            Error! ALTER USER not allowed.
```

# Step-by-Step
| Prompt | Command or User Input |
| ------ | ----------------------|
| > | `liquibase checks customize --check-name=SqlUserDefinedPatternCheck` |
| Give your check a short name for easier identification (up to 64 alpha-numeric characters only) [SqlUserDefinedPatternCheck1]: | `NoAlterUser` |
| Set the Severity to return a code of 0-4 when triggered. (options: 'INFO'=0, 'MINOR'=1, 'MAJOR'=2, 'CRITICAL'=3, 'BLOCKER'=4)? [INFO]: | `<Choose a value: 0, 1, 2, 3, 4>` |
| Set 'SEARCH_STRING' (options: a string, or a valid regular expression): | `(?is)(?=.*\b(alter)\b)(?=.*\b(user)\b).*` |
| Set 'MESSAGE' [A match for regular expression <SEARCH_STRING> was detected in Changeset <CHANGESET>.]: | `Error! ALTER USER not allowed.` |
| Set 'STRIP_COMMENTS' (options: true, false) [true]: | `true` |
