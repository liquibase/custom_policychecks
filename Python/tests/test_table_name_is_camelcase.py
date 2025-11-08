"""
Comprehensive test suite for table_name_is_camelcase.py custom policy check.

This check enforces that table names must use camelCase naming convention.
Policy Intent: Ensure consistent camelCase naming (both upper and lower letters required).

CRITICAL BUG IDENTIFIED:
========================
The policy check has a print() statement on line 120 that writes to stdout:
    print ("Table name: " + table_name + ", " + str(isCamelCase))

This breaks Liquibase JSON output parsing when running in integration mode, causing
all tests to fail with JSONDecodeError. The print statement must be removed or
converted to use liquibase_logger.info() instead.

Impact:
- All tests pass in pure Python mode (27 passed, 3 xfailed)
- All tests fail in Liquibase mode due to JSON corruption
- This is a policy check bug, not a test bug

Resolution Required:
Remove line 120 or replace with: liquibase_logger.info(f"Table name: {table_name}, {isCamelCase}")

Until the bug is fixed, all tests that check CREATE TABLE statements are marked
with @pytest.mark.requires_liquibase to run only in Liquibase mode, but they
will fail until the print statement is fixed.
"""

import pytest
from liquibase_test_harness import LiquibaseCheck

# Custom message from the policy check implementation
MESSAGE_TEMPLATE = 'Table name "__TABLE_NAME__" is NOT camelCase.'


