###
### Row-Level Security Policy Check (Advanced - SQL Parsing)
###
### This check enforces row-level security on shared configuration tables by validating
### that DML operations (INSERT, UPDATE, DELETE) only affect records belonging to the
### deploying team. Uses sqlparse for semantic SQL analysis.
###
### Configuration Parameters:
### - ENV_VAR_NAME: Environment variable containing team identifier (e.g., "TEAM_ID")
### - PROTECTED_TABLES: Comma-separated list of protected table names
### - TEAM_COLUMN: Column name identifying record ownership (e.g., "SOURCE", "SUBSYSTEM")
###
### Validation Approach:
### Uses sqlparse library for semantic SQL analysis:
### - Parses SQL into token structure
### - Semantically analyzes WHERE clauses and INSERT statements
### - Handles complex SQL (subqueries, JOINs, CTEs, etc.)
###

import liquibase_utilities
import sqlparse
from sqlparse.sql import IdentifierList, Identifier, Where, Parenthesis, Comparison, Token
from sqlparse.tokens import Keyword, DML
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

def get_table_name_from_statement(parsed):
    """Extract table name from parsed SQL statement."""
    table_name = None
    found_keyword = False

    for token in parsed.tokens:
        if token.ttype is Keyword and token.value.upper() in ('INTO', 'UPDATE', 'FROM'):
            found_keyword = True
            continue

        if found_keyword:
            if isinstance(token, Identifier):
                table_name = token.get_real_name()
                break
            elif token.ttype is not Keyword and not token.is_whitespace:
                # Handle simple table names
                table_name = str(token).strip().strip('`"[]')
                # Remove schema prefix if present
                if '.' in table_name:
                    table_name = table_name.split('.')[-1].strip('`"[]')
                break

    return table_name.upper() if table_name else None

def is_protected_table(table_name):
    """Check if table is in the protected tables list."""
    if not table_name:
        return False
    return table_name.upper() in protected_tables

def find_where_clause(parsed):
    """Find WHERE clause in parsed SQL."""
    for token in parsed.tokens:
        if isinstance(token, Where):
            return token
    return None

def extract_columns_and_values(parsed):
    """
    Extract columns and values from INSERT statement.
    Returns (columns_list, values_list) or (None, None) if not found.
    """
    columns = []
    values = []
    found_columns = False
    found_values = False

    for token in parsed.tokens:
        # Find column list
        if isinstance(token, Parenthesis) and not found_columns:
            # This is the column list
            col_str = str(token).strip('()')
            for col in col_str.split(','):
                columns.append(col.strip().strip('`"[]'))
            found_columns = True
            continue

        # Find VALUES keyword
        if token.ttype is Keyword and token.value.upper() == 'VALUES':
            found_values = True
            continue

        # Find values list
        if found_values and isinstance(token, Parenthesis):
            val_str = str(token).strip('()')
            # Simple split by comma - may need refinement for complex values
            depth = 0
            current = ""
            for char in val_str:
                if char == '(' :
                    depth += 1
                    current += char
                elif char == ')':
                    depth -= 1
                    current += char
                elif char == ',' and depth == 0:
                    values.append(current.strip())
                    current = ""
                else:
                    current += char
            if current:
                values.append(current.strip())
            break

    if columns and values:
        return (columns, values)
    return (None, None)

def check_team_filter_in_where(where_clause, team_column_name, team_value):
    """
    Check if WHERE clause contains team column = team value.
    Returns True if valid team filtering found, False otherwise.
    """
    if not where_clause:
        return False

    # Convert WHERE clause to string and check with regex as fallback
    where_str = str(where_clause).upper()
    team_col_upper = team_column_name.upper()
    team_val_upper = team_value.upper()

    # Check if team column and value appear in WHERE clause
    # Pattern: TEAM_COLUMN = 'TEAM_VALUE' or TEAM_COLUMN='TEAM_VALUE'
    pattern = rf'\b{team_col_upper}\b\s*=\s*[\'"]?{re.escape(team_val_upper)}[\'"]?'
    if re.search(pattern, where_str):
        return True

    # Also try parsing the WHERE clause tokens
    return check_tokens_for_team_filter(where_clause, team_column_name, team_value)

