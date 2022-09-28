# NoOpenRowSet

No statements with `OPENROWSET` allowed. 

regex: `(?i:openrowset)\s*\(`

# Sample Failing Scripts
``` sql
--changeset amalik:openrowset
SELECT a.*
   FROM OPENROWSET('Microsoft.Jet.OLEDB.4.0',
                   'C:\SAMPLES\Northwind.mdb';
                   'admin';
                   'password',
                   Customers) AS a;
```

# Sample Error Message
``` 
CHANGELOG CHECKS
----------------
Checks completed validation of the changelog and found the following issues:

Check Name:         Check for specific patterns in sql (NoOpenRowSet)
Changeset ID:       openrowset
Changeset Filepath: changeLogs/3_data/openrowset.sql
Check Severity:     INFO (Return code: 4)
Message:            Error! OPENROWSET detected.
```

# Step-by-Step
| Prompt | Command or User Input |
| ------ | ----------------------|
| > | `liquibase checks customize --check-name=SqlUserDefinedPatternCheck` |
| Give your check a short name for easier identification (up to 64 alpha-numeric characters only) [SqlUserDefinedPatternCheck1]: | `NoOpenRowSet` |
| Set the Severity to return a code of 0-4 when triggered. (options: 'INFO'=0, 'MINOR'=1, 'MAJOR'=2, 'CRITICAL'=3, 'BLOCKER'=4)? [INFO]: | `<Choose a value: 0, 1, 2, 3, 4>` |
| Set 'SEARCH_STRING' (options: a string, or a valid regular expression): | `(?i:openrowset)\s*\(` |
| Set 'MESSAGE' [A match for regular expression <SEARCH_STRING> was detected in Changeset <CHANGESET>.]: | `Error! OPENROWSET detected.` |
| Set 'STRIP_COMMENTS' (options: true, false) [true]: | `true` |
