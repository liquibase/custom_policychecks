###
### This script ensures all primary key indexes have a tablespace explicitly defined
###
### Notes:
### 1. Only basic CREATE or ALTER statements are supported
### 2. Constraint names must be provided (not auto-generated)
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
        ### Split raw_statement into list, look for create/alter table, remove schema if provided
        ###
        sql_list = raw_statement.split()
        ###
        ### CREATE TABLE NAME (column1 type1, column2 type2, ...) CONSTRAINT NAME PRIMARY KEY (column) USING INDEX TABLESPACE NAME
        ### ALTER TABLE NAME ADD CONSTRAINT NAME PRIMARY KEY (column) USING INDEX TABLESPACE NAME
        ###
        try:
            if (sql_list[0] == "create" or sql_list[0] == "alter") and (sql_list[1] == "table"):
                ### Table name
                table_name = sql_list[2].split(".")[-1]
                start = table_name.rfind("(")
                if start != -1:
                    table_name = table_name[0:start]
                ### PK name
                start = sql_list.index("primary")
                pk_name = sql_list[start - 1].split(".")[-1]
                ### Tablespace
                if (start + 4 >= len(sql_list)) or (sql_list[start + 4] != "tablespace" and sql_list[start + 5] != "tablespace"):
                    liquibase_status.fired = True
                    status_message = str(liquibase_utilities.get_script_message()).replace("__PK_NAME__", f"\"{pk_name}\"")
                    liquibase_status.message = status_message
                    sys.exit(1)
            else:
                raise UserWarning
        except (IndexError, ValueError):
            liquibase_logger.warning(f"Unsupported Create/Alter statement skipped: {raw_statement}")
            continue
        except UserWarning:
            liquibase_logger.info(f"Non Create/Alter statement skipped: {raw_statement}")
            continue

###
### Default return code
###
False