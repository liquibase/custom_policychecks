###
### This script checks for PascalCase collection names during createCollection
###
### Notes:
### 1. Only basic createCollection statements are supported

###
### Helpers come from Liquibase
###
###
### This script requires the use of Python virtual environment documented here:
### https://docs.liquibase.com/liquibase-pro/policy-checks/custom-policy-checks/python-virtual-environment.html
###

from liquibase_checks_python import liquibase_utilities as lb
import re
import sys
import wordninja

def extract_table_names(content):
    """Extract table names from CREATE TABLE content in SQL file."""
    table_names = []
            
    # Regular expression to match CREATE TABLE statements
    # Matches both [dbo].[TableName] and dbo.TableName formats
    pattern = r'CREATE\s+TABLE\s+(?:\[?dbo\]?\.)?\[?(\w+)\]?'
    
    matches = re.findall(pattern, content, re.IGNORECASE)
    table_names.extend(matches)
            
    return table_names


def find_dictionary_words(input_data):
    """
    Check which words are English dictionary words.
    
    Args:
        input_data:A mixed case string (e.g., "ToDoItem" or "todoItem")
        
    Returns:
        String: dictionary_words
        
    Examples:
        wordninja.split("toDoitem")
    """

    dictionary_words = []

    # Handle string input - split into words first
    dictionary_words = wordninja.split(input_data)
    
    return dictionary_words


def is_pascal_case(input_data):
    """
    Checks if a string is in Pascal Case.

    A string is considered Pascal Case if it:
    - First charater is upper case, all other characters lower case.
    - Does not start with a number.

    Args:
        input_data: A list of strings to check.

    Returns:
        True if the string is in Pascal Case, False otherwise.
    """

    pascal_case_found = True

    for word in input_data:

        # print ("word :" + word)

        if re.match(r"^[A-Z][a-z]*$", word):
            pascal_case_found = pascal_case_found and True
            # return True
        else:
            pascal_case_found = pascal_case_found and False

        if word[0].isdigit():
            # return False
            pascal_case_found = pascal_case_found and False

        print ("word :" + word + ", " + str(pascal_case_found))    

    return pascal_case_found

###
### Retrieve log handler
### Ex. liquibase_logger.info(message)
###
# liquibase_logger = liquibase_utilities.get_logger()
liquibase_logger = lb.get_logger()

###
### Retrieve status handler
###
# liquibase_status = liquibase_utilities.get_status()
liquibase_status = lb.get_status()

###
### Retrieve all changes in changeset
###
# changes = liquibase_utilities.get_changeset().getChanges()
changes = lb.get_changeset().getChanges()

###
### Loop through all changes
###
for change in changes:
    ###
    ###
    ### Split SQL into a list of strings to remove whitespace
    ###
    # sql_list = liquibase_utilities.generate_sql(change).split()
    # print ("sql_list:" + str(sql_list))

    table_names_list = []

    ### 
    ### Send the SQL to extract_table_names(string)
    ###
    # table_names_list = extract_table_names( liquibase_utilities.generate_sql(change) )
    table_names_list = extract_table_names( lb.generate_sql(change) )
    print ("table name:" + str(table_names_list))

    for table_name in table_names_list:
        
        dictionary_words = []

        dictionary_words = find_dictionary_words(table_name)
        print("Dictionary words: " + str(dictionary_words))

        isPascalCase = is_pascal_case(dictionary_words)
        print ("Table name: " + table_name + ", " + str(isPascalCase))

        if not isPascalCase:
            liquibase_status.fired = True
            status_message = "Table name \"" + f"{table_name}" + "\" is NOT PascalCase."
            liquibase_status.message = status_message
            sys.exit(1)

False