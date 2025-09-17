###
### This script checks for raw SSNs in data fixes
###
### Notes:
### 1. This script only checks INSERT and UPDATE statements.

###
### Utilities come from Liquibase
###
import sys
import re
import sqlparse
import liquibase_utilities

###
### Retrieve log handler
### Ex. liquibase_logger.info(message)
###
liquibase_logger = liquibase_utilities.get_logger()

###
### Retrieve status handler
###
liquibase_status = liquibase_utilities.get_status()

###
### Regex pattern for US SSNs
###
SSN_PATTERN = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")

###
### Retrieve all changes in changeset
###
changes = liquibase_utilities.get_changeset().getChanges()

###
### Loop through all changes
###
for change in changes:
    ###
    ### LoadData change types are not currently supported
    ###
    if "loaddatachange" in change.getClass().getSimpleName().lower():
        continue
    ###
    ### Retrieve raw sql
    ###
    sql_text = liquibase_utilities.generate_sql(change)
    ###
    ### Split into statements
    ###
    statements = sqlparse.parse(sql_text)
    for stmt in statements:
        ###
        ### Get the type of SQL statement (INSERT, UPDATE, etc.)
        ###
        stmt_type = stmt.get_type()
        if stmt_type in ("INSERT", "UPDATE"):
            ###
            ### Convert statement to string for regex search
            ###
            stmt_str = str(stmt)
            matches = SSN_PATTERN.findall(stmt_str)
            if matches:
                liquibase_logger.warning(f"Raw SSN detected in {stmt_type} statement: {matches}")
                liquibase_status.fired = True
                liquibase_status.message = f"Raw SSN detected in {stmt_type} statement. Matches: {matches}"
                sys.exit(1)

###
### Default return code
###
False