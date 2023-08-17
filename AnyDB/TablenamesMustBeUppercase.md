# UppercaseTableNames

Table names should be UPPERCASE

regex: `(?im)create\s*(or\s*replace\s*|)table\s*((?-i).*[a-z].*)\s*\(`

# Sample Failing Scripts
``` sql
create table dbo.SALES
```
``` sql
CREATE TABLE DBO.sales
```
``` sql
create table Sales
```

# Sample Error Message
```
CHANGELOG CHECKS
----------------
Checks completed validation of the changelog and found the following issues:

Check Name:         Check for specific patterns in sql (TableNamesMustBeUppercase)
Changeset ID:       01
Changeset Filepath: Tables/SALES.sql
Check Severity:     MINOR (Return code: 1)
Message:            Table names should be UPPERCASE
```
# Step-by-Step

| Prompt | Command or User Input |
| ------ | ----------------------|
| > | `liquibase checks copy --check-name=SqlUserDefinedPatternCheck` |
| Give your check a short name for easier identification (up to 64 alpha-numeric characters only) [SqlUserDefinedPatternCheck1]: | `TableNamesMustBeUppercase` |
| Set the Severity to return a code of 0-4 when triggered. (options: 'INFO'=0, 'MINOR'=1, 'MAJOR'=2, 'CRITICAL'=3, 'BLOCKER'=4)? [INFO]: | `<Choose a value: 0, 1, 2, 3, 4>` |
| Set 'SEARCH_STRING' (options: a string, or a valid regular expression): | `(?im)create\s$\times$(or\s$\times$replace\s$\times$|)table\s$\times$((?-i).$\times$[a-z].$\times$)\s$\times$\(` |
| Set 'MESSAGE' [A match for regular expression <SEARCH_STRING> was detected in Changeset <CHANGESET>.]: | `Table names should be UPPERCASE` |
| Set 'STRIP_COMMENTS' (options: true, false) [true]: | `true` |

