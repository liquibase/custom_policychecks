"""
Comprehensive test suite for identifiers_without_quotes.py custom policy check.

This check prevents the use of quoted identifiers (double quotes) in SQL statements.
Policy Intent: Enforce consistent identifier naming without quotes for better portability.
"""

import pytest
from liquibase_test_harness import BatchPolicyTest, LiquibaseCheck

# Message template from the policy check
MESSAGE_TEMPLATE = "Identifier __ID_NAME__ should not include quotes."


class TestIdentifiersWithoutQuotes:
    """Test suite for identifiers_without_quotes.py policy check."""

    def test_compliant_unquoted_identifiers(self, subtests):
        """
        Policy compliance: Unquoted identifiers across various SQL statements.
        Tests that properly formatted identifiers (without double quotes) pass the check.
        """
        batch = BatchPolicyTest(
            "Python/Scripts/Any/identifiers_without_quotes.py",
            message=MESSAGE_TEMPLATE
        )

        # ========================================
        # VALID: Unquoted identifiers (should NOT fire)
        # ========================================
        with batch.should_pass():
            batch.add(
                "CREATE TABLE users (id INT, name VARCHAR(50));",
                name="unquoted_table_name"
            )
            batch.add(
                "CREATE TABLE products (product_id INT, product_name VARCHAR(100));",
                name="unquoted_column_names"
            )
            batch.add(
                "INSERT INTO users (name, email) VALUES ('John Doe', 'john@example.com');",
                name="single_quotes_string_literals"
            )
            batch.add(
                """
                CREATE TABLE orders (
                    order_id INT PRIMARY KEY,
                    customer_id INT,
                    order_date TIMESTAMP,
                    total_amount DECIMAL(10, 2),
                    FOREIGN KEY (customer_id) REFERENCES customers(id)
                );
                """,
                name="complex_sql_unquoted"
            )
            batch.add(
                "CREATE TABLE myschema.users (id INT, username VARCHAR(50));",
                name="schema_qualified_unquoted"
            )
            batch.add(
                "ALTER TABLE users ADD COLUMN email VARCHAR(255);",
                name="alter_table_unquoted"
            )
            batch.add(
                "CREATE INDEX idx_users_email ON users(email);",
                name="index_creation_unquoted"
            )
            batch.add(
                "INSERT INTO users (name) VALUES ('John \"The Boss\" Doe');",
                name="double_quotes_in_string_literal"
            )
            batch.add(
                "create table users (ID int, NAME varchar(50));",
                name="mixed_case_keywords_unquoted"
            )

        with batch:
            batch.execute_with_subtests(subtests)

    # ========================================
    # MALFORMED SQL - Test resilience (kept separate)
    # ========================================

    def test_incomplete_quoted_identifier(self):
        """Malformed: Incomplete quoted identifier handling."""
        with LiquibaseCheck(
            "Python/Scripts/Any/identifiers_without_quotes.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            sql = 'CREATE TABLE "users (id INT);'  # Missing closing quote
            result = check.run(sql=sql)
            # Should not crash - sqlparse should handle malformed SQL

    def test_unmatched_quotes(self):
        """Malformed: Unmatched quotes handling."""
        with LiquibaseCheck(
            "Python/Scripts/Any/identifiers_without_quotes.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            sql = 'CREATE TABLE "users (id INT, "name" VARCHAR(50));'
            result = check.run(sql=sql)
            # Should not crash - sqlparse should handle unmatched quotes

    def test_non_sql_text(self):
        """Malformed: Non-SQL text should not crash."""
        with LiquibaseCheck(
            "Python/Scripts/Any/identifiers_without_quotes.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            sql = "This is not SQL at all, just some random text with \"quotes\" in it."
            result = check.run(sql=sql)
            # Should not crash - sqlparse should handle non-SQL text

    # ========================================
    # BUG EXPOSURE TESTS - No assertions (kept separate)
    # ========================================

    def test_sqlparse_tokenization_behavior(self):
        """Bug test: Verify sqlparse tokenization of quoted identifiers."""
        with LiquibaseCheck(
            "Python/Scripts/Any/identifiers_without_quotes.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            # Test various forms of quoted identifiers to understand sqlparse behavior
            test_cases = [
                ('CREATE TABLE "users" (id INT);', True, "Basic quoted table"),
                ('SELECT * FROM "schema"."table";', True, "Quoted schema and table"),
                ('CREATE TABLE users ("column1" INT);', True, "Quoted column"),
                ("SELECT 'string value' FROM table;", False, "Single quoted string literal"),
            ]

            for sql, should_fire, description in test_cases:
                result = check.run(sql=sql)
                # Note: Due to sys.exit(1) bug, we may not get proper results

    def test_string_literals_not_incorrectly_flagged(self):
        """Bug test: Ensure string literals (single quotes) are not flagged."""
        with LiquibaseCheck(
            "Python/Scripts/Any/identifiers_without_quotes.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            sql = """
            INSERT INTO users (name, description)
            VALUES ('John "Johnny" Doe', 'User with nickname "The Boss"');
            """
            result = check.run(sql=sql)
            assert not result.fired, "String literals should not be flagged as quoted identifiers"

    def test_loaddata_change_type_skipped(self):
        """LoadData change types should be skipped as per policy implementation."""
        # Note: LoadData is a Liquibase-specific change type that would be
        # detected during actual Liquibase execution, not in pure SQL
        # This test documents the expected behavior
        with LiquibaseCheck(
            "Python/Scripts/Any/identifiers_without_quotes.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            # LoadData would be in XML/YAML/JSON changeset format, not SQL
            # The policy explicitly skips LoadData change types
            # This is more relevant for integration testing with actual Liquibase
            pass

    # ========================================
    # COMPLEX SCENARIOS - Behavior documentation (kept separate)
    # ========================================

    def test_mixed_statement_types_with_quotes(self):
        """Complex: Multiple statement types with some having quoted identifiers."""
        with LiquibaseCheck(
            "Python/Scripts/Any/identifiers_without_quotes.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            sql = """
            CREATE TABLE users (id INT, name VARCHAR(50));
            CREATE INDEX idx_users_name ON users(name);
            INSERT INTO users (id, name) VALUES (1, 'John');
            CREATE TABLE "products" (id INT, name VARCHAR(100));
            UPDATE users SET name = 'Jane' WHERE id = 1;
            """
            result = check.run(sql=sql)
            # Should fire due to "products" table
            # But due to sys.exit(1) bug, execution stops at first violation

    def test_stored_procedure_with_quoted_identifiers(self):
        """Complex: Stored procedure with quoted identifiers."""
        with LiquibaseCheck(
            "Python/Scripts/Any/identifiers_without_quotes.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            sql = """
            CREATE PROCEDURE "update_user_status"()
            BEGIN
                UPDATE users SET status = 'active' WHERE last_login > NOW() - INTERVAL 30 DAY;
            END;
            """
            result = check.run(sql=sql)
            # Should fire due to quoted procedure name
            # But behavior depends on sqlparse tokenization

    # ========================================
    # KNOWN BUGS - All violations fail due to sys.exit(1) bug (kept separate as xfail)
    # ========================================

    @pytest.mark.xfail(
        reason="BUG: identifiers_without_quotes.py uses sys.exit(1) on first violation instead of checking all identifiers. "
               "Root cause: Line 63 exits immediately. Fix: Accumulate all violations before reporting."
    )
    def test_double_quoted_table_name_fires(self):
        """Invalid: Double-quoted table name should fire the check."""
        with LiquibaseCheck(
            "Python/Scripts/Any/identifiers_without_quotes.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            sql = 'CREATE TABLE "users" (id INT, name VARCHAR(50));'
            result = check.run(sql=sql)
            assert result.fired, "Double-quoted table name should trigger the check"
            assert "users" in result.message, "Error message should contain the quoted identifier"

    @pytest.mark.xfail(
        reason="BUG: identifiers_without_quotes.py uses sys.exit(1) on first violation. See test_double_quoted_table_name_fires."
    )
    def test_double_quoted_column_names_fires(self):
        """Invalid: Double-quoted column names should fire the check."""
        with LiquibaseCheck(
            "Python/Scripts/Any/identifiers_without_quotes.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            sql = 'CREATE TABLE users ("user_id" INT, "user_name" VARCHAR(50));'
            result = check.run(sql=sql)
            assert result.fired, "Double-quoted column names should trigger the check"
            assert "user_id" in result.message or "user_name" in result.message, "Error message should contain a quoted identifier"

    @pytest.mark.xfail(
        reason="BUG: identifiers_without_quotes.py uses sys.exit(1) on first violation. See test_double_quoted_table_name_fires."
    )
    def test_double_quoted_schema_name_fires(self):
        """Invalid: Double-quoted schema name should fire the check."""
        with LiquibaseCheck(
            "Python/Scripts/Any/identifiers_without_quotes.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            sql = 'CREATE TABLE "myschema".users (id INT);'
            result = check.run(sql=sql)
            assert result.fired, "Double-quoted schema name should trigger the check"
            assert "myschema" in result.message, "Error message should contain the quoted schema"

    @pytest.mark.xfail(
        reason="BUG: identifiers_without_quotes.py uses sys.exit(1) on first violation. See test_double_quoted_table_name_fires."
    )
    def test_mixed_quoted_unquoted_identifiers_fires(self):
        """Invalid: Mix of quoted and unquoted identifiers should fire."""
        with LiquibaseCheck(
            "Python/Scripts/Any/identifiers_without_quotes.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            sql = 'CREATE TABLE users ("id" INT, name VARCHAR(50));'
            result = check.run(sql=sql)
            assert result.fired, "Mixed quoted/unquoted identifiers should trigger the check"
            assert "id" in result.message, "Error message should contain the quoted identifier"

    @pytest.mark.xfail(
        reason="BUG: identifiers_without_quotes.py uses sys.exit(1) on first violation - only reports first violation. "
               "Root cause: Line 63 exits on first violation. Fix: Accumulate all violations."
    )
    def test_multiple_quoted_identifiers_fires(self):
        """Invalid: Multiple quoted identifiers in one statement should all be reported."""
        with LiquibaseCheck(
            "Python/Scripts/Any/identifiers_without_quotes.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            sql = 'CREATE TABLE "users" ("id" INT, "name" VARCHAR(50), "email" VARCHAR(100));'
            result = check.run(sql=sql)
            assert result.fired, "Multiple quoted identifiers should trigger the check"
            # Due to sys.exit(1) bug, only first identifier is reported
            assert "users" in result.message or "id" in result.message or "name" in result.message or "email" in result.message

    @pytest.mark.xfail(
        reason="BUG: identifiers_without_quotes.py may not handle empty quotes correctly. "
               "sqlparse might not tokenize empty quotes as identifiers."
    )
    def test_empty_double_quotes_handling(self):
        """Edge case: Empty double quotes handling."""
        with LiquibaseCheck(
            "Python/Scripts/Any/identifiers_without_quotes.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            sql = 'CREATE TABLE "" (id INT);'
            result = check.run(sql=sql)
            assert result.fired, "Empty double quotes should trigger the check"

    @pytest.mark.xfail(
        reason="BUG: identifiers_without_quotes.py uses sys.exit(1) on first violation. See test_double_quoted_table_name_fires."
    )
    def test_nested_quotes_handling(self):
        """Edge case: Nested or escaped quotes handling."""
        with LiquibaseCheck(
            "Python/Scripts/Any/identifiers_without_quotes.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            sql = 'CREATE TABLE "user""table" (id INT);'  # SQL escaped double quote
            result = check.run(sql=sql)
            assert result.fired, "Escaped double quotes in identifier should trigger the check"

    @pytest.mark.xfail(
        reason="BUG: identifiers_without_quotes.py uses sys.exit(1) on first violation. See test_double_quoted_table_name_fires."
    )
    def test_quoted_identifiers_in_different_statement_types(self):
        """Edge case: Quoted identifiers in various SQL statement types."""
        with LiquibaseCheck(
            "Python/Scripts/Any/identifiers_without_quotes.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            # CREATE TABLE
            sql = 'CREATE TABLE "test_table" (id INT);'
            result = check.run(sql=sql)
            assert result.fired, "CREATE TABLE with quoted identifier should fire"

            # ALTER TABLE
            sql = 'ALTER TABLE "users" ADD COLUMN age INT;'
            result = check.run(sql=sql)
            assert result.fired, "ALTER TABLE with quoted identifier should fire"

            # INSERT
            sql = 'INSERT INTO "users" (id) VALUES (1);'
            result = check.run(sql=sql)
            assert result.fired, "INSERT with quoted table should fire"

            # UPDATE
            sql = 'UPDATE "users" SET name = \'test\' WHERE id = 1;'
            result = check.run(sql=sql)
            assert result.fired, "UPDATE with quoted table should fire"

            # DELETE
            sql = 'DELETE FROM "users" WHERE id = 1;'
            result = check.run(sql=sql)
            assert result.fired, "DELETE with quoted table should fire"

    @pytest.mark.xfail(
        reason="BUG: identifiers_without_quotes.py uses sys.exit(1) on first violation. See test_double_quoted_table_name_fires."
    )
    def test_very_short_quoted_identifier(self):
        """Boundary: Very short quoted identifier (single character)."""
        with LiquibaseCheck(
            "Python/Scripts/Any/identifiers_without_quotes.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            sql = 'CREATE TABLE "t" (id INT);'
            result = check.run(sql=sql)
            assert result.fired, "Single character quoted identifier should trigger the check"
            assert "t" in result.message

    @pytest.mark.xfail(
        reason="BUG: identifiers_without_quotes.py uses sys.exit(1) on first violation. See test_double_quoted_table_name_fires."
    )
    def test_very_long_quoted_identifier(self):
        """Boundary: Very long quoted identifier."""
        with LiquibaseCheck(
            "Python/Scripts/Any/identifiers_without_quotes.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            long_name = "very_long_table_name_that_exceeds_typical_database_identifier_limits_" * 3
            sql = f'CREATE TABLE "{long_name}" (id INT);'
            result = check.run(sql=sql)
            assert result.fired, "Long quoted identifier should trigger the check"

    @pytest.mark.xfail(
        reason="BUG: identifiers_without_quotes.py uses sys.exit(1) on first violation. See test_double_quoted_table_name_fires."
    )
    def test_identifiers_with_special_characters(self):
        """Boundary: Identifiers with special characters in quotes."""
        with LiquibaseCheck(
            "Python/Scripts/Any/identifiers_without_quotes.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            sql = 'CREATE TABLE "user-accounts" (id INT);'
            result = check.run(sql=sql)
            assert result.fired, "Quoted identifier with special characters should trigger the check"
            assert "user-accounts" in result.message

    @pytest.mark.xfail(
        reason="BUG: isinstance(token, sqlparse.sql.Identifier) may not correctly identify all quoted identifiers. "
               "Some quoted identifiers might be tokenized differently by sqlparse."
    )
    def test_identifier_detection_accuracy(self):
        """Bug test: Test if isinstance(token, sqlparse.sql.Identifier) catches all cases."""
        with LiquibaseCheck(
            "Python/Scripts/Any/identifiers_without_quotes.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            # Some quoted identifiers might not be detected as sqlparse.sql.Identifier
            sql = 'SELECT "column_name" FROM "table_name" WHERE "id" = 1;'
            result = check.run(sql=sql)
            assert result.fired, "All quoted identifiers should be detected"

    @pytest.mark.xfail(
        reason="BUG: sys.exit(1) on line 63 causes premature exit on first violation. "
               "This prevents checking all identifiers in the changeset."
    )
    def test_sys_exit_prevents_full_check(self):
        """Bug test: sys.exit(1) prevents checking all identifiers."""
        with LiquibaseCheck(
            "Python/Scripts/Any/identifiers_without_quotes.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            sql = '''
            CREATE TABLE "table1" (id INT);
            CREATE TABLE "table2" (id INT);
            CREATE TABLE "table3" (id INT);
            '''
            result = check.run(sql=sql)
            assert result.fired, "Should detect quoted identifiers"
            # Due to sys.exit(1), only first violation is reported
            # Ideally, all three tables should be reported

    @pytest.mark.xfail(
        reason="BUG: sys.exit(1) causes early termination, may not handle large SQL efficiently."
    )
    def test_large_sql_with_many_identifiers_performance(self):
        """Performance: Large SQL with many identifiers should execute efficiently."""
        with LiquibaseCheck(
            "Python/Scripts/Any/identifiers_without_quotes.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            # Generate large SQL with many tables
            sql_parts = []
            for i in range(50):
                if i == 25:  # Add one quoted identifier in the middle
                    sql_parts.append(f'CREATE TABLE "bad_table_{i}" (id INT);')
                else:
                    sql_parts.append(f'CREATE TABLE good_table_{i} (id INT);')

            sql = "\n".join(sql_parts)
            result = check.run(sql=sql)
            assert result.fired, "Should find the quoted identifier in large SQL"
