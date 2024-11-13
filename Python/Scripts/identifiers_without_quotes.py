###
### This script checks for quotes in identifier names
###
### Notes:
###

###
### Helpers come from Liquibase
###
import liquibase_utilities
import sqlparse
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
        liquibase_logger.info("LoadData change type not supported. Statement skipped.")
        continue
    ###
    ### Retrieve sql as string, remove extra whitespace
    ###
    raw_sql = liquibase_utilities.strip_comments(liquibase_utilities.generate_sql(change))
    raw_sql = " ".join(raw_sql.split())
    ###
    ### Split sql into statements
    ###
    raw_statements = liquibase_utilities.split_statements(raw_sql)
    for raw_statement in raw_statements:
        # Get list of token objects
        tokens = liquibase_utilities.tokenize(raw_statement)
        identifiers = [str(token) for token in tokens if isinstance(token, sqlparse.sql.Identifier)]
        # Check each string for quotes
        for identifier in identifiers:
            if "\"" in identifier:
                liquibase_status.fired = True
                status_message = str(liquibase_utilities.get_script_message()).replace("__ID_NAME__", identifier)
                liquibase_status.message = status_message
                sys.exit(1)

###
### Default return code
###
False