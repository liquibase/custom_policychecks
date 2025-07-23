# SqlMustContainCreateView

All changesets in the named folder must have CREATE (OR REPLACE) VIEW statement only. For the example, the named folder is "2_view".

regex: `(?is)^((?!(create\s*view|cv|replace\s*view)).)*$`

# Sample Passing Script
``` sql
CREATE VIEW dept AS
 SELECT   deptno(TITLE 'Department Number'),
          deptname(TITLE 'Department Name'), 
          loc (TITLE 'Department Location'), 
          mgrno(TITLE 'Manager Number') 
 FROM department;
```

``` sql
REPLACE VIEW employee_info (number, name, position, department)
 AS SELECT employee.empno, name, jobtitle, deptno 
    FROM emp_info
    WHERE jobtitle NOT IN ('vice pres', 'manager');
```

# Sample Error Message
```
CHANGELOG CHECKS
----------------
Checks completed validation of the changelog and found the following issues:

Check Name:         Check for specific patterns in sql (SqlMustContainCreateView)
Changeset ID:       create_view_dept
Changeset Filepath: sql_code/2_view/create_view_dept.sql
Check Severity:     MAJOR (Return code: 2)
Message:            All changesets in the "2_view" folder must have CREATE VIEW statement only.
```
# Step-by-Step

| Prompt | Command or User Input |
| ------ | ----------------------|
| > | `liquibase checks copy --check-name=SqlUserDefinedPatternCheck` |
| Give your check a short name for easier identification (up to 64 alpha-numeric characters only) [SqlUserDefinedPatternCheck1]: | `SqlMustContainCreateView` |
| Set the Severity to return a code of 0-4 when triggered. (options: 'INFO'=0, 'MINOR'=1, 'MAJOR'=2, 'CRITICAL'=3, 'BLOCKER'=4)? [INFO]: | `<Choose a value: 0, 1, 2, 3, 4>` |
| Set 'SEARCH_STRING' (options: a string, or a valid regular expression): | `(?is)^((?!(create\s*view\|cv\|replace\s*view)).)*$` |
| Set 'MESSAGE' [A match for regular expression <SEARCH_STRING> was detected in Changeset <CHANGESET>.]: | `All changesets in the "2_view" folder must have CREATE (OR REPLACE) VIEW statement only.` |
| Set 'STRIP_COMMENTS' (options: true, false) [true]: | `true` |
| Set 'PATH_FILTER_REGEX': | `.*/2_view\/.*` |
| Set 'SPLIT_STATEMENTS' to split multiple SQL statements on the delimiter, and evaluate each individually (options: true, false) [false]: | `true` |
