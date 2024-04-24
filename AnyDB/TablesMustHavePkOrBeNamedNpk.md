# TablesMustHavePkOrBeNamedNpk

Database check to find tables that do not have a Primary Key AND do not contain "NPK" in their name.
This check uses Check Chaining which requires Liquibase Pro 4.27.0+.

# Sample Passing Tables
``` sql
CREATE TABLE `tablenpk` (
  `id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL
);
```

``` sql
CREATE TABLE `tablewithpk` (
  `id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
);
```

# Sample Failing Table
``` sql
CREATE TABLE `tablewithoutpk` (
  `id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL
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
| > | `liquibase checks enable --check-name=ObjectNameMustNotMatch` |
| Give your check a short name for easier identification (up to 64 alpha-numeric characters only) [ObjectNameMustNotMatch1]: | `TablenameContainsNPK` |
| Set the Severity to return a code of 0-4 when triggered. (options: 'INFO'=0, 'MINOR'=1, 'MAJOR'=2, 'CRITICAL'=3, 'BLOCKER'=4)? [INFO]: | `<Choose a value: 0, 1, 2, 3, 4>` |
| Set 'OPERATOR' (options: STARTS_WITH, ENDS_WITH, CONTAINS, REGEXP, EQUALS) [STARTS_WITH]: | `CONTAINS` |
| Set 'SEARCH_STRING' (options: a string, or a valid regular expression): | `npk` |
| Set 'OBJECT_TYPES' to check, separated by commas (options: TABLE, COLUMN, SEQUENCE, INDEX, SCHEMA): | `TABLE` |
| Set 'CASE_SENSITIVE' (options: true, false) [true]: | `false` |

| Prompt | Command or User Input |
| ------ | ----------------------|
| > | `liquibase checks enable --check-name=ConstraintMustExist` |
| Give your check a short name for easier identification (up to 64 alpha-numeric characters only) [ConstraintMustExist1]: | `TablesMustHavePK` |
| Set the Severity to return a code of 0-4 when triggered. (options: 'INFO'=0, 'MINOR'=1, 'MAJOR'=2, 'CRITICAL'=3, 'BLOCKER'=4)? [INFO]: | `<Choose a value: 0, 1, 2, 3, 4>` |
| Set 'CONSTRAINT_OPERATOR' (options: STARTS_WITH, ENDS_WITH, CONTAINS, REGEXP, ALL) [STARTS_WITH]: | `ALL` |
| Enter the required constraint(s), separated by commas (options: NOT_NULL, UNIQUE, PRIMARYKEY, FOREIGNKEY, DEFAULT) [PRIMARYKEY]: | `PRIMARYKEY` |
| Set 'CASE_SENSITIVE' (options: true, false) [true]: | `true` |
| Set 'MESSAGE' [A match for regular expression <SEARCH_STRING> was detected in Changeset <CHANGESET>.]: | `All tables must have primary key.` |

| Prompt | Command or User Input |
| ------ | ----------------------|
| > | `liquibase checks copy --check-name=ChainedChecksTemplate` |
| Give your check a short name for easier identification (up to 64 alpha-numeric characters only) [ChainedChecksTemplate1]: | `TablesWithoutPKNamingStandard` |
| Set the Severity to return a code of 0-4 when triggered. (options: 'INFO'=0, 'MINOR'=1, 'MAJOR'=2, 'CRITICAL'=3, 'BLOCKER'=4)? [INFO]: | `<Choose a value: 0, 1, 2, 3, 4>` |
| Enter the shortname, logic conditional (using &&, \|\|, !), and optional (groupings) for your checks. Example: "(shortname1 && shortname2) \|\| shortname3": | `TablesMustHavePK && TablenameContainsNPK` |
| Set 'MESSAGE' [A match for regular expression <SEARCH_STRING> was detected in Changeset <CHANGESET>.]: | `Tables without primary keys must have npk in the table name` |