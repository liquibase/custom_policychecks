###
### This script checks database objects for char data types
###
### Notes:

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
### Skip if not a column
###
if liquibase_utilities.is_column(database_object):
    column_name = database_object.getName()
    column_type = liquibase_utilities.get_column_type(database_object)
    if column_type is None:
        liquibase_logger.info(f"Column \"{column_name}\" has unknown type. Check skipped.")
    else:
        column_type_name = str(column_type)
        end = column_type_name.find("(")
        if end != -1:
            column_type_name = column_type_name[0:end]
        if column_type_name.lower() == "char":
            liquibase_status.fired = True
            status_message = str(liquibase_utilities.get_script_message()).replace("__COLUMN_NAME__", f"\"{column_name}\"")
            liquibase_status.message = status_message
            sys.exit(1)

###
### Default return code
###
False