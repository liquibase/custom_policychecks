###
### This script checks for GRANT statements that do not include
### the EXECUTE privilege.
###
### Policy intent:
###   Only GRANT statements that convey EXECUTE are permitted.
###   Any GRANT that omits EXECUTE — whether it grants SELECT,
###   INSERT, UPDATE, DELETE, ALL, or any other privilege — will
###   cause this check to fire and block the changeset.
###
### Examples that PASS  (do not fire):
###   GRANT EXECUTE ON PROCEDURE my_proc TO app_user
###   GRANT EXECUTE ON my_function TO PUBLIC
###   GRANT EXECUTE ON OBJECT::my_proc TO app_user
###   GRANT EXECUTE ON TYPE::dbo.MyType TO app_user
###
### Examples that FAIL  (fire and block):
###   GRANT SELECT ON my_table TO app_user
###   GRANT INSERT, UPDATE ON my_table TO app_user
###   GRANT ALL ON my_schema TO app_user
###   GRANT SELECT (col1) ON my_table TO app_user
###   GRANT INSERT ON Object::Employees TO app_user      (SQL Server securable class)
###   GRANT SELECT ON SCHEMA::dbo TO app_user            (SQL Server securable class)
###
### Implementation notes:
###   Uses liquibase_sqlglot.parse_changes with extract_statements_starting_with
###   so the SQL is walked once and only GRANT-leading statements are parsed.
###   On bulk-INSERT changesets (potentially many MB) that happen to contain
###   the substring "grant" in row data, this short-circuits the parser
###   instead of paying full SQL tokenization on the entire payload.
###
###   sqlglot represents each privilege as a GrantPrivilege node whose
###   `this` child is a Var carrying the privilege keyword as its .name.
###   The comparison is case-insensitive (.upper() == "EXECUTE") so that
###   dialects which emit lowercase or mixed-case keywords are handled
###   correctly.
###
###   GRANT … EXECUTE … statements that also include other privileges
###   (e.g., GRANT EXECUTE, SELECT ON …) are intentionally *not* blocked
###   because the EXECUTE privilege is still present.  If your policy
###   requires EXECUTE-only grants with no additional privileges, replace
###   the `has_execute` check with an `is_execute_only` check:
###
###     is_execute_only = (
###         len(privileges) == 1 and
###         privileges[0].args.get("this") and
###         privileges[0].args["this"].name.upper() == "EXECUTE"
###     )
###
###   Securable-class fallback (SECURE-380):
###     sqlglot's tsql grammar does not model SQL Server's securable-class
###     GRANT syntax (`OBJECT::name`, `SCHEMA::name`, `TYPE::name`, …) and
###     emits an `exp.Command` node instead of `exp.Grant` for those
###     statements.  Relying solely on `isinstance(expression, exp.Grant)`
###     therefore lets every securable-class GRANT slip past silently.  To
###     close that hole this script applies a regex fallback whenever the
###     parser returns a non-Grant node whose raw SQL starts with `grant`:
###     we pull the privilege list directly from the source text and apply
###     the same EXECUTE rule.  Statements that do not look like a
###     recognisable GRANT (no `... ON ...` clause) are still skipped so
###     unrelated `Command` nodes are not mistaken for grants.
###
### Required Liquibase Secure: a build that includes
### liquibase_sqlglot.parse_changes(extract_statements_starting_with=...).
###

###
### Helpers come from Liquibase
###
import liquibase_utilities
import liquibase_sqlglot
import sqlglot.expressions as exp
import re
import sys

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
### Regex used by the securable-class fallback path described above.
### Captures the comma-separated privilege list between `GRANT` and `ON`.
### Tolerates leading whitespace, mixed case, and multi-line statements
### (sqlglot's `Command.sql()` preserves original whitespace).
###
_GRANT_PRIVILEGE_RE = re.compile(
    r"^\s*GRANT\s+(?P<privileges>.+?)\s+ON\b",
    re.IGNORECASE | re.DOTALL,
)


def _extract_privileges_from_raw_sql(raw_sql):
    ###
    ### Returns a list of uppercased privilege keywords parsed from a
    ### GRANT statement that sqlglot could not represent as exp.Grant.
    ### Returns None when the SQL does not look like a recognisable
    ### GRANT (so unrelated Command nodes are not treated as grants).
    ###
    match = _GRANT_PRIVILEGE_RE.match(raw_sql)
    if not match:
        return None
    privilege_names = []
    for piece in match.group("privileges").split(","):
        token = piece.strip()
        if not token:
            continue
        ### A privilege expression is always led by its keyword: the
        ### first whitespace- or paren-delimited token.  `SELECT(col1)`
        ### and `SELECT (col1)` both reduce to `SELECT`.
        head = re.split(r"[\s(]", token, maxsplit=1)[0]
        if head:
            privilege_names.append(head.upper())
    return privilege_names


def _fire():
    ###
    ### Fire the check.  Centralised so the AST path and the regex
    ### fallback record an identical status/exit.
    ###
    liquibase_status.fired = True
    liquibase_status.message = liquibase_utilities.get_script_message()
    sys.exit(1)


###
### Walk each change's SQL once and parse only GRANT-leading statements.
### must_contain_all skips the walk entirely on changes whose generated SQL
### does not contain "grant" anywhere (case-insensitive substring match
### performed by the Liquibase runtime before the parser is invoked).
###
for _stmt, expressions in liquibase_sqlglot.parse_changes(
        must_contain_all=("grant",),
        extract_statements_starting_with="grant"):
    for expression in expressions:
        if isinstance(expression, exp.Grant):
            ###
            ### Collect the list of privilege nodes from this GRANT statement.
            ### Each element is a GrantPrivilege whose .args["this"] is a Var
            ### holding the privilege keyword (SELECT, EXECUTE, INSERT, …).
            ###
            privileges = expression.args.get("privileges") or []
            has_execute = any(
                priv.args.get("this") and
                priv.args["this"].name.upper() == "EXECUTE"
                for priv in privileges
            )
            if not has_execute:
                _fire()
            continue

        ###
        ### Securable-class fallback: sqlglot returned a non-Grant node
        ### (typically exp.Command) for a statement that started with
        ### `grant`.  Try the regex.  If it still doesn't parse, skip —
        ### we don't want to false-fire on something that isn't really
        ### a GRANT.
        ###
        raw_sql = expression.sql()
        if not raw_sql.lstrip().lower().startswith("grant"):
            continue
        privilege_names = _extract_privileges_from_raw_sql(raw_sql)
        if privilege_names is None:
            continue
        if "EXECUTE" not in privilege_names:
            _fire()

###
### Default return code — no violation detected
###
False
