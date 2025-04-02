# CreateTablespaceMustHaveSecqty131760

CREATE TABLESPACE statements must include SECQTY 131760.

regex: `(?is)(?=.*\b(create)\b)(?=.*\b(tablespace)\b)(?!.*\b(secqty\s*131760)\b)`

# Sample Passing Scripts
``` sql
--changeset asmith:create_tablespace_01
  CREATE TABLESPACE ABC00001
    IN DBA0001
    USING STOGROUP SYSPOOL1
	MAXPARTITIONS 20
;
```

# Sample Failing Scripts
``` sql
--changeset asmith:create_tablespace_without_secqty_131760
  CREATE TABLESPACE ABC00001
    IN DBA0001
    USING STOGROUP SYSPOOL1
;
```

# Sample Error Message
``` 
CHANGELOG CHECKS
----------------
Checks completed validation of the changelog and found the following issues:

Check Name:         Check for specific patterns in sql (CreateTablespaceMustHaveSecqty131760)
Changeset ID:       create_tablespace_without_secqty_131760
Changeset Filepath: sql_code/Scripts/TBSPACE_01.sql
Check Severity:     BLOCKER (Return code: 4)
Message:            Error! CREATE TABLESPACE must contain SECQTY 131760.
```

# Step-by-Step
| Prompt | Command or User Input |
| ------ | ----------------------|
| > | `liquibase checks customize --check-name=SqlUserDefinedPatternCheck` |
| Give your check a short name for easier identification (up to 64 alpha-numeric characters only) [SqlUserDefinedPatternCheck1]: | `CreateTablespaceMustHaveSecqty131760` |
| Set the Severity to return a code of 0-4 when triggered. (options: 'INFO'=0, 'MINOR'=1, 'MAJOR'=2, 'CRITICAL'=3, 'BLOCKER'=4)? [INFO]: | `<Choose a value: 0, 1, 2, 3, 4>` |
| Set 'SEARCH_STRING' (options: a string, or a valid regular expression): | `(?is)(?=.*\b(create)\b)(?=.*\b(tablespace)\b)(?!.*\b(secqty\s*131760)\b)` |
| Set 'MESSAGE' [A match for regular expression <SEARCH_STRING> was detected in Changeset <CHANGESET>.]: | `Error! CREATE TABLESPACE must contain SECQTY 131760.` |
| Set 'STRIP_COMMENTS' (options: true, false) [true]: | `true` |
