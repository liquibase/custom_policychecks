# NoAlterProcedure

Every `ALTER PROCEDURE` statement should be flagged.

regex: `(?i:alter\s)\s*(?i:procedure\s)`

# Sample Failing Scripts
``` sql
--changeset amalik:alter_CustOrderHist
ALTER PROCEDURE [dbo].[CustOrderHist] @CustomerID nchar(5)
AS
SELECT ProductName, Total=SUM(Quantity)
FROM Products P, [Order Details] OD, Orders O, Customers C
WHERE C.CustomerID = @CustomerID
AND C.CustomerID = O.CustomerID AND O.OrderID = OD.OrderID AND OD.ProductID = P.ProductID
GROUP BY ProductName
```

# Sample Error Message
``` 
CHANGELOG CHECKS
----------------
Checks completed validation of the changelog and found the following issues:

Check Name:         Check for specific patterns in sql (NoAlterProcedure)
Changeset ID:       alter_CustOrderHist
Changeset Filepath: changeLogs/2_objects/02_storedprocedure/alter_CustOrderHist.sql
Check Severity:     BLOCKER (Return code: 4)
Message:            Error! ALTER PROCEDURE not allowed.
```

# Step-by-Step
| Prompt | Command or User Input |
| ------ | ----------------------|
| > | `liquibase checks customize --check-name=SqlUserDefinedPatternCheck` |
| Give your check a short name for easier identification (up to 64 alpha-numeric characters only) [SqlUserDefinedPatternCheck1]: | `NoAlterProcedure` |
| Set the Severity to return a code of 0-4 when triggered. (options: 'INFO'=0, 'MINOR'=1, 'MAJOR'=2, 'CRITICAL'=3, 'BLOCKER'=4)? [INFO]: | `<Choose a value: 0, 1, 2, 3, 4>` |
| Set 'SEARCH_STRING' (options: a string, or a valid regular expression): | `(?i:alter\s)\s*(?i:procedure\s)` |
| Set 'MESSAGE' [A match for regular expression <SEARCH_STRING> was detected in Changeset <CHANGESET>.]: | `Error! ALTER PROCEDURE not allowed.` |
| Set 'STRIP_COMMENTS' (options: true, false) [true]: | `true` |
