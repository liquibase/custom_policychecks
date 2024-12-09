###
### This script ensures the billing mode for new tables is PROVISIONED.
###
### Notes:

###
### Helpers come from Liquibase
###
import sys
import liquibase_utilities

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
### Retrive maximum size from check definition
###
billing_mode = liquibase_utilities.get_arg("BILLING_MODE")
if len(billing_mode) == 0:
    liquibase_logger.error(f"Missing billing mode from check definition.")
    sys.exit(1)

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
    change_type = change.getClass().getSimpleName()
    if change_type.casefold() != "DynamoCreateTableChange".casefold():
        liquibase_logger.info(f"{change_type} changetype skipped.")
        continue
    new_billing_mode = change.getBillingMode()
    if new_billing_mode.casefold() != billing_mode.casefold():
        liquibase_status.fired = True
        liquibase_status.message = str(liquibase_utilities.get_script_message()).replace("__BILLING_MODE__", f"'{billing_mode}'")
        sys.exit(1)

###
### Default return code
###
False