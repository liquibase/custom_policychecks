# ViewsMustHaveCreateOrReplaceViewOnly

All changesets in the Views folder must have CREATE OR REPLACE VIEW statement.

regex: `(?is)^((?!create\s*or\s*replace\s*view).)*$`

path_filter_regex: `Views\/.*`

# Sample Passing Changeset
``` sql
--changeset user.name:films_01_vw labels:CRQ123456
CREATE OR REPLACE VIEW films_01_vw(name,id) AS (
  SELECT
    name,id
  FROM
    films_01
);
```

# Sample Failing Changeset
``` sql
--changeset user.name:films_01_vw labels:CRQ123456
CREATE VIEW films_01_vw(name,id) AS (
  SELECT
    name,id
  FROM
    films_01
);
```

# Sample Error Message
```
CHANGELOG CHECKS
----------------
Checks completed validation of the changelog and found the following issues:

Check Name:         Check for specific patterns in sql (ViewsMustHaveCreateOrReplaceViewOnly)
Changeset ID:       new-view
Changeset Filepath: Views/bad_view.sql
Check Severity:     MAJOR (Return code: 2)
Message:            Views must have CREATE OR REPLACE VIEW statement.
```
# Step-by-Step

| Prompt | Command or User Input |
| ------ | ----------------------|
| > | `liquibase checks copy --check-name=SqlUserDefinedPatternCheck` |
| Give your check a short name for easier identification (up to 64 alpha-numeric characters only) [SqlUserDefinedPatternCheck1]: | `ViewsMustHaveCreateOrReplaceViewOnly` |
| Set the Severity to return a code of 0-4 when triggered. (options: 'INFO'=0, 'MINOR'=1, 'MAJOR'=2, 'CRITICAL'=3, 'BLOCKER'=4)? [INFO]: | `<Choose a value: 0, 1, 2, 3, 4>` |
| Set 'SEARCH_STRING' (options: a string, or a valid regular expression): | `(?is)^((?!create\s*or\s*replace\s*view).)*$` |
| Set 'MESSAGE' [A match for regular expression <SEARCH_STRING> was detected in Changeset <CHANGESET>.]: | `Views must have CREATE OR REPLACE VIEW statement.` |
| Set 'STRIP_COMMENTS' (options: true, false) [true]: | `true` |
| Set 'PATH_FILTER_REGEX': | `Views\/.*` |
