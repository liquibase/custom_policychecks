###
### This script ensures all VARCHAR columns are under a maximum size
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
### Retrive maximum size from check definition
###
max_size = int(liquibase_utilities.get_arg("VARCHAR_MAX"))

###
### Retrieve database object
###
database_object = liquibase_utilities.get_database_object()

###
### Skip if not a varchar column
###
if "column" in database_object.getObjectTypeName().lower() and "varchar" in str(database_object.getType()).lower():
    column_name = database_object.getName()
    column_size = int(database_object.getType().getColumnSize())
    if column_size > max_size:
        liquibase_status.fired = True
        status_message = str(liquibase_utilities.get_script_message()).replace("__COLUMN_NAME__", f"'{column_name}'")
        status_message = status_message.replace("__COLUMN_SIZE__", f"{max_size}")
        liquibase_status.message = status_message
        sys.exit(1)

###
### Default return code
###
False