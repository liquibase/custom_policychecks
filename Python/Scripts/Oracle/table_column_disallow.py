###
### This script checks for DATA_TYPE columns when creating tables
###
### Notes:
### 1. Only basic CREATE statements are supported
###

###
### Helpers come from Liquibase
###
import liquibase_utilities
import sys

###
### Functions
###
def find_snapshot_object(object_list, type, key, value):
    """Returns a snapshot object given a key (e.g., name) and attribute."""
    for object in object_list:
        if object[type][key].lower() == value.lower():
            return object
    return None

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
### Retrive datatype from check definition
###
data_type = liquibase_utilities.get_arg("DATA_TYPE").lower()

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
        sql_list = raw_statement.split()
        ###
        ### CREATE [SCHEMA.]TABLE NAME (column1 datatype1, column2 datatype2, ...)
        ###
        try:
            if sql_list[0] == "create" and sql_list[1] == "table":
                ###
                ### Remove schema and parenthesis if provided
                ###
                table_name = sql_list[2].split(".")[-1]
                start = table_name.rfind("(")
                if start != -1:
                    table_name = table_name[0:start]
            else:
                raise UserWarning
        except IndexError:
            liquibase_logger.warning(f"Unsupported Create Table statement skipped: {raw_statement}")
            continue
        except UserWarning:
            liquibase_logger.info(f"Non Create Index statement skipped: {raw_statement}")
            continue
        ###
        ### Process column list
        ###
        column_list = []
        search_string = f"{table_name} ("
        start = raw_statement.find(search_string)
        if start == -1:
            liquibase_logger.warning(f"Unsupported Create Table statement skipped: {raw_statement}")
            continue
        start += len(search_string)
        end = raw_statement.rfind(")")
        if end != -1:
            column_list = [column_type.strip() for column_type in raw_statement[start:end].split(",")]
        ###
        ### Look for data_type in column list
        ###
        data_type_size = len(data_type)
        for name_type in column_list:
            column_type = name_type.split()[:2]
            if len(column_type) < 2 or column_type[0] == "constraint":
                continue
            column_name = column_type[0]
            column_type = column_type[1]
            if column_type[0:data_type_size] == data_type:            
                liquibase_status.fired = True
                status_message = str(liquibase_utilities.get_script_message()).replace("__COLUMN_TYPE__", f"\"{data_type}\"")
                status_message = status_message.replace("__COLUMN_NAME__", f"\"{column_name}\"")
                liquibase_status.message = status_message
                sys.exit(1)

###
### Default return code
###
False
