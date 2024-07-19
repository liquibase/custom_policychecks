# CannotModifyUsersOrRoles

Do not allow the following statements for `USER`:
<br>`CREATE [OR REPLACE] USER`
<br>`DROP USER`
<br>`ALTER USER`
<br>`RENAME USER`

Do not allow the following statements for `ROLE`:
<br>`CREATE [OR REPLACE] ROLE`
<br>`DROP ROLE`
<br>`SET ROLE`

regex: `(?is)(?=.*\b(create|replace|drop|alter|set)\b)(?=.*\b(user|role)\b).*`

# Sample Failing Scripts for USER
``` sql
CREATE [OR REPLACE] USER lb_user 
    IDENTIFIED BY L!QU!B@S3 
    DEFAULT TABLESPACE lb_tbsp 
    QUOTA 10M ON lb_tbsp 
    QUOTA 5M ON system 
    PROFILE app_user 
    PASSWORD EXPIRE;
```
``` sql
DROP USER lb_user;
```
``` sql
ALTER USER lb_user 
    IDENTIFIED BY L1QU1B@&3
    DEFAULT TABLESPACE lb_tbsp;
```
``` sql
RENAME USER 'lb_user' TO 'liquibase';
```

# Sample Failing Scripts for ROLE
``` sql
CREATE [OR REPLACE] ROLE lb_role;
```
``` sql
DROP ROLE lb_role;
```
``` sql
SET ROLE lb_role;
```

# Sample Error Message
```
CHANGELOG CHECKS
----------------
Checks completed validation of the changelog and found the following issues:

Check Name:         Check for specific patterns in sql (CannotModifyUsersOrRoles)
Changeset ID:       01
Changeset Filepath: sql/main/100_ddl/97_alter_user.sql
Check Severity:     MAJOR (Return code: 2)
Message:            Modifying USER or ROLE is prohibited.
```

# Step-by-Step
| Prompt | Command or User Input |
| ------ | ----------------------|
| > | `liquibase checks customize --check-name=SqlUserDefinedPatternCheck` |
| Give your check a short name for easier identification (up to 64 alpha-numeric characters only) [SqlUserDefinedPatternCheck1]: | `CannotModifyUsersOrRoles` |
| Set the Severity to return a code of 0-4 when triggered. (options: 'INFO'=0, 'MINOR'=1, 'MAJOR'=2, 'CRITICAL'=3, 'BLOCKER'=4)? [INFO]: | `<Choose a value: 0, 1, 2, 3, 4>` |
| Set 'SEARCH_STRING' (options: a string, or a valid regular expression): | `(?is)(?=.*\b(create\|replace\|drop\|alter\|set)\b)(?=.*\b(user\|role)\b).*` |
| Set 'MESSAGE' [A match for regular expression <SEARCH_STRING> was detected in Changeset <CHANGESET>.]: | `Modifying USER or ROLE is prohibited.` |
| Set 'STRIP_COMMENTS' (options: true, false) [true]: | `true` |