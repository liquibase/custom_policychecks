###
### This script checks scans changesets that are referencing a specified key word, such as 'product' 
## for any any createcollection or modcoll calls. If those are not present it exits. 
### If those function calls exist it does check to ensure the data domain key
###  identifier is inclued in the required field section of the associated 
### collection validator.
### 
### The example code below is using Product data domain as an example and looking for
### productID
###
### This will fail is there is no validator, no required field section in the validator or
### if a field called productID is not in the required fields.
###

###
### Helpers come from Liquibase
###
import sys
import liquibase_database
import liquibase_utilities
import json
import re

###
### Constants
###
NOSQL_DATABASES = ["MongoDB"]

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
### Check for Mongo
###
current_database = liquibase_utilities.get_database()
product_name = liquibase_database.get_short_name(current_database)
if not product_name.casefold() in map(str.casefold, NOSQL_DATABASES):
    liquibase_logger.info(f"Database {product_name} ignored")
    liquibase_status.fired = False
    sys.exit(1)

###
### Retrieve all changes in changeset
###
changes = liquibase_utilities.get_changeset().getChanges()

###
### Loop through all changes
###
err_cnt = 0
for change in changes:
    ###
    ### Retrieve sql as string, remove extra whitespace
    ###
    raw_sql = liquibase_utilities.strip_comments(liquibase_utilities.generate_sql(change))
    raw_sql = " ".join(raw_sql.split())
    
    ###
    ### Look for reference to 'product' related script if not present exit
    ###
    if "product" in raw_sql:
        ###
        ### Look for reference to 'productID' related script without including required field 'productID'
        ###
        ## debug print (raw_sql)
        ## Are any validator elements present
        ## and being modified
        createcollection_match = re.search(r'createcollection', raw_sql, re.IGNORECASE)
        collmodcollection_match = re.search(r'collmod', raw_sql, re.IGNORECASE)

        if createcollection_match or collmodcollection_match: 
            # Find required: section to make sure 'ProductID' is included
            required_pattern = r'(?i:required)\s*:\s*\['
            required_match = re.search(required_pattern, raw_sql.lower())
            ## debug print (required_match)
            #
            ## if no required section bump err_cnt
            if not required_match:
                err_cnt += 1
                break
            else:
                # Search for 'productID:' (case-sensitive) in required field list
                #
                start_pos = required_match.end() - 1   # Position of opening brace
                
                # Find the end position where ']' occurs
                end_pattern = ']'
                end_pos = raw_sql.find(end_pattern, start_pos)
    
                if end_pos == -1:
                    # If ']' not found, take rest of content
                    required_content = raw_sql[start_pos:]
                else:
                    # Include the ']' in the content
                    required_content = raw_sql[start_pos:end_pos + len(end_pattern)]
                    ##debug print(required_content)
                    
                    prodID_chk = re.search(r'productID', required_content)
                    ##debug  print(prodID_chk)

            
                # If the productID is not found in required fields, report error
                #
                if not prodID_chk:
                    liquibase_status.fired = True
                    liquibase_status.message = liquibase_utilities.get_script_message()
                    err_cnt += 1
                    break    

if err_cnt != 0:
    liquibase_status.fired = True
    liquibase_status.message = liquibase_utilities.get_script_message()
    sys.exit(1)

        
###
### Default return code
###
False
