###
### This script tests arguments with quotes
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
### Retrive string from check definition
###
input_str = liquibase_utilities.get_arg("STR_VALUE")

###
### Display message
###
print(input_str)

###
### Default return code
###
False