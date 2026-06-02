###
### This script checks that all SQL object references include a schema (e.g., dbo.TableName)
###
### Notes:
### 1. Applies to SELECT, INSERT, UPDATE, DELETE, EXEC, CREATE, and ALTER statements
### 2. Ignores literals, column names, and functions
###
import sys
import re
import sqlparse
from sqlparse.sql import Identifier
from sqlparse.tokens import Keyword, DDL, DML, Name
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

def extract_object_identifiers(stmt):
    """
    Return object identifiers (tables, procs) that should have a schema.
    Only takes the first token after relevant keywords to avoid multi-line issues.
    """
    identifiers = []
    tokens = [t for t in stmt.tokens if not t.is_whitespace]
    
    # Pre-collect all aliases defined in the statement (e.g., "dbo.users u" -> alias "u")
    defined_aliases = set()
    for token in tokens:
        if isinstance(token, Identifier):
            alias = token.get_alias()
            if alias:
                defined_aliases.add(alias.lower())

    # Pre-collect cursor names (e.g., DECLARE crs_Year CURSOR ...)
    defined_cursors = set()
    for i, token in enumerate(tokens):
        if token.ttype is Keyword and token.value.upper() == "CURSOR":
            if i > 0:
                cursor_name = str(tokens[i - 1]).strip().lower()
                defined_cursors.add(cursor_name)
    
    for i, token in enumerate(tokens):
        is_dml_trigger = (
            token.ttype is DML and token.value.upper() in ("UPDATE", "INSERT", "DELETE")
        )
        is_ddl_trigger = (
            token.ttype in (DDL, Keyword) and token.value.upper() in ("CREATE", "ALTER")
        )
        is_keyword_trigger = (
            token.ttype is Keyword and token.value.upper() in (
                "FROM", "JOIN", "INTO", "EXEC", "EXECUTE",
                "PROCEDURE", "TABLE", "VIEW"
            )
        )
        if not (is_dml_trigger or is_ddl_trigger or is_keyword_trigger):
            continue

        # Look ahead for next non-whitespace token
        j = i + 1
        while j < len(tokens) and tokens[j].is_whitespace:
            j += 1
        if j >= len(tokens):
            continue

        next_token = tokens[j]

        # Skip tokens that are known aliases or cursor names (e.g., UPDATE u ... FROM dbo.users u)
        token_str = str(next_token).strip().lower()
        if token_str in defined_aliases or token_str in defined_cursors:
            continue

        # Skip subqueries (next token is an opening parenthesis)
        if str(next_token).strip().startswith("("):
            continue

        if isinstance(next_token, Identifier):
            identifiers.append(next_token)
        elif next_token.ttype in (Name, None):
            obj_name_str = str(next_token).strip()
            if obj_name_str:
                identifiers.append(Identifier([next_token]))

    return identifiers

def check_schema_qualification(sql_text):
    """
    Parses the provided SQL text and returns a list of unqualified object names
    that are missing a schema prefix (e.g., TableName instead of dbo.TableName).
    Returns an empty list if all objects are properly schema-qualified.
    """
    violations = []
    statements = sqlparse.parse(sql_text)
    for stmt in statements:
        stmt_str = str(stmt).strip()
        # Skip unsupported statements
        if not re.match(r"^\s*(SELECT|INSERT|UPDATE|DELETE|EXEC|EXECUTE|CREATE|ALTER)\b", stmt_str, re.IGNORECASE):
            continue
        # Extract identifiers and check for schema prefix
        identifiers = extract_object_identifiers(stmt)
        for ident in identifiers:
            full_name = str(ident).strip().split()[0]  # only first token
            schema = ident.get_parent_name()
            name = ident.get_real_name() or ident.get_name()
            # Ignore temp tables, variables, sys objects, etc.
            if not name or name.startswith("#") or name.startswith("@") or full_name.lower().startswith("sys."):
                continue
            # Flag if schema missing
            if not schema and "." not in full_name:
                violations.append(full_name)
    return violations

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
        continue
    ###
    ### Retrieve raw sql and check for schema qualification violations
    ###
    sql_text = liquibase_utilities.generate_sql(change)
    # print(f"RAW SQL: {repr(sql_text)}")
    violations = check_schema_qualification(sql_text)
    if violations:
        msg = f"Missing schema for object '{violations[0]}' in SQL statement."
        liquibase_logger.warning(msg)
        liquibase_status.fired = True
        liquibase_status.message = msg
        sys.exit(1)

###
### Default return code
###
False