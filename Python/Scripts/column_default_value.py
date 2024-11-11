###
### This script ensures new columns do not have default values explicity listed
###
### Notes:
### 1. Only basic ALTER table statements are supported
### 2. Single and multiple columns in an alter statement *are* supported
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
        ### Split raw_statement into list, look for alter table, remove schema if provided
        ###
        sql_list = raw_statement.split()
        try:
            if sql_list[0] == "alter" and sql_list[1] == "table" and sql_list[3] == "add":
                ### Table name
                table_name = sql_list[2].split(".")[-1]
                start = table_name.rfind("(")
                if start != -1:
                    table_name = table_name[0:start]
            else:
                raise UserWarning
        except (IndexError, ValueError):
            liquibase_logger.warning(f"Unsupported Alter statement skipped: {raw_statement}")
            continue
        except UserWarning:
            liquibase_logger.info(f"Non Alter statement skipped: {raw_statement}")
            continue
        ###
        ### ALTER
        ###
        found = False
        search_string = " add ("
        start = raw_statement.find(search_string)
        ###
        ### ALTER TABLE NAME ADD column type [DEFAULT value]
        ###
        if start == -1:
            if raw_statement.find("default") != -1:
                found = True
                column_name = sql_list[4]
        ###
        ### ALTER TABLE NAME ADD (column1 type1 [DEFAULT value1], column2 type2, [DEFAULT value2], ...)
        ###
        else:
            start += len(search_string)
            end = raw_statement.rfind(")")
            if end != -1:
                column_list = raw_statement[start:end].split(",")
                for column in column_list:
                    if "default" in column:
                        found = True
                        column_name = column.split()[0].strip()
        ###
        ### Report matches
        ###
        if found == True:
            liquibase_status.fired = True
            status_message = str(liquibase_utilities.get_script_message()).replace("__COLUMN_NAME__", f"\"{column_name}\"")
            status_message = status_message.replace("__TABLE_NAME__", f"\"{table_name}\"")
            liquibase_status.message = status_message
            sys.exit(1)

###
### Default return code
###
False