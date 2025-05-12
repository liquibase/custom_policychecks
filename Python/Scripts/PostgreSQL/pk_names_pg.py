###
### This script ensures all primary key names have the pattern tablename_pkey.
### Sakila database
###

###
### Script helper comes from jar
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
if "table" in database_object.getObjectTypeName().lower():
    pk_object = database_object.getPrimaryKey()
    ###
    ### Skip if table doesn't have PK
    ###
    if pk_object != None:
        table_name = database_object.getName()
        pk_name_current = pk_object.getName()
        # pk_standard = liquibase_utilities.get_arg("STANDARD")
        # pk_name_standard = f"{table_name}_{pk_standard}"
        pk_name_standard = f"{table_name}_" + liquibase_utilities.get_arg("STANDARD")
        # pk_name_standard = f"{table_name}_pk"
        print("Standard: " + pk_name_standard + " Current: " + pk_name_current ) 
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