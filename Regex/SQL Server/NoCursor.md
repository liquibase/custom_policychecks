# NoCursor

No statements with `CURSOR` allowed. 

regex: `(?i:\scursor\s)`

# Sample Failing Scripts
``` sql
--changeset amalik:cursor
DECLARE @name VARCHAR(50) -- database name 
DECLARE @path VARCHAR(256) -- path for backup files 
DECLARE @fileName VARCHAR(256) -- filename for backup 
DECLARE @fileDate VARCHAR(20) -- used for file name 

SET @path = 'C:\Backup\' 

SELECT @fileDate = CONVERT(VARCHAR(20),GETDATE(),112) 

DECLARE db_cursor CURSOR FOR 
SELECT name 
FROM MASTER.dbo.sysdatabases 
WHERE name NOT IN ('master','model','msdb','tempdb') 

OPEN db_cursor  
FETCH NEXT FROM db_cursor INTO @name  

WHILE @@FETCH_STATUS = 0  
BEGIN  
      SET @fileName = @path + @name + '_' + @fileDate + '.BAK' 
      BACKUP DATABASE @name TO DISK = @fileName 

      FETCH NEXT FROM db_cursor INTO @name 
END 

CLOSE db_cursor  
DEALLOCATE db_cursor
```

# Sample Error Message
```
CHANGELOG CHECKS
----------------
Checks completed validation of the changelog and found the following issues:

Check Name:         Check for specific patterns in sql (NoCursor)
Changeset ID:       cursor
Changeset Filepath: changeLogs/2_objects/02_storedprocedure/cursor.sql
Check Severity:     INFO (Return code: 0)
Message:            Warning! CURSOR detected!
```

# Step-by-Step
| Prompt | Command or User Input |
| ------ | ----------------------|
| > | `liquibase checks customize --check-name=SqlUserDefinedPatternCheck` |
| Give your check a short name for easier identification (up to 64 alpha-numeric characters only) [SqlUserDefinedPatternCheck1]: | `NoCursor` |
| Set the Severity to return a code of 0-4 when triggered. (options: 'INFO'=0, 'MINOR'=1, 'MAJOR'=2, 'CRITICAL'=3, 'BLOCKER'=4)? [INFO]: | `<Choose a value: 0, 1, 2, 3, 4>` |
| Set 'SEARCH_STRING' (options: a string, or a valid regular expression): | `(?i:\scursor\s)` |
| Set 'MESSAGE' [A match for regular expression <SEARCH_STRING> was detected in Changeset <CHANGESET>.]: | `Warning! CURSOR detected!` |
| Set 'STRIP_COMMENTS' (options: true, false) [true]: | `true` |