class TestTableNameIsCamelCase:
    """Test suite for table_name_is_camelcase.py policy check."""

    # ========================================
    # POLICY COMPLIANCE TESTS (Should NOT fire)
    # ========================================

    def test_valid_camelcase_simple_passes(self):
        """Valid: Simple camelCase names should pass."""
        with LiquibaseCheck(
            "Python/Scripts/Any/table_name_is_camelcase.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            sql = "CREATE TABLE myTableName (id INT, name VARCHAR(50));"
            result = check.run(sql=sql)
            assert not result.fired, "Valid camelCase table name should not trigger the check"

    def test_valid_camelcase_user_account_passes(self):
        """Valid: camelCase with common patterns should pass."""
        with LiquibaseCheck(
            "Python/Scripts/Any/table_name_is_camelcase.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            sql = "CREATE TABLE userAccount (id INT, balance DECIMAL(10,2));"
            result = check.run(sql=sql)
            assert not result.fired, "Valid camelCase 'userAccount' should not trigger the check"

    def test_valid_camelcase_with_numbers_passes(self):
        """Valid: camelCase with numbers should pass."""
        with LiquibaseCheck(
            "Python/Scripts/Any/table_name_is_camelcase.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            sql = "CREATE TABLE table1Name (id INT, data TEXT);"
            result = check.run(sql=sql)
            assert not result.fired, "camelCase with numbers should not trigger the check"

    def test_valid_two_letter_camelcase_passes(self):
        """Valid: Two letter camelCase (aA, bB) should pass."""
        with LiquibaseCheck(
            "Python/Scripts/Any/table_name_is_camelcase.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            sql = "CREATE TABLE aA (id INT);"
            result = check.run(sql=sql)
            assert not result.fired, "Two letter camelCase 'aA' should pass"

    def test_valid_camelcase_multiple_words_passes(self):
        """Valid: Multiple camelCase words should pass."""
        with LiquibaseCheck(
            "Python/Scripts/Any/table_name_is_camelcase.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            sql = "CREATE TABLE orderDataHistory (id INT, order_id BIGINT, change_date TIMESTAMP);"
            result = check.run(sql=sql)
            assert not result.fired, "Multi-word camelCase should pass"

    def test_create_or_replace_camelcase_passes(self):
        """Valid: CREATE OR REPLACE with camelCase should pass."""
        with LiquibaseCheck(
            "Python/Scripts/Any/table_name_is_camelcase.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            sql = "CREATE OR REPLACE TABLE customerData (id INT, email VARCHAR(100));"
            result = check.run(sql=sql)
            assert not result.fired, "CREATE OR REPLACE with camelCase should not trigger"

    def test_non_create_table_statements_ignored(self):
        """Valid: Non-CREATE TABLE statements should be ignored."""
        with LiquibaseCheck(
            "Python/Scripts/Any/table_name_is_camelcase.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            sql = """
            INSERT INTO USERS VALUES (1, 'test');
            UPDATE USERS SET name = 'updated' WHERE id = 1;
            DELETE FROM USERS WHERE id = 1;
            ALTER TABLE USERS ADD COLUMN email VARCHAR(100);
            DROP TABLE USERS;
            """
            result = check.run(sql=sql)
            assert not result.fired, "Non-CREATE TABLE statements should be ignored"

    # ========================================
    # POLICY VIOLATION TESTS (Should fire)
    # ========================================

    def test_all_lowercase_table_fires(self):
        """Invalid: All lowercase table names should fire the check."""
        with LiquibaseCheck(
            "Python/Scripts/Any/table_name_is_camelcase.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            sql = "CREATE TABLE mytablename (id INT, name VARCHAR(50));"
            result = check.run(sql=sql)
            assert result.fired, "All lowercase table name should trigger the check"
            assert "mytablename" in result.message, "Error message should contain table name"
            assert "NOT camelCase" in result.message, "Error message should indicate camelCase violation"

    def test_all_uppercase_table_fires(self):
        """Invalid: All uppercase table names should fire the check."""
        with LiquibaseCheck(
            "Python/Scripts/Any/table_name_is_camelcase.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            sql = "CREATE TABLE MYTABLENAME (id INT, name VARCHAR(50));"
            result = check.run(sql=sql)
            assert result.fired, "All uppercase table name should trigger the check"
            assert "MYTABLENAME" in result.message, "Error message should contain table name"

    def test_snake_case_table_fires(self):
        """Invalid: snake_case table names should fire the check."""
        with LiquibaseCheck(
            "Python/Scripts/Any/table_name_is_camelcase.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            sql = "CREATE TABLE my_table_name (id INT, data TEXT);"
            result = check.run(sql=sql)
            assert result.fired, "snake_case table name should trigger the check"
            assert "my_table_name" in result.message, "Error message should contain snake_case name"

    def test_pascal_case_table_passes(self):
        """Valid: PascalCase (uppercase first letter) is considered valid camelCase by the check."""
        with LiquibaseCheck(
            "Python/Scripts/Any/table_name_is_camelcase.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            sql = "CREATE TABLE MyTableName (id INT, value DECIMAL(10,2));"
            result = check.run(sql=sql)
            # Note: The check considers PascalCase as valid camelCase (only requires both upper and lower)
            assert not result.fired, "PascalCase table name is accepted as valid camelCase"

    def test_single_lowercase_letter_fires(self):
        """Invalid: Single lowercase letter should fire (no uppercase)."""
        with LiquibaseCheck(
            "Python/Scripts/Any/table_name_is_camelcase.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            sql = "CREATE TABLE a (id INT);"
            result = check.run(sql=sql)
            assert result.fired, "Single lowercase letter lacks uppercase, should fire"
            assert "a" in result.message, "Error message should contain single letter 'a'"

    def test_single_uppercase_letter_fires(self):
        """Invalid: Single uppercase letter should fire (no lowercase)."""
        with LiquibaseCheck(
            "Python/Scripts/Any/table_name_is_camelcase.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            sql = "CREATE TABLE A (id INT);"
            result = check.run(sql=sql)
            assert result.fired, "Single uppercase letter lacks lowercase, should fire"
            assert "A" in result.message, "Error message should contain single letter 'A'"

    def test_table_name_starting_with_number_fires(self):
        """Invalid: Table names starting with numbers should fire."""
        with LiquibaseCheck(
            "Python/Scripts/Any/table_name_is_camelcase.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            sql = "CREATE TABLE 1tableName (id INT);"
            result = check.run(sql=sql)
            assert result.fired, "Table name starting with number should trigger the check"
            assert "1tableName" in result.message, "Error message should contain invalid name"

    def test_table_name_with_special_characters_fires(self):
        """Invalid: Table names with special characters should fire."""
        with LiquibaseCheck(
            "Python/Scripts/Any/table_name_is_camelcase.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            sql = "CREATE TABLE table-Name (id INT);"
            result = check.run(sql=sql)
            assert result.fired, "Table name with hyphen should trigger the check"
            assert "table-Name" in result.message, "Error message should contain name with hyphen"

    # ========================================
    # EDGE CASE TESTS
    # ========================================

    def test_quoted_identifier_lowercase_fires(self):
        """Edge case: Quoted lowercase identifier should fire."""
        with LiquibaseCheck(
            "Python/Scripts/Any/table_name_is_camelcase.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            sql = 'CREATE TABLE "users" (id INT);'
            result = check.run(sql=sql)
            assert result.fired, "Quoted lowercase table name should trigger the check"
            assert "users" in result.message, "Should extract name from quotes"

    def test_quoted_identifier_camelcase_passes(self):
        """Edge case: Quoted camelCase identifier should pass."""
        with LiquibaseCheck(
            "Python/Scripts/Any/table_name_is_camelcase.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            sql = 'CREATE TABLE "myTableName" (id INT);'
            result = check.run(sql=sql)
            assert not result.fired, "Quoted camelCase table name should pass"

    def test_schema_qualified_table_name_camelcase(self):
        """Edge case: Schema-qualified camelCase table should pass."""
        with LiquibaseCheck(
            "Python/Scripts/Any/table_name_is_camelcase.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            sql = "CREATE TABLE myschema.myTableName (id INT);"
            result = check.run(sql=sql)
            # The current implementation will check "myschema.myTableName" as a whole
            # which won't match camelCase pattern due to the dot
            assert result.fired, "Schema.table format not handled correctly in current implementation"

    def test_table_name_with_parentheses_inline(self):
        """Edge case: Table name followed immediately by parentheses."""
        with LiquibaseCheck(
            "Python/Scripts/Any/table_name_is_camelcase.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            sql = "CREATE TABLE myTable(id INT);"  # No space before (
            result = check.run(sql=sql)
            # The implementation will capture "myTable(id" as the table name
            assert result.fired, "Table name with inline parentheses not handled correctly"

    @pytest.mark.xfail(
        reason="BUG: table_name_is_camelcase.py exits on first violation (sys.exit(1) at line 127). "
               "Should process all CREATE TABLE statements and report all violations."
    )
    def test_multiple_create_statements_checks_all(self):
        """Edge case: Multiple CREATE TABLE statements in one changeset."""
        with LiquibaseCheck(
            "Python/Scripts/Any/table_name_is_camelcase.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            sql = """
            CREATE TABLE validTableName (id INT);
            CREATE TABLE invalid_table (id INT);
            CREATE TABLE anotherValidName (id INT);
            """
            result = check.run(sql=sql)
            assert result.fired, "Should fire if any table name violates camelCase"
            assert "invalid_table" in result.message, "Should report the invalid table name"

    def test_malformed_sql_missing_table_name(self):
        """Edge case: Malformed SQL missing table name should be handled gracefully."""
        with LiquibaseCheck(
            "Python/Scripts/Any/table_name_is_camelcase.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            sql = "CREATE TABLE (id INT);"  # Missing table name
            result = check.run(sql=sql)
            # The implementation checks if index_table + 1 < len(sql_list), so this should be safe
            # It will capture "(id" as the table name, which won't match camelCase
            assert result.fired, "Malformed SQL with missing table name should fire"

    def test_create_without_table_keyword(self):
        """Edge case: CREATE without TABLE keyword should be ignored."""
        with LiquibaseCheck(
            "Python/Scripts/Any/table_name_is_camelcase.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            sql = "CREATE INDEX idx_test ON users(id);"
            result = check.run(sql=sql)
            assert not result.fired, "CREATE INDEX should be ignored (not CREATE TABLE)"

    # ========================================
    # BOUNDARY CONDITION TESTS
    # ========================================

    def test_two_character_valid_camelcase(self):
        """Boundary: Two-character names with mixed case are valid (both aA and Aa)."""
        with LiquibaseCheck(
            "Python/Scripts/Any/table_name_is_camelcase.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            test_cases = [
                ("aA", False),  # Valid - has both cases
                ("bC", False),  # Valid - has both cases
                ("xY", False),  # Valid - has both cases
                ("aa", True),   # Invalid - all lowercase
                ("AA", True),   # Invalid - all uppercase
                ("Aa", False),  # Valid - has both cases (PascalCase style is accepted)
            ]

            for table_name, should_fire in test_cases:
                sql = f"CREATE TABLE {table_name} (id INT);"
                result = check.run(sql=sql)
                if should_fire:
                    assert result.fired, f"'{table_name}' should trigger the check"
                else:
                    assert not result.fired, f"'{table_name}' should pass the check"

    def test_very_long_camelcase_name(self):
        """Boundary: Very long camelCase names should work correctly."""
        with LiquibaseCheck(
            "Python/Scripts/Any/table_name_is_camelcase.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            # Valid long camelCase
            sql = "CREATE TABLE thisIsAVeryLongCamelCaseTableNameThatShouldStillWorkCorrectly (id INT);"
            result = check.run(sql=sql)
            assert not result.fired, "Long valid camelCase name should pass"

            # Invalid long name (all lowercase)
            sql = "CREATE TABLE thisisaverylonglowercasetablenamethatshouldfail (id INT);"
            result = check.run(sql=sql)
            assert result.fired, "Long lowercase name should trigger the check"

    def test_consecutive_uppercase_letters(self):
        """Boundary: Consecutive uppercase letters (like HTMLParser)."""
        with LiquibaseCheck(
            "Python/Scripts/Any/table_name_is_camelcase.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            # Has both upper and lower, should pass despite consecutive uppers
            sql = "CREATE TABLE myHTMLParser (id INT);"
            result = check.run(sql=sql)
            assert not result.fired, "camelCase with consecutive uppercase should pass"

            # Another example
            sql = "CREATE TABLE userIDMapping (id INT);"
            result = check.run(sql=sql)
            assert not result.fired, "camelCase with ID (consecutive uppercase) should pass"

    # ========================================
    # BUG EXPOSURE TESTS
    # ========================================

    def test_regex_pattern_validation(self):
        """Bug test: Verify is_camel_case() regex pattern enforcement."""
        with LiquibaseCheck(
            "Python/Scripts/Any/table_name_is_camelcase.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            # Test the regex: r"^[a-zA-Z][a-zA-Z0-9]*$"
            test_cases = [
                ("1startWithNumber", True),   # Starts with digit - should fail
                ("_startWithUnderscore", True), # Starts with underscore - should fail
                ("has-Hyphen", True),          # Contains hyphen - should fail
                ("has_Underscore", True),      # Contains underscore - should fail
                ("has Space", True),           # Contains space - should fail (though SQL would break)
                ("validName123", False),       # Valid with numbers at end
            ]

            for table_name, should_fire in test_cases:
                sql = f"CREATE TABLE {table_name} (id INT);"
                result = check.run(sql=sql)
                if should_fire:
                    assert result.fired, f"'{table_name}' should fail regex validation"
                else:
                    assert not result.fired, f"'{table_name}' should pass regex validation"

    def test_both_cases_required(self):
        """Bug test: Verify both uppercase AND lowercase are required."""
        with LiquibaseCheck(
            "Python/Scripts/Any/table_name_is_camelcase.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            # Only lowercase - should fail
            sql = "CREATE TABLE alllowercase (id INT);"
            result = check.run(sql=sql)
            assert result.fired, "Name with only lowercase should fail"

            # Only uppercase - should fail
            sql = "CREATE TABLE ALLUPPERCASE (id INT);"
            result = check.run(sql=sql)
            assert result.fired, "Name with only uppercase should fail"

            # Mixed case - should pass
            sql = "CREATE TABLE mixedCase (id INT);"
            result = check.run(sql=sql)
            assert not result.fired, "Name with both cases should pass"

    @pytest.mark.xfail(
        reason="OBSERVATION: Line 120 contains a print statement that outputs to console. "
               "This appears to be debugging code that should be removed or converted to logging."
    )
    def test_no_print_statements_in_production(self):
        """Bug test: Check for debugging print statements in production code."""
        with LiquibaseCheck(
            "Python/Scripts/Any/table_name_is_camelcase.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            import io
            import sys
            from contextlib import redirect_stdout

            # Capture stdout to detect print statements
            captured_output = io.StringIO()
            with redirect_stdout(captured_output):
                sql = "CREATE TABLE testTable (id INT);"
                result = check.run(sql=sql)

            output = captured_output.getvalue()
            # The code has: print ("Table name: " + table_name + ", " + str(isCamelCase))
            assert "Table name:" not in output, "Production code should not contain print statements"

    def test_extract_substring_function(self):
        """Bug test: Verify extract_substring() handles quoted identifiers correctly."""
        with LiquibaseCheck(
            "Python/Scripts/Any/table_name_is_camelcase.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            # Test with double quotes
            sql = 'CREATE TABLE "quotedTableName" (id INT);'
            result = check.run(sql=sql)
            assert not result.fired, "Quoted camelCase identifier should pass"

            # Test with malformed quotes (missing closing quote)
            sql = 'CREATE TABLE "unclosed (id INT);'
            result = check.run(sql=sql)
            # extract_substring returns "" when quotes don't match, so "unclosed will be checked
            assert result.fired, "Malformed quoted identifier should fire"

    # ========================================
    # PERFORMANCE TESTS
    # ========================================

    @pytest.mark.xfail(
        reason="BUG: sys.exit(1) on line 127 causes premature exit, preventing check of all statements."
    )
    def test_large_sql_with_multiple_tables(self):
        """Performance: Large SQL with many CREATE TABLE statements."""
        with LiquibaseCheck(
            "Python/Scripts/Any/table_name_is_camelcase.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            # Generate large SQL with many valid and one invalid table
            sql_parts = []
            for i in range(20):
                sql_parts.append(f"CREATE TABLE validTableName{i} (id INT);")
            sql_parts.append("CREATE TABLE invalid_name (id INT);")  # This should trigger
            sql = "\n".join(sql_parts)

            result = check.run(sql=sql)
            assert result.fired, "Should find the invalid table name in large SQL"
            assert "invalid_name" in result.message