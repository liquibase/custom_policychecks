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

# Sample Passing Scripts
``` sql
create table DBO.SALES
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
```
Command: liquibase checks copy --check-name=SqlUserDefinedPatternCheck
Short Name: TableNamesMustBeUppercase
Severity: <Choose a value: 0, 1, 2, 3, 4>
Search String: (?im)create\s*(or\s*replace\s*|)table\s*((?-i).*[a-z].*)\s*\(
Message: Table names should be UPPERCASE
Strip Comments: true
```