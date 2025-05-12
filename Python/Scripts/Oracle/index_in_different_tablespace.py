###
### This script ensures an index is created
### in a different tablespace than table
### Limitations:
### Table must exist, if table is created in a prior changeset TBD
### Does not check for schema included in names i.e. schema.table



###
### Script helper comes from Liquibase
###
import liquibase_utilities
import sys
import sqlparse

###
### Functions
###

### Check sql statement for the tablename to create the index on
def get_tablename(sql_tokens):
    for idx, sql_token in enumerate(sql_tokens):
        if sql_token == "on":
            return sql_tokens[idx+1]

### Check if a table exists in the database
### Requires a snapshot to be taken as part of the check
def table_exists(table_name):
    table = None 
    liquibase_logger.info("Table name " + table_name)
    tables = liquibase_snapshot['snapshot']['objects']['liquibase.structure.core.Table']
    for t in tables:
        if table_name.upper() == t['table']['name']:
            table = t
            break
    return table

### This function assumes table exists in snapshot

def get_tablespace_for_table_from_snapshot(table_name):
    tablespace = "DEFAULT"
    tables = liquibase_snapshot['snapshot']['objects']['liquibase.structure.core.Table']
    for table in tables:
        if table_name.upper() == table['table']['name']:
            tablespace = table['table']['tablespace']
            break
    return tablespace

### This function gets the index name from the sql tokens
def get_indexname_from_sql(sql_tokens):
    for idx_idx, indexname in enumerate(sql_tokens):
        if "index" == indexname:
            return sql_tokens[idx_idx + 1]
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
    # print(f"{raw_sql}")
    ###
    ### Split sql into statements
    ###
    raw_statements = liquibase_utilities.split_statements(raw_sql)
    for raw_statement in raw_statements:
        # Get list of sql tokens
        tokens = raw_statement.split()
        # print(f"T0: {tokens[0]}")
        # print(f"T1: {tokens[1]}")
        if tokens[0] == "create":
            # this could be a create index or create unique index statement tokens
            # print(f"TOKEN1: {tokens[1]}")
            # print(f"TOKEN2: {tokens[2]}")
            if tokens[1] == "index" or tokens[2] == "index":
                # Look for table name
                table_name = get_tablename(tokens)
                # Look for tablespace in snapshot
                s_tablespace = get_tablespace_for_table_from_snapshot(table_name)
                # Look for index name in sql statement
                index_name = get_indexname_from_sql(tokens)
                # Look for tablespace in sql_statement
                found_tablespace = raw_statement.rfind("tablespace")
                # print(f"TB: {found_tablespace}")
                #If no tablespace found then it will default to same tablespace so error
                if found_tablespace == -1:
                    liquibase_status.fired = True
                    status_message = str(liquibase_utilities.get_script_message()).replace("__INDEX_NAME__", f"\"{index_name}\"")
                    status_message = status_message.replace("__TABLE_NAME__",f"{table_name}")
                    status_message = status_message.replace("__TABLE_SPACE__",f"{s_tablespace}")
                    liquibase_status.message = status_message
                    sys.exit(1)
                # If defined tablespace, it must not be same as table
                else:
                    #Found a tablespace token in sql statement
                    for tkidx, tk in enumerate(tokens):
                        if tk == "tablespace":
                            # Tablespace name is the next token so use it
                            tbspace = tokens[tkidx+1]
                            #If endswith semicolon, remove it
                            if tbspace.endswith(';'):
                                tbspace = tbspace.rstrip(';')
                            #If quotes around tablespace remove them
                            if tbspace.startswith('"') and tbspace.endswith('"'):
                                tbspace = tbspace[1:-1]
                            # Now check to see if the tablespaces are equal
                            # if the tablespaces are equal then that's a no-no
                            # print(f"DB tbs: {s_tablespace} SQL tbs: {tbspace}")
                            if tbspace.lower() == s_tablespace.lower():
                                liquibase_status.fired = True
                                status_message = str(liquibase_utilities.get_script_message()).replace("__INDEX_NAME__", f"\"{index_name}\"")
                                status_message = status_message.replace("__TABLE_NAME__",f"{table_name}")
                                status_message = status_message.replace("__TABLE_SPACE__",f"{s_tablespace}")
                                liquibase_status.message = status_message
                                sys.exit(1)
###
### Default return code
###
False
