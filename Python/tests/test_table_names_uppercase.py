"""
Comprehensive test suite for table_names_uppercase.py custom policy check.

This check enforces that table names must be uppercase during table creation.
Policy Intent: Ensure consistent naming conventions across the database schema.
"""

import pytest
from liquibase_test_harness import BatchPolicyTest, LiquibaseCheck

# Message template from README configuration
MESSAGE_TEMPLATE = "Table __TABLE_NAME__ must be UPPERCASE."


class TestTableNamesUppercase:
    """Test suite for table_names_uppercase.py policy check."""

    def test_core_functionality(self, subtests):
        """
        Core functionality: Table naming validation during CREATE TABLE.
        Tests standard uppercase compliance and common violations.
        """
        batch = BatchPolicyTest(
            "Python/Scripts/Any/table_names_uppercase.py",
            message=MESSAGE_TEMPLATE
        )

        # ========================================
        # VALID: Uppercase table names (should NOT fire)
        # ========================================
        with batch.should_pass():
            batch.add(
                "CREATE TABLE USERS (id INT, name VARCHAR(50));",
                name="basic_uppercase"
            )
            batch.add(
                "CREATE TABLE USER_ACCOUNTS (id INT, balance DECIMAL(10,2));",
                name="uppercase_with_underscore"
            )
            batch.add(
                "CREATE OR REPLACE TABLE CUSTOMERS (id INT, email VARCHAR(100));",
                name="create_or_replace"
            )
            batch.add(
                """
                INSERT INTO users VALUES (1, 'test');
                UPDATE users SET name = 'updated' WHERE id = 1;
                DELETE FROM users WHERE id = 1;
                """,
                name="non_table_statements"
            )
            batch.add(
                "CREATE TABLE TEMP_TABLE",
                name="without_parentheses"
            )

        # ========================================
        # INVALID: Non-uppercase table names (SHOULD fire)
        # ========================================
        with batch.should_fail():
            batch.add(
                "CREATE TABLE users (id INT, name VARCHAR(50));",
                name="all_lowercase",
                match_message="users"
            )
            batch.add(
                "CREATE TABLE Users (id INT, name VARCHAR(50));",
                name="mixed_case",
                match_message="Users"
            )
            batch.add(
                "CREATE TABLE myTableName (id INT, data TEXT);",
                name="camelCase",
                match_message="myTableName"
            )

        with batch:
            batch.execute_with_subtests(subtests)

    def test_edge_cases_and_boundaries(self, subtests):
        """
        Edge cases and boundary conditions.
        Tests schema prefixes, quoted identifiers, special characters, and malformed SQL.
        """
        batch = BatchPolicyTest(
            "Python/Scripts/Any/table_names_uppercase.py",
            message=MESSAGE_TEMPLATE
        )

        # ========================================
        # VALID: Boundary cases (should NOT fire)
        # ========================================
        with batch.should_pass():
            batch.add(
                "CREATE TABLE A (id INT);",
                name="single_char_uppercase"
            )
            batch.add(
                "CREATE TABLE TABLE123 (id INT);",
                name="with_numbers"
            )
            batch.add(
                "CREATE TABLE USER_ACCOUNT_DATA (id INT);",
                name="multiple_underscores"
            )

        # ========================================
        # INVALID: Edge cases (SHOULD fire)
        # ========================================
        with batch.should_fail():
            batch.add(
                "CREATE TABLE myschema.users (id INT);",
                name="schema_prefix_lowercase"
            )
            batch.add(
                'CREATE TABLE "users" (id INT);',
                name="quoted_identifier"
            )
            batch.add(
                "CREATE TABLE a (id INT);",
                name="single_char_lowercase"
            )

        with batch:
            batch.execute_with_subtests(subtests)

    # ========================================
    # MALFORMED SQL - Test resilience (kept separate)
    # ========================================

    def test_malformed_sql_handling(self):
        """Edge case: Malformed SQL should not crash the check."""
        with LiquibaseCheck(
            "Python/Scripts/Any/table_names_uppercase.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            sql = "CREATE TABLE (id INT);"  # Missing table name
            result = check.run(sql=sql)
            # Should not crash - proper bounds checking should handle this

    def test_index_out_of_bounds_protection(self):
        """Bug test: Verify protection against IndexError when parsing SQL."""
        with LiquibaseCheck(
            "Python/Scripts/Any/table_names_uppercase.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            sql = "CREATE TABLE"  # Incomplete statement
            result = check.run(sql=sql)
            # Should not crash - bounds checking should protect against IndexError

    # ========================================
    # KNOWN BUGS - Kept separate as xfail
    # ========================================

    @pytest.mark.xfail(
        reason="BUG: table_names_uppercase.py exits on first violation instead of checking all CREATE TABLE statements. "
               "Root cause: Line 53 uses sys.exit(1) prematurely. Fix: Accumulate all violations before reporting."
    )
    def test_multiple_create_statements(self):
        """Edge case: Multiple CREATE TABLE statements in one changeset."""
        with LiquibaseCheck(
            "Python/Scripts/Any/table_names_uppercase.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            sql = """
            CREATE TABLE VALID_TABLE (id INT);
            CREATE TABLE invalid_table (id INT);
            """
            result = check.run(sql=sql)
            assert result.fired, "Should fire if any table name is not uppercase"

    @pytest.mark.xfail(
        reason="BUG: table_names_uppercase.py exits on first violation instead of checking all CREATE TABLE statements. "
               "Root cause: Line 53 uses sys.exit(1) prematurely. Same bug as test_multiple_create_statements."
    )
    def test_large_sql_performance(self):
        """Performance: Large SQL with many statements should execute efficiently."""
        with LiquibaseCheck(
            "Python/Scripts/Any/table_names_uppercase.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            # Generate large SQL with many valid statements and one invalid table
            sql_parts = ["CREATE TABLE VALID_TABLE_{} (id INT);".format(i) for i in range(50)]
            sql_parts.append("CREATE TABLE invalid_table (id INT);")  # This should trigger
            sql = "\n".join(sql_parts)

            result = check.run(sql=sql)
            assert result.fired, "Should find the invalid table name in large SQL"
            assert "Table" in result.message and "invalid_table" in result.message
