###
### This script checks for a validator when creating a new collection
###

###
### Helpers come from Liquibase
###
import sys
import liquibase_database
import liquibase_utilities

###
### Constants
###
NOSQL_DATABASES = ["MongoDB"]

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
### Check for Mongo
###
current_database = liquibase_utilities.get_database()
product_name = liquibase_database.get_short_name(current_database)
if not product_name.casefold() in map(str.casefold, NOSQL_DATABASES):
    liquibase_logger.info(f"Database {product_name} ignored")
    liquibase_status.fired = False
    sys.exit(1)

###
### Retrieve all changes in changeset
###
changes = liquibase_utilities.get_changeset().getChanges()

###
### Loop through all changes
###
for change in changes:
    ###
    ### Retrieve sql as string, remove extra whitespace
    ###
    raw_sql = liquibase_utilities.strip_comments(liquibase_utilities.generate_sql(change)).casefold()
    raw_sql = " ".join(raw_sql.split())

    ###
    ### Look for createCollection
    ###
    if "createcollection" in raw_sql and not "validator:" in raw_sql:
        liquibase_status.fired = True
        liquibase_status.message = liquibase_utilities.get_script_message()
        sys.exit(1)

###
### Default return code
###
False
