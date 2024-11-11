###
### This script ensures all foreign key names have the pattern FK_<child table>_<parent table>
###
### Notes:
### 1. Only basic CREATE or ALTER statements are supported
### 2. Constraint names must be provided (not auto-generated)
### 3. Only first foreign key name is checked in CREATE statement
###

###
### Helpers come from Liquibase
###
import sys
import liquibase_utilities

###
### Functions
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
        ### CREATE TABLE NAME (column1 type1, column2 type2, ...) CONSTRAINT NAME FOREIGN KEY (column) REFERENCES TABLE (column)
        ### ALTER TABLE NAME ADD CONSTRAINT NAME FOREIGN KEY (column) REFERENCES TABLE (column)
        ###
        try:
            if (sql_list[0] == "create" or sql_list[0] == "alter") and (sql_list[1] == "table"):
                ### Child (current) table name
                table_name_child = sql_list[2].split(".")[-1]
                start = table_name_child.rfind("(")
                if start != -1:
                    table_name_child = table_name_child[0:start]
                ### FK name
                start = sql_list.index("foreign")
                fk_name_current = sql_list[start - 1].split(".")[-1]
                ### Parent table name
                start = sql_list.index("references", start)
                table_name_parent = sql_list[start + 1].split(".")[-1]
                start = table_name_parent.rfind("(")
                if start != -1:
                    table_name_parent = table_name_parent[0:start]
            else:
                raise UserWarning
        except (IndexError, ValueError):
            liquibase_logger.warning(f"Unsupported Create/Alter statement skipped: {raw_statement}")
            continue
        except UserWarning:
            liquibase_logger.info(f"Non Create/Alter statement skipped: {raw_statement}")
            continue
        ###
        ### Compare constraint name to pattern
        ###
        fk_name_standard = f"fk_{table_name_child}_{table_name_parent}"
        if fk_name_standard not in fk_name_current:
            liquibase_status.fired = True
            status_message = str(liquibase_utilities.get_script_message()).replace("__NAME_CURRENT__", f"\"{fk_name_current}\"")
            status_message = status_message.replace("__NAME_STANDARD__", f"\"{fk_name_standard}\"")
            liquibase_status.message = status_message
            sys.exit(1)


###
### Default return code
###
False