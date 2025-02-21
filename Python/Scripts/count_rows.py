###
### This script counts rows in a table
###
### Notes:
###

###
### Helpers come from Liquibase
###
import liquibase_utilities
import sys

###
### main
###

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
### Retrieve table from check definition
###
table_name = liquibase_utilities.get_arg("TABLE_NAME")

###
### Build SQL
###
sql_query = f"select count(*) from {table_name};"

###
### Execute SQL - returns a list of dictionaries
###
row_count = liquibase_utilities.query_for_list(sql_query, None, ";")[0]["COUNT"]

###
### Show output
###
liquibase_status.fired = True
status_message = str(liquibase_utilities.get_script_message()).replace("__TABLE_NAME__", f"\"{table_name}\"")
status_message = status_message.replace("__ROW_COUNT__", f"{row_count}")
liquibase_status.message = status_message
sys.exit(1)

###
### Default return code
###
False