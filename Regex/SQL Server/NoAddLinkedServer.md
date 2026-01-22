# NoAddLinkedServer

Do not allow Add Linked Server statements.

regex: `(?i)sp_addlinked(server|srvlogin)`

# Sample Failing Scripts
``` sql
--changeset asmith:add_linked_server
EXECUTE master.dbo.sp_addlinkedserver
    @server = N'SRVR002\ACCTG',
    @srvproduct = N'SQL Server';	
```

# Sample Error Message
```
CHANGELOG CHECKS
----------------
Checks completed validation of the changelog and found the following issues:

Check Name:         Check for specific patterns in sql (NoAddLinkedServer)
Changeset ID:       add_linked_server
Changeset Filepath: changeLogs/logins/01_createLinkedServer.sql
Check Severity:     INFO (Return code: 0)
Message:            Error! Creation of linked servers is not allowed.
```

# Step-by-Step
| Prompt | Command or User Input |
| ------ | ----------------------|
| > | `liquibase checks customize --check-name=SqlUserDefinedPatternCheck` |
| Give your check a short name for easier identification (up to 64 alpha-numeric characters only) [SqlUserDefinedPatternCheck1]: | `NoAddLinkedServer` |
| Set the Severity to return a code of 0-4 when triggered. (options: 'INFO'=0, 'MINOR'=1, 'MAJOR'=2, 'CRITICAL'=3, 'BLOCKER'=4)? [INFO]: | `<Choose a value: 0, 1, 2, 3, 4>` |
| Set 'SEARCH_STRING' (options: a string, or a valid regular expression): | `(?i)sp_addlinked(server\|srvlogin)` |
| Set 'MESSAGE' [A match for regular expression <SEARCH_STRING> was detected in Changeset <CHANGESET>.]: | `Error! Creation of linked servers is not allowed.` |
| Set 'STRIP_COMMENTS' (options: true, false) [true]: | `true` |
