###
### This script ensures a table has less than x indexes
###
### Notes:
### 1. Uses liquibase_utilities cache to aggregate index totals across changesets
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
### Retrieve JSON snapshot
###
liquibase_snapshot = liquibase_utilities.get_snapshot()

###
### Exit if table data is missing
###
if "liquibase.structure.core.Table" not in liquibase_snapshot["snapshot"]["objects"]:
    liquibase_status.fired = False
    liquibase_logger.warning("Table data missing from snapshot. Check skipped.")
    sys.exit(1)

###
### Retrieve columns and tables from snapshot
###
all_tables = liquibase_snapshot["snapshot"]["objects"]["liquibase.structure.core.Table"]

###
### Retrive maximum size from check definition
###
max_index = int(liquibase_utilities.get_arg("MAX_INDEX"))

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
    raw_sql = liquibase_utilities.strip_comments(liquibase_utilities.generate_sql(change)).casefold()
    raw_sql = " ".join(raw_sql.split())
    ###
    ### Split raw_sql into statements
    ###
    raw_statements = liquibase_utilities.split_statements(raw_sql)
    for raw_statement in raw_statements:
        ###
        ### Split raw_statement into list
        ###
        sql_list = raw_statement.split()
        ###
        ### CREATE [UNIQUE] INDEX NAME ON [SCHEMA.]TABLE (column1, column2, ...)
        ###
        try:
            if (sql_list[0] == "create") and (sql_list[1] == "index" or sql_list[2] == "index"):
                start = sql_list.index("on")
                ###
                ### Remove schema and parenthesis if provided
                ###
                table_name = sql_list[start + 1].split(".")[-1]
                start = table_name.rfind("(")
                if start != -1:
                    table_name = table_name[0:start]
            else:
                raise UserWarning
        except (IndexError, ValueError):
            liquibase_logger.warning(f"Unsupported Create Index statement skipped: {raw_statement}")
            continue
        except UserWarning:
            liquibase_logger.info(f"Non Create Index statement skipped: {raw_statement}")
            continue
        ###
        ### Locate table
        ###
        table_object = find_snapshot_object(all_tables, "table", "name", table_name.strip())
        if table_object is None:
            liquibase_logger.warning(f"Table \"{table_name}\" not found in snapshot. Statement skipped.")
            continue
        table_name = table_object['table']['name']
        ###
        ### Sum indexes, check for maximum
        ###
        index_total = liquibase_utilities.get_cache(table_name, 1)
        if "indexes" in table_object["table"]:
            index_total += len(table_object["table"]["indexes"])
        liquibase_utilities.put_cache(table_name, index_total)
        if index_total > max_index:
            liquibase_status.fired = True
            status_message = str(liquibase_utilities.get_script_message()).replace("__TABLE_NAME__", f"\"{table_name}\"")
            status_message = status_message.replace("__INDEX_COUNT__", str(index_total))
            liquibase_status.message = status_message
            sys.exit(1)

###
### Default return code
###
False
