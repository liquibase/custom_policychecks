# NoGrantAll

Do not allow `GRANT <Privilege Type> TO SYSTEM` statements.

regex: `(?i:grant)[\t\n\r\s\S]*(?i:to system)`

# Sample Failing Scripts
```
GRANT ALL PRIVILEGES TO user1;
```

# Sample Error Message
```
CHANGELOG CHECKS
----------------
Checks completed validation of the changelog and found the following issues:

Check Name:         Warn on Grant of Specific Privileges (NoGrantAll)
Changeset ID:       grant_all_to_user1
Changeset Filepath: changeLogs/1_tables/03_grants.sql
Check Severity:     BLOCKER (Return code: 4)
Message:            Change set grant_all_to_user1 contains '"ALL PRIVILEGES"'
```
# Step-by-Step

| Prompt | Command or User Input |
| ------ | ----------------------|
| > | `liquibase checks customize --check-name=SqlUserDefinedPatternCheck` |
| Give your check a short name for easier identification (up to 64 alpha-numeric characters only) [SqlGrantSpecificPrivsWarn1]: | `NoGrantAll` |
| Set the Severity to return a code of 0-4 when triggered. (options: 'INFO'=0, 'MINOR'=1, 'MAJOR'=2, 'CRITICAL'=3, 'BLOCKER'=4)? [INFO]: | `<Choose a value: 0, 1, 2, 3, 4>` |
| Set 'PRIVILEGE_LIST' of users and roles, separated by commas (options: comma-separated list of valid database privileges): | `ALL,"ALL PRIVILEGES"` |


