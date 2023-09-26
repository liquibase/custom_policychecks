# NoGrantWithGrantOption

`GRANT ... WITH GRANT OPTION;` not allowed.

regex: `(?is)(?=.*\b(grant)\b).*(?=.*\b(with)\b)(?=.*\b(grant)\b)(?=.*\b(option)\b).*`


# Sample Failing Scripts
``` sql
--changeset amalik:grant_with_grant_option
GRANT EXECUTE ON myProc TO AppRole WITH GRANT OPTION;
```

# Sample Error Message
``` 
CHANGELOG CHECKS
----------------
Checks completed validation of the changelog and found the following issues:

Check Name:         Check for specific patterns in sql (NoGrantWithGrantOption)
Changeset ID:       QC_script
Changeset Filepath: main/QCs/grant_with_grant_option.sql
Check Severity:     BLOCKER (Return code: 4)
Message:            Error! GRANT ... WITH GRANT OPTION statement found.
```

# Step-by-Step
| Prompt | Command or User Input |
| ------ | ----------------------|
| > | `liquibase checks customize --check-name=SqlUserDefinedPatternCheck` |
| Give your check a short name for easier identification (up to 64 alpha-numeric characters only) [SqlUserDefinedPatternCheck1]: | `NoGrantWithGrantOption` |
| Set the Severity to return a code of 0-4 when triggered. (options: 'INFO'=0, 'MINOR'=1, 'MAJOR'=2, 'CRITICAL'=3, 'BLOCKER'=4)? [INFO]: | `<Choose a value: 0, 1, 2, 3, 4>` |
| Set 'SEARCH_STRING' (options: a string, or a valid regular expression): | `(?is)(?=.*\b(grant)\b).*(?=.*\b(with)\b)(?=.*\b(grant)\b)(?=.*\b(option)\b).*` |
| Set 'MESSAGE' [A match for regular expression <SEARCH_STRING> was detected in Changeset <CHANGESET>.]: | `Error! GRANT ... WITH GRANT OPTION statement found.` |
| Set 'STRIP_COMMENTS' (options: true, false) [true]: | `true` |