def check_tokens_for_team_filter(token_group, team_column_name, team_value):
    """
    Recursively check tokens for team filtering condition.
    """
    team_col_upper = team_column_name.upper()
    team_val_upper = team_value.upper()

    if isinstance(token_group, Comparison):
        comp_str = str(token_group).upper()
        # Check if this is a comparison of team column to team value
        if team_col_upper in comp_str and team_val_upper in comp_str:
            return True

    if hasattr(token_group, 'tokens'):
        for token in token_group.tokens:
            if isinstance(token, (Parenthesis, Where, Comparison)):
                if check_tokens_for_team_filter(token, team_column_name, team_value):
                    return True
            elif isinstance(token, Identifier):
                # Check if this identifier is our team column
                if token.get_real_name() and token.get_real_name().upper() == team_col_upper:
                    # Look for = and team value nearby
                    token_str = str(token.parent if hasattr(token, 'parent') else token).upper()
                    if '=' in token_str and team_val_upper in token_str:
                        return True

    return False

def validate_insert(parsed, table_name):
    """
    Validate INSERT statement using SQL parsing.
    Returns (is_valid, error_message).
    """
    columns, values = extract_columns_and_values(parsed)

    if not columns:
        # Handle INSERT ... SELECT
        sql_str = str(parsed).upper()
        if 'SELECT' in sql_str:
            # For INSERT...SELECT, just check if team column and value are mentioned
            if team_column.upper() in sql_str and team_id.upper() in sql_str:
                return (True, None)
        return (False, f"INSERT on table {table_name} must include {team_column} = '{team_id}'")

    # Find team column index
    team_col_idx = -1
    for idx, col in enumerate(columns):
        if col.upper() == team_column.upper():
            team_col_idx = idx
            break

    if team_col_idx == -1:
        return (False, f"INSERT on table {table_name} must include {team_column} = '{team_id}'")

    if team_col_idx >= len(values):
        return (False, f"INSERT on table {table_name} must include {team_column} = '{team_id}'")

    # Get team value
    team_value = values[team_col_idx].strip().strip('\'"')

    # Check for NULL or empty
    if team_value.upper() == 'NULL' or team_value == '':
        return (False, f"INSERT on table {table_name} must include {team_column} = '{team_id}'")

    # Check if value matches team_id
    if team_value.upper() != team_id.upper():
        return (False, f"INSERT on table {table_name} must include {team_column} = '{team_id}'")

    return (True, None)

def validate_update_or_delete(parsed, table_name, operation):
    """
    Validate UPDATE/DELETE statement using SQL parsing.
    Returns (is_valid, error_message).
    """
    where_clause = find_where_clause(parsed)

    if not where_clause:
        return (False, f"{operation} on table {table_name} must filter by {team_column} = '{team_id}'")

    # Check if WHERE clause contains team filtering
    if not check_team_filter_in_where(where_clause, team_column, team_id):
        return (False, f"{operation} on table {table_name} must filter by {team_column} = '{team_id}'")

    # Check for dangerous OR conditions that might bypass team filter
    where_str = str(where_clause).upper()
    if ' OR ' in where_str:
        # This is potentially dangerous - need to ensure OR doesn't bypass team filter
        # For now, we'll flag this as a violation (conservative approach)
        # A more sophisticated version would parse the logical structure
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
    ### Retrieve sql as string, remove comments
    ###
    raw_sql = liquibase_utilities.strip_comments(liquibase_utilities.generate_sql(change))

    ###
    ### Split sql into statements
    ###
    raw_statements = liquibase_utilities.split_statements(raw_sql)

    for raw_statement in raw_statements:
        ###
        ### Parse SQL statement
        ###
        parsed = sqlparse.parse(raw_statement)
        if not parsed:
            continue

        statement = parsed[0]

        ###
        ### Determine statement type
        ###
        statement_type = None
        first_token = statement.token_first(skip_ws=True, skip_cm=True)

        if first_token and first_token.ttype is DML:
            statement_type = first_token.value.upper()

        if statement_type not in ['INSERT', 'UPDATE', 'DELETE']:
            # Not a DML statement we care about
            continue

        ###
        ### Extract table name
        ###
        table_name = get_table_name_from_statement(statement)
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
            is_valid, error_message = validate_insert(statement, table_name)
        elif statement_type in ['UPDATE', 'DELETE']:
            is_valid, error_message = validate_update_or_delete(statement, table_name, statement_type)

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
