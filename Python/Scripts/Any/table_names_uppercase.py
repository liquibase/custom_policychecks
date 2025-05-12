###
### This script checks for uppercase table names during creation
###
### Notes:
### 1. Only basic CREATE statements are supported

###
### Helpers come from Liquibase
###
import sys
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
    ### Split sql into a list of strings to remove whitespace
    ###
    sql_list = liquibase_utilities.generate_sql(change).split()
    ###
    ### Locate create (or replace) table in list
    ###
    if "create" in map(str.casefold, sql_list) and "table" in map(str.casefold, sql_list):
        index_table = [token.lower() for token in sql_list].index("table")
        if index_table + 1 < len(sql_list):
            table_name = sql_list[index_table + 1]
            if not table_name.isupper():
                liquibase_status.fired = True
                status_message = str(liquibase_utilities.get_script_message()).replace("__TABLE_NAME__", f"\"{table_name}\"")
                liquibase_status.message = status_message
                sys.exit(1)

###
### Default return code
###
False