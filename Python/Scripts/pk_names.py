###
### This script ensures all primary key names have the pattern PK_tablename
###
### Notes:
###

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
### Retrieve database object
###
database_object = liquibase_utilities.get_database_object()

###
### Skip if not a table
###
if liquibase_utilities.is_table(database_object):
    table_name = database_object.getName()
    pk_object = database_object.getPrimaryKey()
    ###
    ### Skip if table doesn't have PK
    ###
    if pk_object is None:
        liquibase_logger.info(f"Table \"{table_name}\" does not have a primary key. Check skipped.")
    else:
        pk_name_current = pk_object.getName()
        pk_name_standard = f"PK_{table_name}"
        if pk_name_standard not in pk_name_current:
            liquibase_status.fired = True
            status_message = str(liquibase_utilities.get_script_message()).replace("__CURRENT_NAME__", f"\"{pk_name_current}\"")
            status_message = status_message.replace("__NAME_STANDARD__", f"\"{pk_name_standard}\"")
            liquibase_status.message = status_message
            sys.exit(1)

###
### Default return code
###
False