###
### This script checks that the Buffer Pool specified in the tablespace
### matches the default Buffer Pool for the Database.
###
###
### This script throws the following errors:
### 1) Multiple CREATE TABLESPACE statements found in changeset. Only one CREATE TABLESPACE allowed per changeset.
### 2) Default Buffer Pool Not Found for Database {database_name}.
### 3) Multiple BUFFER POOL statements found in CREATE TABLESPACE statement. Only one Buffer Pool can be specified.
### 4) Buffer Pool Not Found in CREATE TABLESPACE script.
### 5) CREATE TABLESPACE Buffer Pool (buffer_name) must match the default Buffer Pool (default_buffer_pool) for the database (database_name).
###
### Sample Tablespace:
###
###  CREATE TABLESPACE SBA01003
###    IN DBA0001
###    USING STOGROUP SYSPOOL1
###    PRIQTY 720 SECQTY 720
###    ERASE  NO
###    FREEPAGE 5 PCTFREE 15 FOR UPDATE 0
###    GBPCACHE CHANGED
###    TRACKMOD YES
###    MAXPARTITIONS 20
###    LOGGED
###    DSSIZE 8 G
###    SEGSIZE 32
###    BUFFERPOOL BP0
###    LOCKSIZE ANY
###    LOCKMAX SYSTEM....
###
### Query to find default Buffer Pool:
### 
### SELECT BPOOL FROM SYSIBM.SYSDATABASE WHERE NAME = 'DBA0001';

###
### Helpers come from Liquibase
###
import liquibase_utilities
import re
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
### Define regex patterns for a Tablespace's DatabaseName and BufferPool
###
regex_pattern_database = f"(?is)CREATE\s+TABLESPACE\s+\w+\s+IN\s+(\w+)"
regex_pattern_bufferpool = f"(?is)BUFFERPOOL\s+(\S+)"

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
    ### Split sql into a list of strings to remove whitespace
    ###
    raw_sql = liquibase_utilities.generate_sql(change)
    
    ###
    ### Look for database regex in SQL
    ###
    database_list = re.findall(regex_pattern_database, raw_sql)
    
    if len(database_list) > 1:
        liquibase_status.fired = True                  
        status_message = f"Multiple CREATE TABLESPACE statements found in changeset. Only one CREATE TABLESPACE allowed per changeset."
        liquibase_status.message = status_message
        sys.exit(1)
        break
    else:
        database_name = ''.join(database_list)
        
        ### 
        ### End check if script does not contain regex pattern
        ###    
        if database_name is None or database_name == '':
            break
        else:
            ### print(f"Database Name: {database_name}")
            
            ###
            ### Execute query to get the default buffer pool for the database
            ###
            sql_query = f"SELECT BPOOL FROM SYSIBM.SYSDATABASE WHERE NAME = '{database_name}'"
            default_buffer_pool_list = liquibase_utilities.query_for_list(sql_query, None, ";")
            
            if len(default_buffer_pool_list) == 0:
                ### print(f"Default Buffer Pool Not Found for Database {database_name}")
                
                liquibase_status.fired = True                  
                status_message = f"Default Buffer Pool Not Found for Database {database_name}."
                liquibase_status.message = status_message
                sys.exit(1)
                break
            else:
            
                default_buffer_pool = default_buffer_pool_list [0]["BPOOL"].strip()
                ### print(f"Default Buffer Pool: {default_buffer_pool}")
                
                ###
                ### Look for bufferpool regex in SQL
                ###
                buffer_pool_list = re.findall(regex_pattern_bufferpool, raw_sql)
                
                if len(buffer_pool_list) > 1:
                    liquibase_status.fired = True                  
                    status_message = f"Multiple BUFFER POOL statements found in CREATE TABLESPACE statement. Only one Buffer Pool can be specified."
                    liquibase_status.message = status_message
                    sys.exit(1)
                    break
                else:
                
                    buffer_pool = ''.join(buffer_pool_list)
                    
                    if buffer_pool is None or buffer_pool == '':
                        ### print(f"Buffer Pool Not Found in script {buffer_pool}")
                       
                        liquibase_status.fired = True                  
                        status_message = f"Buffer Pool Not Found in CREATE TABLESPACE script."
                        liquibase_status.message = status_message
                        sys.exit(1)
                        break
                        
                    else:
                        ### print(f"Buffer Pool in script: {buffer_pool}")
                        
                        ###
                        ### Check that the buffer pool values match
                        ###
                        
                        if buffer_pool != default_buffer_pool:
                            
                            liquibase_status.fired = True                    
                            status_message = str(liquibase_utilities.get_script_message()).replace("__BUFFER_POOL__", f"{buffer_pool}")
                            status_message = status_message.replace("__DEFAULT_BUFFER_POOL__", f"{default_buffer_pool}")
                            status_message = status_message.replace("__DATABASE_NAME__", f"{database_name}")
                            liquibase_status.message = status_message
                            sys.exit(1)
                            break

###
### Default return code
###
False