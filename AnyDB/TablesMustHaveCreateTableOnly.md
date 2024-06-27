# TablesMustHaveCreateTableOnly

All changesets in the Tables folder must have CREATE TABLE statement only.

regex: `(?is)^((?!create\s*table).)*$`
path_filter_regex: `Tables\/.*`

# Sample Passing Changeset
``` sql
--changeset user.name:films_01 labels:CRQ123456
create table films_01 (
  id int, 
  name varchar(30)
);
```

# Sample Failing Changeset
``` sql
--changeset user.name:films_01 labels:CRQ123456
create or replace table films_01 (
  id int, 
  name varchar(30)
);
```

# Sample Error Message
```
CHANGELOG CHECKS
----------------
Checks completed validation of the changelog and found the following issues:

Check Name:         Check for specific patterns in sql (TablesMustHaveCreateTableOnly)
Changeset ID:       new-table
Changeset Filepath: Tables/bad_table.sql
Check Severity:     INFO (Return code: 2)
Message:            Tables must have CREATE TABLE statement.
```
# Step-by-Step

| Prompt | Command or User Input |
| ------ | ----------------------|
| > | `liquibase checks copy --check-name=SqlUserDefinedPatternCheck` |
| Give your check a short name for easier identification (up to 64 alpha-numeric characters only) [SqlUserDefinedPatternCheck1]: | `TablesMustHaveCreateTableOnly` |
| Set the Severity to return a code of 0-4 when triggered. (options: 'INFO'=0, 'MINOR'=1, 'MAJOR'=2, 'CRITICAL'=3, 'BLOCKER'=4)? [INFO]: | `<Choose a value: 0, 1, 2, 3, 4>` |
| Set 'SEARCH_STRING' (options: a string, or a valid regular expression): | `(?is)^((?!create\s*table).)*$` |
| Set 'MESSAGE' [A match for regular expression <SEARCH_STRING> was detected in Changeset <CHANGESET>.]: | `Tables must have CREATE TABLE statement.` |
| Set 'STRIP_COMMENTS' (options: true, false) [true]: | `true` |
