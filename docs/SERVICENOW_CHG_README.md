# ServiceNow CHG Label Validation Policy Check

## Overview

This custom Liquibase policy check ensures that every database changeset has a valid ServiceNow Change Request (CHG) label **and** verifies that the CHG ticket exists in ServiceNow via API.

## Purpose

- **Traceability**: Links every database change to an approved ServiceNow Change Request
- **Compliance**: Ensures no unauthorized database changes
- **Audit**: Provides clear audit trail between database changes and change management process

## How It Works

1. **Label Format Check**: Validates that the changeset has a label matching pattern `CHG\d{7}` (case-insensitive)
2. **API Validation**: Makes a REST API call to ServiceNow to verify the CHG ticket exists
3. **Failure Actions**: Blocks the changeset execution if:
   - No CHG label is present
   - CHG label format is invalid
   - CHG ticket doesn't exist in ServiceNow
   - API authentication fails

## Configuration

### Required Settings

Set these via **environment variables** or **Liquibase check arguments**:

| Variable | Description | Example |
|----------|-------------|---------|
| `SERVICENOW_INSTANCE` | Your ServiceNow instance hostname | `mycompany.service-now.com` |
| `SERVICENOW_USERNAME` | ServiceNow API username | `api_user` |
| `SERVICENOW_PASSWORD` | ServiceNow API password | `your_password` |

### Option 1: Environment Variables

```bash
export SERVICENOW_INSTANCE="mycompany.service-now.com"
export SERVICENOW_USERNAME="api_user"
export SERVICENOW_PASSWORD="your_password"

liquibase checks run
```

### Option 2: Check Arguments

Add to your `liquibase.checks-settings.yml`:

```yaml
- shortName: servicenow_chg_label
  enabled: true
  arg:
    SERVICENOW_INSTANCE: mycompany.service-now.com
    SERVICENOW_USERNAME: api_user
    SERVICENOW_PASSWORD: ${SERVICENOW_PASSWORD}  # Use environment variable for password
```

## Usage Examples

### Valid Changeset (Will Pass)

```xml
<changeSet id="1" author="john.doe" labels="CHG0010001">
    <createTable tableName="users">
        <column name="id" type="int">
            <constraints primaryKey="true"/>
        </column>
        <column name="username" type="varchar(50)"/>
    </createTable>
</changeSet>
```

### Invalid Changeset (Will Fail)

```xml
<!-- No CHG label -->
<changeSet id="2" author="john.doe">
    <createTable tableName="orders">
        <column name="id" type="int"/>
    </createTable>
</changeSet>

<!-- Invalid CHG format -->
<changeSet id="3" author="john.doe" labels="CHG123">
    <createTable tableName="products">
        <column name="id" type="int"/>
    </createTable>
</changeSet>

<!-- Valid format, but doesn't exist in ServiceNow -->
<changeSet id="4" author="john.doe" labels="CHG9999999">
    <createTable tableName="inventory">
        <column name="id" type="int"/>
    </createTable>
</changeSet>
```

### Multiple Labels

You can have multiple labels, but at least one must be a valid CHG:

```xml
<changeSet id="5" author="john.doe" labels="production,CHG0010001,hotfix">
    <addColumn tableName="users">
        <column name="email" type="varchar(100)"/>
    </addColumn>
</changeSet>
```

## ServiceNow API Details

### Endpoint Used

```
GET https://{instance}/api/now/table/change_request?sysparm_query=number={CHG}&sysparm_limit=1
```

### Required Permissions

The ServiceNow user must have:
- Read access to the `change_request` table
- API access enabled

### Authentication

Uses HTTP Basic Authentication with base64-encoded credentials.

## Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| `ServiceNow configuration missing` | Environment variables not set | Set `SERVICENOW_INSTANCE`, `SERVICENOW_USERNAME`, `SERVICENOW_PASSWORD` |
| `Changeset does not have a valid ServiceNow CHG label` | No label matching `CHG\d{7}` pattern | Add a label like `CHG0010001` to your changeset |
| `CHG {number} not found in ServiceNow` | CHG doesn't exist in ServiceNow | Verify the CHG number is correct and exists |
| `Authentication failed to ServiceNow` | Invalid credentials | Check username and password |
| `Access forbidden to ServiceNow` | User lacks API permissions | Grant API access to the ServiceNow user |
| `Failed to connect to ServiceNow` | Network/DNS issue | Verify instance hostname and network connectivity |

## Testing

### Test Without ServiceNow Connection

For testing purposes, you can create a mock version that skips API validation:

```python
# Set this environment variable to skip API validation
export SERVICENOW_MOCK_MODE=true
```

### Integration Tests

See the comprehensive test suite in:
```
custom_policychecks/Python/tests/test_servicenow_chg_label.py
```

Run tests:
```bash
cd custom_policychecks
pytest Python/tests/test_servicenow_chg_label.py -v
```

## Security Considerations

⚠️ **Important Security Notes:**

1. **Password Storage**: Never hardcode passwords in configuration files
   - Use environment variables
   - Use secret management tools (HashiCorp Vault, AWS Secrets Manager, etc.)
   - Use CI/CD pipeline secrets

2. **API User**: Create a dedicated ServiceNow user for API access
   - Grant minimal required permissions (read-only on change_request table)
   - Rotate credentials regularly

3. **Network Security**: Use HTTPS only (enforced in the script)
   - Consider network whitelisting
   - Use VPN if accessing ServiceNow from external networks

## Troubleshooting

### Enable Debug Logging

Set Liquibase log level to DEBUG:

```bash
liquibase --log-level=DEBUG checks run
```

### Test ServiceNow Connectivity

```bash
curl -u "username:password" \
  "https://mycompany.service-now.com/api/now/table/change_request?sysparm_query=number=CHG0010001&sysparm_limit=1"
```

### Common Issues

1. **Timeout errors**: Check network connectivity and ServiceNow instance availability
2. **401 Unauthorized**: Verify credentials are correct
3. **403 Forbidden**: Check user has API access and table permissions
4. **CHG not found**: Verify CHG exists and is spelled correctly (case-insensitive)

## Customization

### Adjust CHG Pattern

To support different CHG formats, modify line 151:

```python
# Current: CHG followed by exactly 7 digits
chg_pattern = re.compile(r'^CHG\d{7}$', re.IGNORECASE)

# Alternative: CHG followed by 4-10 digits
chg_pattern = re.compile(r'^CHG\d{4,10}$', re.IGNORECASE)
```

### Add State Validation

You can modify the validation function to check CHG state (e.g., only allow "Approved" changes):

```python
if result.get('result') and len(result['result']) > 0:
    chg_data = result['result'][0]
    state = chg_data.get('state', '')
    if state != '3':  # 3 = Approved in ServiceNow
        return False, f"CHG {chg_number} is not in Approved state"
    return True, f"CHG {chg_number} found and approved"
```

## Support

For issues or questions:
1. Check the error message in Liquibase output
2. Verify ServiceNow API connectivity with curl
3. Review Liquibase logs with DEBUG level
4. Check ServiceNow user permissions

## Related Documentation

- [ServiceNow Table API](https://docs.servicenow.com/bundle/tokyo-application-development/page/integrate/inbound-rest/concept/c_TableAPI.html)
- [ServiceNow Change Management](https://docs.servicenow.com/bundle/tokyo-it-service-management/page/product/change-management/concept/c_ITILChangeManagement.html)
- [Liquibase Custom Policy Checks](https://docs.liquibase.com/workflows/liquibase-community/using-liquibase-custom-policy-checks.html)
