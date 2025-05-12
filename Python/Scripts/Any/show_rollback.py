###
### This script displays rollback scripts on changesets
###
### Notes:
### 1. liquibase checks run --check-rollbacks

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
### Deployment SQL
###
deploy_changes = liquibase_utilities.get_changeset().getChanges()

###
### Deployment or rollback SQL
###
working_changes = liquibase_utilities.get_changes()

###
### If deploy != working we are looking at rollback SQL
###
if len(deploy_changes) == 0 or len(working_changes) == 0:
    print(f"List is empty, skipping")
else:
    if not deploy_changes[0].equals(working_changes[0]):
        raw_sql = liquibase_utilities.generate_sql(working_changes[0])
        print(f"Rollback: {raw_sql}")

###
### Default return code
###
False