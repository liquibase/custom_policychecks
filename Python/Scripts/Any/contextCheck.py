###
### This script ensures all context values must be INT or INT,UAT or INT,UAT,PRD (case insensitive)
###

###
### Helpers come from Liquibase
###
import sys
import liquibase_utilities, liquibase_changesets
import re

###
### function: is_subset_of_strings
###
def is_subset_of_strings(main_list):
    """
    Checks if all strings in subset_list are present in main_list.

    Args:
        main_list (list): The list of strings to check against.
        subset_list (list): The list of strings to check for presence.

    Returns:
        bool: True if all strings in subset_list are in main_list, False otherwise.
    """

    INT_list = ["int"]
    INT_UAT_list = ["int", "uat"]
    INT_UAT_PRD_list = ["int", "uat", "prd"]

    match len(main_list):
        case 1:
            # print ("Length: " + str(len(main_list)) + " main_list: " + str(main_list) + ", context list: " + str(INT_list))
            return all(item in main_list for item in INT_list)
        case 2:
            # print ("Length: " + str(len(main_list)) + " main_list: " + str(main_list) + ", context list: " + str(INT_UAT_list))
            return all(item in main_list for item in INT_UAT_list)
        case 3:
            # print ("Length: " + str(len(main_list)) + " main_list: " + str(main_list) + ", context list: " + str(INT_UAT_PRD_list))
            return all(item in main_list for item in INT_UAT_PRD_list)
        case _:
            return False

###
### Retrieve log handler
###
liquibase_logger = liquibase_utilities.get_logger()

###
### Retrieve status handler
###
liquibase_status = liquibase_utilities.get_status()

id = liquibase_changesets.get_id(liquibase_utilities.get_changeset())
author = liquibase_changesets.get_author(liquibase_utilities.get_changeset())

## Obtain all contexts in a list
contexts_found_list = list(liquibase_changesets.get_contexts(liquibase_utilities.get_changeset()))

context_correct = is_subset_of_strings(contexts_found_list)

context_string = ",".join(contexts_found_list)

if not (context_correct):

    liquibase_status.fired = True
    status_message = "The context \"" + context_string + "\" does not include \"int\" or \"int,uat\" or \"int,uat,prd\"."
    liquibase_status.message = status_message
    sys.exit(1)


###
### Default return code
###
False