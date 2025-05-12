import sys
import liquibase_utilities

#
# This check addresses this MySQL 8.0 issue
# 
# https://www.bytebase.com/blog/fault-in-schema-migration-outage/
#
#

def isMySQL8():
    database = liquibase_utilities.get_database()
    product_name = str(database.getDatabaseProductName())
    version = str(database.getDatabaseProductVersion())
    logger.info("Database version is " + version)
    if product_name != "MySQL" or version.startswith("8.0") == False:
        logger.info("Skipping " + product_name + " version " + version)
        return False
    return True

def table_exists(table_name):
    table = None 
    logger.info("Table name " + table_name)
    tables = snapshot['snapshot']['objects']['liquibase.structure.core.Table']
    for t in tables:
        if table_name == t['table']['name']:
            table = t
            break
    return table

def column_exists(column_name):
    column = None
    columns = snapshot['snapshot']['objects']['liquibase.structure.core.Column']
    for c in columns:
        if column_name == c['column']['name']:
            column = c['column']
            break
    if column != None:
        coltype = column['type']['typeName']
        if column == None or coltype != "VARCHAR": 
            return None
    return column

def statementIsAlterTable(tokens):
    #
    # Make sure the SQL modify statement is of the form
    # ALTER TABLE <table> MODIFY <column> <data type>
    # 
    alter_to_upper = str(tokens[0]).upper()
    table_to_upper = str(tokens[2]).upper()
    modify_to_upper = str(tokens[6]).upper()
    if (alter_to_upper != 'ALTER' or table_to_upper != 'TABLE' or modify_to_upper != 'MODIFY'):
        return False 
    return True

#
# Get the logger handle
#
logger = liquibase_utilities.get_logger()

if not isMySQL8():
    status = liquibase_utilities.get_status()
    status.fired = False
    sys.exit(1)

script_name = liquibase_utilities.get_script_path()
message = "The script name is '" + script_name + "'"
logger.info(message)

#
# Get the JSON snapshot object
#
snapshot = liquibase_utilities.get_snapshot()

#
# Get the SQL
# Split into individual statements
#
changes = liquibase_utilities.get_changeset().getChanges()
for change in changes:
    sql = liquibase_utilities.generate_sql(change)
    sql = liquibase_utilities.strip_comments(sql)
    logger.info("Processing SQL " + sql)
    statements = liquibase_utilities.split_statements(sql)
    for statement in statements:
        #
        # Break into tokens
        #
        tokens = liquibase_utilities.tokenize(statement)
        if not statementIsAlterTable(tokens):
            continue 

        #
        # Make sure the new datatype is VARCHAR
        #
        data_type = str(tokens[10])
        if not data_type.upper().startswith('VARCHAR'):
            continue 

        #
        # Check to see if the table and column exist and the data type is VARCHAR
        #
        table_name = str(tokens[4])
        table = table_exists(table_name)
        if table == None: 
            continue 
        column_name = str(tokens[8])
        column = column_exists(column_name)
        if column == None:
            continue 

        #
        # Check the size
        # If it is out of range then set the status.fired to True and create a message
        #
        col_size_text = column['type']['columnSize'].split('!')[0]
        col_size = int(col_size_text)
        mod_size = data_type.replace("(","").replace(")","").replace("VARCHAR","")
        i_mod_size = int(mod_size)
        if col_size < 256 and i_mod_size >= 256:
            status = liquibase_utilities.get_status()
            status.fired = True
            status.message = liquibase_utilities.get_script_message()
            status.message = status.message.replace("<TABLE_NAME>",table['table']['name'])
            status.message = status.message.replace("<COLUMN_NAME>",column['name'])
            status.message = status.message.replace("<OLD_SIZE>", str(col_size))
            status.message = status.message.replace("<NEW_SIZE>", str(mod_size))
            status.message = status.message.replace("<SQL>", sql)
            if status.message == None:
                status.message = \
                    "Column '" + table_name + "." + column['name'] + \
                    "' has an illegal size modification from '" + str(col_size) + "' to '" + mod_size + "' in SQL %n'" + \
                    sql + "'"
            sys.exit(1)
#
# Fall through to return False
#
False
