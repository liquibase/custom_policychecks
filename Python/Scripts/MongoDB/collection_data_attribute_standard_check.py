###
### This script checks scans changesets that are referencing a specified key word, such as 'product' 
### for any any createcollection or modcoll calls. If those functions are not present it exits. 
### If those function calls exist it does check to ensure the data domain key
### identifier is inclued in the required field section and properties section and then checks for 
### additional 
### 
### The example code below is using Product data domain as an example and looking for
### productID in properties and the bsonType is "string" and the MaxLength is set to 15
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
        ##debug print (raw_sql)

        ## Are any validator elements present
        ## and being modified
        createcollection_match = re.search(r'createcollection', raw_sql, re.IGNORECASE)
        collmodcollection_match = re.search(r'collmod', raw_sql, re.IGNORECASE)

        if createcollection_match or collmodcollection_match: 
            #
            # Now find 'properties:' (case-insensitive) section
            ##
            vproperties_pattern = r'(?i:properties)\s*:\s*\{'
            vproperties_match = re.search(vproperties_pattern, raw_sql)
            ##debug print (vproperties_match)

            ## if no properties section bump err_cnt
            if not vproperties_match:
                err_cnt += 1
                break
            else:
                # Search for 'productID:' (case-sensitive) section in properties
                #
                start_pos = vproperties_match.start() -1  # Position after opening brace
                
                # Find the end position where '}}' occurs
                end_pattern = '}\s*}'
                end_pos = raw_sql.find(end_pattern, start_pos)
    
                if end_pos == -1:
                    # If '}}' not found, take rest of content
                    vproperties_content = raw_sql[start_pos:]
                else:
                    # Include the '}}' in the content
                    vproperties_content = raw_sql[start_pos:end_pos + len(end_pattern)]
                ## debug  print (vproperties_content)

                ## search 
                productID_pattern = r'(?i:productID)\s*:\s*\{'
                productID_match = re.search(productID_pattern, vproperties_content)
                ## debug print (productID_match)

            
            # If the productID is not found report error
            #
            if not productID_match:
                liquibase_status.fired = True
                liquibase_status.message = liquibase_utilities.get_script_message()
                err_cnt += 1
                break
            elif productID_match:
                # Search for 'bsonType: "string"' (case-sensitive) entry in productID 
                # section of properties to ensure it will be formatted as string
                start_pos = productID_match.start() -1  # Position after opening brace
                
                # Find the end position where '}' occurs
                end_pattern = '}'
                end_pos = vproperties_content.find(end_pattern, start_pos)
    
                if end_pos == -1:
                    # If '}' not found, take rest of content
                    productID_content = vproperties_content[start_pos:]
                else:
                    # Include the '}}' in the content
                    productID_content = vproperties_content[start_pos:end_pos + len(end_pattern)]   
                ## debug
                print (productID_content)
                
                datatype_pattern = r'bsonType\s*:\s*\"string\"'
                datatype_match = re.search(datatype_pattern, productID_content)
                ##debug 
                print (datatype_match)

                if not datatype_match:
                    liquibase_status.fired = True
                    liquibase_status.message = liquibase_utilities.get_script_message()
                    err_cnt += 1
                    break 
                elif datatype_match:
                    ##debug  print ("datatype match was found checking for maxLength")

                    # Search for 'maxLength: [15,' (case-sensitive) entry in productID section
                    # section of properties to ensure it will not be longer than 15 characters  

                    maxlen_pattern = r'maxLength\s*:\s*\[15,'
                    maxlen_match = re.search(maxlen_pattern, productID_content)
                    
                    ##debug 
                    print (maxlen_match)

                    if not maxlen_match:
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
