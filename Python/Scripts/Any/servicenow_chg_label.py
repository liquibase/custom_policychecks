###
### This script checks that every changeset has a valid ServiceNow CHG label
### and verifies the CHG exists in ServiceNow via API
###
### ServiceNow Change Request numbers follow the pattern: CHG followed by 7 digits
### Example: CHG0010001, CHG1234567
###
### This ensures traceability between database changes and ServiceNow Change Management
###
### Configuration (via environment variables or check arguments):
### - SERVICENOW_INSTANCE: Your ServiceNow instance (e.g., 'mycompany.service-now.com')
### - SERVICENOW_USERNAME: ServiceNow API username
### - SERVICENOW_PASSWORD: ServiceNow API password (or use OAuth token)
###
### Notes:
### - Pattern is case-insensitive (CHG, chg, ChG all accepted)
### - Must be exactly CHG followed by 7 digits
### - Validates CHG exists in ServiceNow via REST API
### - Can be one of multiple comma-separated labels
###

###
### Helpers come from Liquibase
###
import liquibase_utilities
import liquibase_changesets
import re
import sys
import os
import urllib.request
import urllib.error
import json
import base64

###
### Function to validate CHG exists in ServiceNow
###
def validate_chg_in_servicenow(chg_number, instance, username, password):
    """
    Validates that a CHG exists in ServiceNow via REST API

    Args:
        chg_number: The CHG number to validate (e.g., CHG0010001)
        instance: ServiceNow instance hostname
        username: ServiceNow username
        password: ServiceNow password

    Returns:
        tuple: (success: bool, message: str)
    """
    try:
        # ServiceNow Table API endpoint for change_request table
        url = f"https://{instance}/api/now/table/change_request"
        params = f"?sysparm_query=number={chg_number}&sysparm_limit=1&sysparm_fields=number,state,short_description"
        full_url = url + params

        # Create Basic Auth header
        credentials = f"{username}:{password}"
        encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')

        # Create request
        request = urllib.request.Request(full_url)
        request.add_header("Authorization", f"Basic {encoded_credentials}")
        request.add_header("Accept", "application/json")

        # Make API call
        response = urllib.request.urlopen(request, timeout=10)
        response_data = response.read().decode('utf-8')
        result = json.loads(response_data)

        # Check if CHG was found
        if result.get('result') and len(result['result']) > 0:
            chg_data = result['result'][0]
            return True, f"CHG {chg_number} found in ServiceNow (State: {chg_data.get('state', 'unknown')})"
        else:
            return False, f"CHG {chg_number} not found in ServiceNow"

    except urllib.error.HTTPError as e:
        if e.code == 401:
            return False, "Authentication failed to ServiceNow: Invalid credentials"
        elif e.code == 403:
            return False, "Access forbidden to ServiceNow: Check API permissions"
        else:
            return False, f"HTTP error from ServiceNow: {e.code} - {e.reason}"
    except urllib.error.URLError as e:
        return False, f"Failed to connect to ServiceNow: {str(e.reason)}"
    except Exception as e:
        return False, f"Error validating CHG in ServiceNow: {str(e)}"


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
### Get the changeset object
###
changeset = liquibase_utilities.get_changeset()

###
### Get configuration from environment variables or arguments
###
servicenow_instance = os.getenv('SERVICENOW_INSTANCE', '')
servicenow_username = os.getenv('SERVICENOW_USERNAME', '')
servicenow_password = os.getenv('SERVICENOW_PASSWORD', '')

# Try to get from check arguments if not in environment
if not servicenow_instance:
    servicenow_instance = liquibase_utilities.get_arg('SERVICENOW_INSTANCE', '')
if not servicenow_username:
    servicenow_username = liquibase_utilities.get_arg('SERVICENOW_USERNAME', '')
if not servicenow_password:
    servicenow_password = liquibase_utilities.get_arg('SERVICENOW_PASSWORD', '')

###
### Validate configuration
###
if not servicenow_instance or not servicenow_username or not servicenow_password:
    liquibase_logger.error("ServiceNow configuration missing!")
    liquibase_logger.error("Required: SERVICENOW_INSTANCE, SERVICENOW_USERNAME, SERVICENOW_PASSWORD")
    liquibase_logger.error("Set via environment variables or check arguments")
    liquibase_status.fired = True
    liquibase_status.message = "ServiceNow configuration missing. Set SERVICENOW_INSTANCE, SERVICENOW_USERNAME, and SERVICENOW_PASSWORD."
    sys.exit(1)

###
### Get labels from changeset using liquibase_changesets.get_labels()
### This returns a set of string labels
###
labels_set = liquibase_changesets.get_labels(changeset)

###
### Convert to list for easier processing
###
if labels_set is None:
    labels_list = []
else:
    labels_list = list(labels_set)

###
### Define ServiceNow CHG pattern: CHG followed by exactly 7 digits
### Pattern is case-insensitive
###
chg_pattern = re.compile(r'^CHG\d{7}$', re.IGNORECASE)

###
### Find and validate CHG labels
###
chg_found = None
for label in labels_list:
    if chg_pattern.match(label):
        chg_found = label.upper()  # Normalize to uppercase for API call
        liquibase_logger.info(f"Found CHG label: {chg_found}")
        break

###
### If no CHG label found with correct format, fire the check
###
if not chg_found:
    liquibase_logger.warning(f"Changeset {changeset.getId()} does not have a valid ServiceNow CHG label")
    liquibase_logger.warning(f"Current labels: {labels_list if labels_list else 'None'}")
    liquibase_logger.warning("Required format: CHGxxxxxxx (where x is a digit)")
    liquibase_status.fired = True
    liquibase_status.message = liquibase_utilities.get_script_message()
    sys.exit(1)

###
### Validate CHG exists in ServiceNow
###
liquibase_logger.info(f"Validating {chg_found} in ServiceNow instance: {servicenow_instance}")
success, message = validate_chg_in_servicenow(chg_found, servicenow_instance, servicenow_username, servicenow_password)

if not success:
    liquibase_logger.error(f"CHG validation failed: {message}")
    liquibase_status.fired = True
    liquibase_status.message = f"CHG validation failed: {message}"
    sys.exit(1)

liquibase_logger.info(f"CHG validation successful: {message}")

###
### Default return code
###
False
