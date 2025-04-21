###
### This script checks for camelCase collection names during createCollection
###
### Notes:
### 1. Only basic createCollection statements are supported

###
### Helpers come from Liquibase
###
import re
import sys
import liquibase_utilities


def find_substring_indices(string_list, substring):
    """
    Finds the indices of list elements containing a specified substring.

    Args:
        string_list: A list of strings.
        substring: The substring to search for.

    Returns:
        A list of indices where the substring is found, or an empty list if not found.
    """
    return [index for index, string in enumerate(string_list) if substring in string.casefold()]

def is_camel_case(input_string):
    """
    Checks if a string is in camel case.

    A string is considered camel case if it:
    - Contains only letters (a-z, A-Z) and optionally numbers (0-9).
    - Contains both lowercase and uppercase letters.
    - Does not start with a number.

    Args:
        input_string: The string to check.

    Returns:
        True if the string is in camel case, False otherwise.
    """
    if not isinstance(input_string, str):
        return False

    if not re.match(r"^[a-zA-Z][a-zA-Z0-9]*$", input_string):
        return False

    if input_string[0].isdigit():
        return False
    
    if not any(char.islower() for char in input_string) or not any(char.isupper() for char in input_string):
      return False

    return True

def extract_substring(text, start_char, end_char):
    """
    Extracts the substring between the first occurrence of start_char and end_char in text.

    Args:
        text: The string to search within.
        start_char: The character marking the beginning of the substring.
        end_char: The character marking the end of the substring.

    Returns:
        The extracted substring, or an empty string if start_char or end_char are not found,
        or if end_char appears before start_char.
    """
    try:
        start_index = text.index(start_char) + 1
        end_index = text.index(end_char, start_index)
        return text[start_index:end_index]
    except ValueError:
        return ""


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
    ###
    ### Split mongo code into a list of strings to remove whitespace
    ###
    js_list = liquibase_utilities.generate_sql(change).split()
    # print (list(js_list))
    ###
    ### Locate createCollection in list
    ###

    if any("createcollection" in element for element in map(str.casefold, js_list)):

        ### Get all indexes consisting of "createCollection", irrelevant of case
        ### Returns indices as list
        indices = find_substring_indices(js_list, "createcollection")

        for index in indices:
            collection = js_list[index]

            ### Look for collection name in this format: 
            ### db.createCollection('collectionName');
            collectionName = extract_substring (collection, "'", "'")

            ### Account for spaces like this:
            ### db.createCollection( 'collectionName');
            if not collectionName:
                collectionName = extract_substring (js_list[index+1], "'", "'")

            isCamelCase = is_camel_case(collectionName)
            print ("index=" + str(index) + ", " + str(collection) + ", ", str(collectionName) + ", ", str(isCamelCase))

            if not isCamelCase:
                liquibase_status.fired = True
                status_message = "Collection name \"" + f"{collectionName}" + "\" is NOT camelCase."
                liquibase_status.message = status_message
                sys.exit(1)

###
### Default return code
###
False