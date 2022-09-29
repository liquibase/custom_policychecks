# MultipleGrantsNotAllowed

Multiple `GRANT` statements not allowed in a changeset.

regex: `(?is)[\t\r\n\s]*\bgrant\b[\t\r\n\s]+.*[\t\r\n\s]+\bgrant\b[\t\r\n\s]+`

# Sample Passing Script
``` sql
--changeset amalik:ORACLE_grant
GRANT SELECT ON TABLE sales TO appUser1;

--changeset amalik:SQLSERVER_grants
GRANT CONTROL ON dbo::CustOrderHist TO appUser;
```
# Sample Failing Scripts
``` sql
--changeset amalik:ORACLE_grant
GRANT SELECT ON TABLE sales TO appUser1;
GRANT EXECUTE TO appUser1;

--changeset amalik:SQLSERVER_grants
GRANT CONTROL ON dbo::CustOrderHist TO appUser;
GRANT CONTROL ON dbo::CustOrderHist TO appUser;
GRANT SHOWPLAN ON dbo::CustOrderHist TO appUser;
GRANT CREATE VIEW ON dbo::CustOrderHist TO appUser;
```

# Sample Error Message
```
CHANGELOG CHECKS
----------------
Checks completed validation of the changelog and found the following issues:

Check Name:         Check for specific patterns in sql (MultipleGrantsNotAllowed)
Changeset ID:       ORACLE_grant
Changeset Filepath: changeLogs/1_tables/03_grants.sql
Check Severity:     BLOCKER (Return code: 4)
Message:            Error! Multiple GRANT statements not allowed in a single
                    changeset. Only a single GRANT statement is allowed.
```

# Step-by-Step
| Prompt | Command or User Input |
| ------ | ----------------------|
| > | `liquibase checks customize --check-name=SqlUserDefinedPatternCheck` |
| Give your check a short name for easier identification (up to 64 alpha-numeric characters only) [SqlUserDefinedPatternCheck1]: | `# MultipleGrantsNotAllowed` |
| Set the Severity to return a code of 0-4 when triggered. (options: 'INFO'=0, 'MINOR'=1, 'MAJOR'=2, 'CRITICAL'=3, 'BLOCKER'=4)? [INFO]: | `<Choose a value: 0, 1, 2, 3, 4>` |
| Set 'SEARCH_STRING' (options: a string, or a valid regular expression): | `(?is)[\t\r\n\s]*\bgrant\b[\t\r\n\s]+.*[\t\r\n\s]+\bgrant\b[\t\r\n\s]+` |
| Set 'MESSAGE' [A match for regular expression <SEARCH_STRING> was detected in Changeset <CHANGESET>.]: | `Error! Multiple GRANT statements not allowed in a single changeset. Only a single GRANT statement is allowed.` |
| Set 'STRIP_COMMENTS' (options: true, false) [true]: | `true` |
