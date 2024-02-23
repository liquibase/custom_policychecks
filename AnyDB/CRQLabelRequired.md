# CRQLabelRequired

All changesets must have a CRQ (change request) label assigned.

regex: `(?i:crq\d+)`

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
--changeset user.name:films_01 labels:v.1.0.1
create table films_01 (
  id int, 
  name varchar(30)
);
```

# Sample Error Message
```
CHANGELOG CHECKS
----------------
Checks completed validation of the changelog and found the following issues:

Check Name:         Check for User Defined Label (CRQLabelRequired)
Changeset ID:       table_missing_crq
Changeset Filepath: changelogs/ddl/missing_crq.sql
Check Severity:     INFO (Return code: 4)
Message:            Changeset label: '' did not match the pattern: matches the regular expression '(?i:crq\d+)'. Please review this label.
```
# Step-by-Step

| Prompt | Command or User Input |
| ------ | ----------------------|
| > | `liquibase checks copy --check-name=UserDefinedLabelCheck` |
| Give your check a short name for easier identification (up to 64 alpha-numeric characters only) [UserDefinedLabelCheck1]: | `CRQLabelRequired` |
| Set the Severity to return a code of 0-4 when triggered. (options: 'INFO'=0, 'MINOR'=1, 'MAJOR'=2, 'CRITICAL'=3, 'BLOCKER'=4)? [INFO]: | `<Choose a value: 0, 1, 2, 3, 4>` |
| Set 'OPERATOR' (options: STARTS_WITH, ENDS_WITH, CONTAINS, REGEXP, EQUALS) [STARTS_WITH]: | `REGEXP` |
| Set 'SEARCH_STRING' (options: a string, or a valid regular expression): | `(?i:crq\d+)` |