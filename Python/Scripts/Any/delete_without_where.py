###
### This script checks for the phrase "DELETE FROM" without "WHERE"
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
    ### Retrieve sql as string, remove extra whitespace
    ###
    raw_sql = liquibase_utilities.strip_comments(liquibase_utilities.generate_sql(change)).casefold()
    raw_sql = " ".join(raw_sql.split())
    ###
    ### Split sql into statements
    ###
    raw_statements = liquibase_utilities.split_statements(raw_sql)
    for raw_statement in raw_statements:
        ###
        ### Get list of token objects, convert to string
        ###
        tokens = liquibase_utilities.tokenize(raw_statement)
        keywords = [str(token) for token in tokens if token.is_keyword or isinstance(token, sqlparse.sql.Where)]
        keywords = [keyword for keyword in " ".join(keywords).split()]
        ###
        ### Look for delete
        ###
        if len(keywords) >= 2 and keywords[0] == "delete" and keywords[1] == "from" and "where" not in keywords:
            liquibase_status.fired = True
            liquibase_status.message = liquibase_utilities.get_script_message()
            sys.exit(1)
###
### Default return code
###
False