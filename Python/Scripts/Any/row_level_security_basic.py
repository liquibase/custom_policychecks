###
### Row-Level Security Policy Check (Basic - Pattern Matching)
###
### This check enforces row-level security on shared configuration tables by validating
### that DML operations (INSERT, UPDATE, DELETE) only affect records belonging to the
### deploying team.
###
### Configuration Parameters:
### - ENV_VAR_NAME: Environment variable containing team identifier (e.g., "TEAM_ID")
### - PROTECTED_TABLES: Comma-separated list of protected table names
### - TEAM_COLUMN: Column name identifying record ownership (e.g., "SOURCE", "SUBSYSTEM")
###
### Validation Approach:
### Uses pattern matching/regex to validate:
### - INSERT: Team column must be present with correct value
### - UPDATE/DELETE: WHERE clause must include team_column = 'team_value'
###

import liquibase_utilities
import sys
import os
import re

###
### Retrieve log handler
###
liquibase_logger = liquibase_utilities.get_logger()

###
### Retrieve status handler
###
liquibase_status = liquibase_utilities.get_status()

###
### Retrieve configuration parameters
###
env_var_name = liquibase_utilities.get_arg("ENV_VAR_NAME")
protected_tables_str = liquibase_utilities.get_arg("PROTECTED_TABLES")
team_column = liquibase_utilities.get_arg("TEAM_COLUMN")

###
### Parse protected tables list
###
protected_tables = [table.strip().upper() for table in protected_tables_str.split(",")]

###
### Get team identifier from environment variable
###
team_id = os.environ.get(env_var_name)
if not team_id:
    liquibase_logger.warning(f"Environment variable '{env_var_name}' not set. Row-level security check skipped.")
    liquibase_status.fired = False
    sys.exit(1)

###
### Helper Functions
###

def extract_table_name(sql_statement):
    """
    Extract table name from INSERT, UPDATE, or DELETE statement.
    Returns table name in uppercase, or None if not found.
    """
    # Remove schema prefix if present and handle various formats
    # Pattern: INSERT INTO [schema.]table_name or UPDATE [schema.]table_name or DELETE FROM [schema.]table_name

    # Handle INSERT INTO
    insert_match = re.search(r'insert\s+into\s+(?:[\w]+\.)?([`"\[]?\w+[`"\]]?)', sql_statement, re.IGNORECASE)
    if insert_match:
        table = insert_match.group(1).strip('`"[]').upper()
        return table

    # Handle UPDATE
    update_match = re.search(r'update\s+(?:[\w]+\.)?([`"\[]?\w+[`"\]]?)', sql_statement, re.IGNORECASE)
    if update_match:
        table = update_match.group(1).strip('`"[]').upper()
        return table

    # Handle DELETE FROM
    delete_match = re.search(r'delete\s+from\s+(?:[\w]+\.)?([`"\[]?\w+[`"\]]?)', sql_statement, re.IGNORECASE)
    if delete_match:
        table = delete_match.group(1).strip('`"[]').upper()
        return table

    return None

def is_protected_table(table_name):
    """Check if table is in the protected tables list."""
    if not table_name:
        return False
    return table_name.upper() in protected_tables

def validate_insert(sql_statement, table_name):
    """
    Validate INSERT statement has team column with correct value.
    Returns (is_valid, error_message).
    """
    # Check if team column is present in the INSERT statement
    # Pattern: INSERT INTO table (col1, team_column, col3) VALUES (val1, 'team_id', val3)

    # Find column list
    columns_match = re.search(r'\(\s*([^)]+)\s*\)\s*values', sql_statement, re.IGNORECASE)
    if not columns_match:
        # Handle INSERT ... SELECT or other formats - check if team column mentioned
        if re.search(rf'\b{team_column}\b', sql_statement, re.IGNORECASE):
            # Check if team value is present (quoted)
            if re.search(rf"'{re.escape(team_id)}'", sql_statement, re.IGNORECASE):
                return (True, None)
        return (False, f"INSERT on table {table_name} must include {team_column} = '{team_id}'")

    columns_str = columns_match.group(1)
    columns = [col.strip().strip('`"[]') for col in columns_str.split(',')]

    # Check if team column is in the column list (case insensitive)
    team_column_idx = -1
    for idx, col in enumerate(columns):
        if col.upper() == team_column.upper():
            team_column_idx = idx
            break

    if team_column_idx == -1:
        return (False, f"INSERT on table {table_name} must include {team_column} = '{team_id}'")

    # Find VALUES clause
    values_match = re.search(r'values\s*\(([^)]+)\)', sql_statement, re.IGNORECASE)
    if not values_match:
        # Handle INSERT ... SELECT
        if re.search(rf"'{re.escape(team_id)}'", sql_statement, re.IGNORECASE):
            return (True, None)
        return (False, f"INSERT on table {table_name} must include {team_column} = '{team_id}'")

    values_str = values_match.group(1)

    # Split values by comma, but be careful with nested parentheses and functions
    values = []
    current_value = ""
    paren_depth = 0
    in_quotes = False
    quote_char = None

    for char in values_str:
        if char in ('"', "'") and not in_quotes:
            in_quotes = True
            quote_char = char
            current_value += char
        elif char == quote_char and in_quotes:
            in_quotes = False
            quote_char = None
            current_value += char
        elif char == '(' and not in_quotes:
            paren_depth += 1
            current_value += char
        elif char == ')' and not in_quotes:
            paren_depth -= 1
            current_value += char
        elif char == ',' and paren_depth == 0 and not in_quotes:
            values.append(current_value.strip())
            current_value = ""
        else:
            current_value += char

    if current_value:
        values.append(current_value.strip())

    # Check if we have enough values
    if team_column_idx >= len(values):
        return (False, f"INSERT on table {table_name} must include {team_column} = '{team_id}'")

    # Get the value at the position of the team column
    team_value = values[team_column_idx].strip()

    # Check for NULL
    if team_value.upper() == 'NULL':
        return (False, f"INSERT on table {table_name} must include {team_column} = '{team_id}'")

    # Check for empty string
    if team_value in ("''", '""'):
        return (False, f"INSERT on table {table_name} must include {team_column} = '{team_id}'")

    # Check if it matches the team_id (with or without quotes)
    team_value_unquoted = team_value.strip('\'"')
    if team_value_unquoted.upper() != team_id.upper():
        return (False, f"INSERT on table {table_name} must include {team_column} = '{team_id}'")

    return (True, None)

