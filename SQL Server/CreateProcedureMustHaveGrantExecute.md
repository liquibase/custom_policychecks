# CreateProcedureMustHaveGrantExecute

Every `CREATE PROCEDURE` statement must follow `GRANT EXECUTE` statement for the same procedure.

regex: `(?is)(?=.*\b(create)\b)(?=.*\b(procedure)\b)(?!.*\b(grant)\b)(?!.*\b(execute)\b).*`

# Sample Passing Scripts
``` sql
--changeset amalik:CustOrderHist
CREATE OR REPLACE PROCEDURE dbo.CustOrderHist @CustomerID nchar(5)
AS
SELECT ProductName, Total=SUM(Quantity)
FROM Products P, [Order Details] OD, Orders O, Customers C
WHERE C.CustomerID = @CustomerID
AND C.CustomerID = O.CustomerID AND O.OrderID = OD.OrderID AND OD.ProductID = P.ProductID
GROUP BY ProductName

GRANT EXECUTE ON dbo::CustOrderHist TO AppUser1;  
```

# Sample Failing Scripts
``` sql
--changeset amalik:CustOrderHist
CREATE OR REPLACE PROCEDURE dbo.CustOrderHist @CustomerID nchar(5)
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

Check Name:         Check for specific patterns in sql (CreateProcedureMustHaveGrantExecute)
Changeset ID:       CustOrderHist
Changeset Filepath: changeLogs/2_objects/02_storedprocedure/CustOrderHist.sql
Check Severity:     BLOCKER (Return code: 4)
Message:            Error! CREATE PROCEDURE statement found without a GRANT
                    EXECUTE statement.
```

# Step-by-Step
| Prompt | Command or User Input |
| ------ | ----------------------|
| > | `liquibase checks customize --check-name=SqlUserDefinedPatternCheck` |
| Give your check a short name for easier identification (up to 64 alpha-numeric characters only) [SqlUserDefinedPatternCheck1]: | `CreateProcedureMustHaveGrantExecute` |
| Set the Severity to return a code of 0-4 when triggered. (options: 'INFO'=0, 'MINOR'=1, 'MAJOR'=2, 'CRITICAL'=3, 'BLOCKER'=4)? [INFO]: | `<Choose a value: 0, 1, 2, 3, 4>` |
| Set 'SEARCH_STRING' (options: a string, or a valid regular expression): | `(?is)(?=.*\b(create)\b)(?=.*\b(procedure)\b)(?!.*\b(grant)\b)(?!.*\b(execute)\b).*` |
| Set 'MESSAGE' [A match for regular expression <SEARCH_STRING> was detected in Changeset <CHANGESET>.]: | `Error! CREATE PROCEDURE statement found without a GRANT EXECUTE statement.` |
| Set 'STRIP_COMMENTS' (options: true, false) [true]: | `true` |
