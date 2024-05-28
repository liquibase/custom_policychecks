# EnumerationListContext

Check that IF a context is provided, the context value must match a specified pattern.
Different than **UserDefinedContextCheck** because context is NOT REQUIRED in this check.
This check uses Check Chaining which requires Liquibase Pro 4.27.0+.

# Sample Passing Changesets
``` sql
--changeset ASmith:table01 context:PROD
create table table01 (
	id numeric not null,
	name varchar (255)
);
```

``` sql
--changeset ASmith:table01 context:!PROD
create table table01 (
	id numeric not null,
	name varchar (255)
);
```

``` sql
--changeset ASmith:table01
create table table01 (
	id numeric not null,
	name varchar (255)
);
```

# Sample Failing Changeset
``` sql
--changeset ASmith:table01 context:INVALID_ENVIRONMENT
create table table01 (
	id numeric not null,
	name varchar (255)
);
```

# Sample Error Message
```
DATABASE CHECKS
----------------
Validation of the database snapshot found the following issues:

Check Name:         Chained checks template (TablesWithoutPKNamingStandard)
Object Type:        table
Object Name:        tablewithoutpk
Object Location:    horses.horses.tablewithoutpk
Check Severity:     MAJOR (Return code: 2)
Message:            Tables without primary keys must have npk in the table name
```
# Step-by-Step

| Prompt | Command or User Input |
| ------ | ----------------------|
| > | `liquibase checks enable --check-name=ChangesetContextCheck` |

| Prompt | Command or User Input |
| ------ | ----------------------|
| > | `liquibase checks copy --check-name=UserDefinedContextCheck` |
| Give your check a short name for easier identification (up to 64 alpha-numeric characters only) [UserDefinedContextCheck1]: | `ContextEnvironmentsDevUatProd` |
| Set the Severity to return a code of 0-4 when triggered. (options: 'INFO'=0, 'MINOR'=1, 'MAJOR'=2, 'CRITICAL'=3, 'BLOCKER'=4)? [INFO]: | `<Choose a value: 0, 1, 2, 3, 4>` |
| Set 'OPERATOR' (options: STARTS_WITH, ENDS_WITH, CONTAINS, REGEXP, EQUALS) [STARTS_WITH]: | `REGEXP` |
| Set 'SEARCH_STRING' (options: a string, or a valid regular expression): | `(?i:(|(|!)DEV|(|!)UAT|(|!)PROD))` |

| Prompt | Command or User Input |
| ------ | ----------------------|
| > | `liquibase checks copy --check-name=ChainedChecksTemplate` |
| Give your check a short name for easier identification (up to 64 alpha-numeric characters only) [ChainedChecksTemplate1]: | `EnumerationListContext` |
| Set the Severity to return a code of 0-4 when triggered. (options: 'INFO'=0, 'MINOR'=1, 'MAJOR'=2, 'CRITICAL'=3, 'BLOCKER'=4)? [INFO]: | `<Choose a value: 0, 1, 2, 3, 4>` |
| Enter the shortname, logic conditional (using &&, \|\|, !), and optional (groupings) for your checks. Example: "(shortname1 && shortname2) \|\| shortname3": | `(!ChangesetContextCheck && ContextEnvironmentsDevUatProd)` |
| Set 'MESSAGE' [A match for regular expression <SEARCH_STRING> was detected in Changeset <CHANGESET>.]: | `If context is provided, value must be DEV, UAT, or PROD.` |