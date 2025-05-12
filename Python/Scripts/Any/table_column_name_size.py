###
### This script ensures all tables and column names are under a maximum size
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
### Retrive maximum size from check definition
###
max_size = int(liquibase_utilities.get_arg("MAX_SIZE"))

###
### Check column and table names
###
if liquibase_utilities.is_column(database_object) or liquibase_utilities.is_table(database_object):
    object_name = database_object.getName()
    object_type = database_object.getObjectTypeName()
else:
    liquibase_status.fired = False
    liquibase_logger.info("Object not table or column. Check skipped.")
    sys.exit(1)

###
### Check size
###
if len(object_name) > max_size:
    liquibase_status.fired = True
    status_message = str(liquibase_utilities.get_script_message()).replace("__OBJECT_TYPE__", object_type)
    status_message = status_message.replace("__OBJECT_NAME__", f"\"{object_name}\"")
    status_message = status_message.replace("__CURRENT_SIZE__", str(len(object_name)))
    liquibase_status.message = status_message
    sys.exit(1)

###
### Default return code
###
False