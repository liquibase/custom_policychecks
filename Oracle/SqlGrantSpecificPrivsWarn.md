# SqlGrantSpecificPrivsWarn

This is a built-in check in Liquibase Pro. It is documented here: [SqlGrantSpecificPrivsWarn](https://docs.liquibase.com/commands/quality-checks/checks/changelog-checks/sql-grant-specific-privs-warn.html)

# Sample Failing Scripts
This check can be configured to warn on specific grant statements
``` sql
GRANT CREATE ANY TABLE TO LIQUIBASEUSER;
```
``` sql
GRANT DROP ANY TABLE TO LIQUIBASEUSER;
```
``` sql
GRANT SELECT ANY TABLE TO LIQUIBASEUSER;
```

# Sample Error Message
```
CHANGELOG CHECKS
----------------
Checks completed validation of the changelog and found the following issues:

Check Name:         Warn on Grant of Specific Privileges (SqlPrivsWarning)
Changeset ID:       grants
Changeset Filepath: changelog.xml
Check Severity:     BLOCKER (Return code: 4)
Message:            Changeset grants contains '"CREATE ANY TABLE"'
```
# Step-by-Step

| Prompt | Command or User Input |
| ------ | ----------------------|
| > | `liquibase checks enable --check-name=SqlGrantSpecificPrivsWarn` |
| Give your check a short name for easier identification (up to 64 alpha-numeric characters only) [SqlGrantSpecificPrivsWarn1]: | `SqlPrivsWarning` |
| Set the Severity to return a code of 0-4 when triggered. (options: 'INFO'=0, 'MINOR'=1, 'MAJOR'=2, 'CRITICAL'=3, 'BLOCKER'=4)? [INFO]: | `<Choose a value: 0, 1, 2, 3, 4>` |
| SSet 'PRIVILEGE_LIST' of users and roles, separated by commas (options: comma-separated list of valid database privileges): | This is an example list of privileges: `"ALTER SESSION","ALTER SYSTEM",EXP_FULL_DATABASE,IMP_FULL_DATABASE,"CREATE ANY TABLE","DROP ANY TABLE","ALTER ANY TABLE","SELECT ANY TABLE","COMMENT ANY TABLE","EXECUTE ANY PROCEDURE"` |
| Set 'STRIP_COMMENTS' (options: true, false) [true]: | `true` |

