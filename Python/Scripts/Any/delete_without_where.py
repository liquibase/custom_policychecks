###
### This script checks for the phrase "DELETE FROM" without "WHERE"
###
### Implementation notes:
###   Uses liquibase_sqlglot.parse_changes with extract_statements_starting_with
###   so the SQL is walked once and only DELETE-leading statements are parsed.
###   On bulk-INSERT changesets (potentially many MB) that happen to contain
###   the substring "delete" in row data, this short-circuits the parser
###   instead of paying full SQL tokenization on the entire payload.
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
### Walk each change's SQL once and parse only DELETE-leading statements.
### must_contain_all skips the walk entirely on changes whose generated SQL
### does not contain "delete" anywhere.
###
for _stmt, expressions in liquibase_sqlglot.parse_changes(
        must_contain_all=("delete",),
        extract_statements_starting_with="delete"):
    for expression in expressions:
        ###
        ### Fire when a DELETE statement carries no WHERE clause.
        ### sqlglot represents missing WHERE as args.get("where") is None,
        ### so cases like "DELETE FROM t WHERE 1=1" parse correctly and
        ### do not fire, while "DELETE FROM t" does fire.
        ###
        if isinstance(expression, exp.Delete) and expression.args.get("where") is None:
            liquibase_status.fired = True
            liquibase_status.message = liquibase_utilities.get_script_message()
            sys.exit(1)

###
### Default return code
###
False
