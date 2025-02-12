###
### This script checks ensures that all columns of a specified type include a postfix
### e.g., timestamp columns must include _ts at the end
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
### Retrive column information from check definition
###
column_check = liquibase_utilities.get_arg("COLUMN_TYPE").casefold()
column_postfix = liquibase_utilities.get_arg("COLUMN_POSTFIX").casefold()

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
    ### Retrieve sql as string, remove extra whitespace, split into statements
    ###
    raw_sql = liquibase_utilities.strip_comments(liquibase_utilities.generate_sql(change)).casefold()
    raw_sql = " ".join(raw_sql.split())
    raw_statements = liquibase_utilities.split_statements(raw_sql)
    ###
    ### Process each statement
    ###
    for raw_statement in raw_statements:
        column_list_detail = []
        is_create, is_table = False, False
        token_list = [token for token in liquibase_utilities.tokenize(raw_statement) if not token.is_whitespace]
        for token in token_list:
            if token.ttype == sqlparse.tokens.DDL and token.value == "create":
                is_create = True
            elif is_create and token.ttype == sqlparse.tokens.Keyword and token.value == "table":
                is_table = True
            elif is_create and is_table and token.value.startswith("("):
                columns = token.value[1:token.value.rfind(")")].replace("\n","").split(",")
                for column in columns:
                    column_list_detail.append(' '.join(column.split()).split())
                break
        if (is_create == False or is_table == False):
            liquibase_logger.info(f"Non create table statement skipped: {raw_statement}")
            continue
        ###
        ### Process column list
        ###
        postfix_len = len(column_postfix)
        for column in column_list_detail:
            column_name = column[0].replace("\"","")
            column_type = column[1]
            if column_type == column_check and column_name[-postfix_len:] != column_postfix:
                liquibase_status.fired = True
                status_message = str(liquibase_utilities.get_script_message()).replace("__COLUMN_NAME__", f"\"{column_name}\"")
                status_message = status_message.replace("__COLUMN_POSTFIX__", f"\"{column_postfix}\"")
                liquibase_status.message = status_message
                sys.exit(1)

###
### Default return code
###
False