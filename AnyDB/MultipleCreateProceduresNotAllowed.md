# MultipleCreateProceduresNotAllowed

Multiple `CREATE PROCEDURE` statements not allowed in a changeset.

regex: `(?is)[\t\r\n\s]*\bcreate\b[\t\r\n\s]+.*\bprocedure\b[\t\r\n\s]+.*[\t\r\n\s]+\bcreate\b[\t\r\n\s]+.*\bprocedure\b[\t\r\n\s]+`

# Sample Failing Scripts
``` sql
--changeset amalik:Procedures_CustOrder
CREATE OR REPLACE PROCEDURE CustOrderHist @CustomerID nchar(5)
AS
SELECT ProductName, Total=SUM(Quantity)
FROM Products P, [Order Details] OD, Orders O, Customers C
WHERE C.CustomerID = @CustomerID
AND C.CustomerID = O.CustomerID AND O.OrderID = OD.OrderID AND OD.ProductID = P.ProductID
GROUP BY ProductName 

CREATE PROCEDURE [dbo].[CustOrdersDetail] @OrderID int
AS
SELECT ProductName,
    UnitPrice=ROUND(Od.UnitPrice, 2),
    Quantity,
    Discount=CONVERT(int, Discount * 100), 
    ExtendedPrice=ROUND(CONVERT(money, Quantity * (1 - Discount) * Od.UnitPrice), 2)
FROM Products P, [Order Details] Od
WHERE Od.ProductID = P.ProductID and Od.OrderID = @OrderID

GRANT EXECUTE ON dbo::CustOrderHist TO AppUser1;  
GRANT EXECUTE ON dbo::CustOrdersDetail TO AppUser1; 
```

# Sample Error Message
```
CHANGELOG CHECKS
----------------
Checks completed validation of the changelog and found the following issues:

Check Name:         Check for specific patterns in sql (MultipleCreateProceduresNotAllowed)
Changeset ID:       Procedures_CustOrder
Changeset Filepath: changeLogs/2_objects/02_storedprocedure/CustOrders.sql
Check Severity:     BLOCKER (Return code: 4)
Message:            Error! Multiple CREATE PROCEDURE statements not allowed in a
                    single changeset. Only a single CREATE PROCEDURE statement
                    is allowed.
```

# Step-by-Step
| Prompt | Command or User Input |
| ------ | ----------------------|
| > | `liquibase checks customize --check-name=SqlUserDefinedPatternCheck` |
| Give your check a short name for easier identification (up to 64 alpha-numeric characters only) [SqlUserDefinedPatternCheck1]: | `MultipleCreateProceduresNotAllowed` |
| Set the Severity to return a code of 0-4 when triggered. (options: 'INFO'=0, 'MINOR'=1, 'MAJOR'=2, 'CRITICAL'=3, 'BLOCKER'=4)? [INFO]: | `<Choose a value: 0, 1, 2, 3, 4>` |
| Set 'SEARCH_STRING' (options: a string, or a valid regular expression): | `(?is)[\t\r\n\s]*\bcreate\b[\t\r\n\s]+.*\bprocedure\b[\t\r\n\s]+.*[\t\r\n\s]+\bcreate\b[\t\r\n\s]+.*\bprocedure\b[\t\r\n\s]+` |
| Set 'MESSAGE' [A match for regular expression <SEARCH_STRING> was detected in Changeset <CHANGESET>.]: | `Error! Multiple CREATE PROCEDURE statements not allowed in a single changeset. Only a single CREATE PROCEDURE statement is allowed.` |
| Set 'STRIP_COMMENTS' (options: true, false) [true]: | `true` |
