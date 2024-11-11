###
### This script ensures only changes using current schema are allowed
###
### Notes:
### 1. Only checks for schemas available in snapshot
###

###
### Helpers come from Liquibase
###
import sys
import liquibase_database
import liquibase_utilities

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
### Exit if schema data is missing
###
if not "liquibase.structure.core.Schema" in liquibase_snapshot["snapshot"]["objects"]:
    liquibase_status.fired = False
    liquibase_logger.warning("Schema data missing from snapshot. Check skipped.")
    sys.exit(1)

###
### Retrieve schemas from snapshot
###
all_schemas = liquibase_snapshot["snapshot"]["objects"]["liquibase.structure.core.Schema"]

###
### Retrieve current schema name, remove from all_schemas
###
current_schema = liquibase_database.get_default_schema_name(liquibase_utilities.get_database())
current_schema_object = find_snapshot_object(all_schemas, "schema", "name", current_schema)
if current_schema_object != None:
    all_schemas.remove(current_schema_object)

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
    ### Split sql into statements
    ###
    raw_statements = liquibase_utilities.split_statements(raw_sql)
    for raw_statement in raw_statements:
        ###
        ### Split raw_statement into list
        ###
        sql_list = raw_statement.split()
        ###
        ### Check for schemas from snapshot
        ###
        for schema in all_schemas:
            if schema in sql_list:
                liquibase_status.fired = True
                status_message = str(liquibase_utilities.get_script_message()).replace("__SCHEMA_NAME__", f"\"{current_schema}\"")
                liquibase_status.message = status_message
                sys.exit(1)

###
### Default return code
###
False