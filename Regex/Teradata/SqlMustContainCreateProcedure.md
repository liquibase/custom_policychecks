# SqlMustContainCreateProcedure

All changesets in the named folder must have CREATE (OR REPLACE) PROCEDURE statement only. For the example, the named folder is "4_procedure".

regex: `(?is)^((?!(create\s*procedure|replace\s*procedure)).)*$`

# Sample Passing Script
``` sql
CREATE PROCEDURE NewProc (IN name CHAR(12),
                          IN number INTEGER,
                          IN dept INTEGER,
                          OUT dname CHAR(10))
BEGIN
   INSERT INTO Employee (EmpName, EmpNo, DeptNo )
      VALUES (name, number, dept);
   SELECT DeptName
      INTO dname FROM Department
         WHERE DeptNo = dept;
END;
```

# Sample Error Message
```
CHANGELOG CHECKS
----------------
Checks completed validation of the changelog and found the following issues:

Check Name:         Check for specific patterns in sql (SqlMustContainCreateProcedure)
Changeset ID:       create_procedure_new_proc
Changeset Filepath: sql_code/4_procedure/create_procedure_new_proc.sql
Check Severity:     MAJOR (Return code: 2)
Message:            All changesets in the "4_procedure" folder must have CREATE PROCEDURE statement only.
```
# Step-by-Step

| Prompt | Command or User Input |
| ------ | ----------------------|
| > | `liquibase checks copy --check-name=SqlUserDefinedPatternCheck` |
| Give your check a short name for easier identification (up to 64 alpha-numeric characters only) [SqlUserDefinedPatternCheck1]: | `SqlMustContainCreateProcedure` |
| Set the Severity to return a code of 0-4 when triggered. (options: 'INFO'=0, 'MINOR'=1, 'MAJOR'=2, 'CRITICAL'=3, 'BLOCKER'=4)? [INFO]: | `<Choose a value: 0, 1, 2, 3, 4>` |
| Set 'SEARCH_STRING' (options: a string, or a valid regular expression): | `(?is)^((?!(create\s*procedure\|replace\s*procedure)).)*$` |
| Set 'MESSAGE' [A match for regular expression <SEARCH_STRING> was detected in Changeset <CHANGESET>.]: | `All changesets in the "4_procedure" folder must have CREATE (OR REPLACE) PROCEDURE statement only.` |
| Set 'STRIP_COMMENTS' (options: true, false) [true]: | `true` |
| Set 'PATH_FILTER_REGEX': | `.*/4_procedure\/.*` |
| Set 'SPLIT_STATEMENTS' to split multiple SQL statements on the delimiter, and evaluate each individually (options: true, false) [false]: | `true` |