def validate_update_or_delete(sql_statement, table_name, operation):
    """
    Validate UPDATE/DELETE statement has WHERE clause with team filtering.
    Returns (is_valid, error_message).
    """
    # Check for WHERE clause
    if not re.search(r'\bwhere\b', sql_statement, re.IGNORECASE):
        return (False, f"{operation} on table {table_name} must filter by {team_column} = '{team_id}'")

    # Extract WHERE clause
    where_match = re.search(r'where\s+(.+?)(?:;|$)', sql_statement, re.IGNORECASE | re.DOTALL)
    if not where_match:
        return (False, f"{operation} on table {table_name} must filter by {team_column} = '{team_id}'")

    where_clause = where_match.group(1)

    # Check if team column is in WHERE clause with correct value
    # Pattern: team_column = 'team_id' (with various spacing and quote variations)
    team_filter_pattern = rf'\b{team_column}\b\s*=\s*[\'"]?{re.escape(team_id)}[\'"]?'

    if not re.search(team_filter_pattern, where_clause, re.IGNORECASE):
        return (False, f"{operation} on table {table_name} must filter by {team_column} = '{team_id}'")

    # Check for dangerous OR conditions that might bypass the team filter
    # If OR is present, we need to be more careful
    if re.search(r'\bor\b', where_clause, re.IGNORECASE):
        # This is potentially dangerous - the OR could allow access to other teams' data
        # For basic pattern matching, we'll flag this as a violation
        # The advanced version with SQL parsing can handle this more intelligently
        return (False, f"{operation} on table {table_name} must filter by {team_column} = '{team_id}'")

    return (True, None)

###
### Main Processing
###

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
        liquibase_logger.info("LoadData change type not supported. Statement skipped.")
        continue

    ###
    ### Retrieve sql as string, remove comments but preserve case for values
    ###
    raw_sql = liquibase_utilities.strip_comments(liquibase_utilities.generate_sql(change))

    ###
    ### Split sql into statements
    ###
    raw_statements = liquibase_utilities.split_statements(raw_sql)

    for raw_statement in raw_statements:
        ###
        ### Normalize whitespace for easier pattern matching
        ###
        normalized_sql = " ".join(raw_statement.split())

        ###
        ### Determine statement type (INSERT, UPDATE, DELETE)
        ###
        statement_type = None
        if re.match(r'^\s*insert\s+into', normalized_sql, re.IGNORECASE):
            statement_type = 'INSERT'
        elif re.match(r'^\s*update\s+', normalized_sql, re.IGNORECASE):
            statement_type = 'UPDATE'
        elif re.match(r'^\s*delete\s+from', normalized_sql, re.IGNORECASE):
            statement_type = 'DELETE'
        else:
            # Not a DML statement we care about
            continue

        ###
        ### Extract table name
        ###
        table_name = extract_table_name(normalized_sql)
        if not table_name:
            liquibase_logger.warning(f"Could not extract table name from {statement_type} statement. Statement skipped.")
            continue

        ###
        ### Check if table is protected
        ###
        if not is_protected_table(table_name):
            # Not a protected table, skip validation
            continue

        ###
        ### Validate based on statement type
        ###
        is_valid = False
        error_message = None

        if statement_type == 'INSERT':
            is_valid, error_message = validate_insert(normalized_sql, table_name)
        elif statement_type in ['UPDATE', 'DELETE']:
            is_valid, error_message = validate_update_or_delete(normalized_sql, table_name, statement_type)

        ###
        ### Fire violation if validation failed
        ###
        if not is_valid:
            liquibase_status.fired = True
            # Replace tokens in message template
            status_message = str(liquibase_utilities.get_script_message())
            status_message = status_message.replace("__OPERATION__", statement_type)
            status_message = status_message.replace("__TABLE_NAME__", table_name)
            status_message = status_message.replace("__TEAM_COLUMN__", team_column)
            status_message = status_message.replace("__TEAM_VALUE__", team_id)

            liquibase_status.message = status_message
            liquibase_logger.warning(f"Row-level security violation: {error_message}")
            liquibase_logger.info(f"SQL: {raw_statement[:200]}...")  # Log first 200 chars
            sys.exit(1)

###
### Default return code
###
False
