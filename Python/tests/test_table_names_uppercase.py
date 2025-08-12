
"""
Comprehensive test suite for table_names_uppercase.py custom policy check.

This check enforces that table names must be uppercase during table creation.
Policy Intent: Ensure consistent naming conventions across the database schema.
"""

import pytest
from liquibase_test_harness import LiquibaseCheck

# Message template from README configuration
MESSAGE_TEMPLATE = "Table __TABLE_NAME__ must be UPPERCASE."


class TestTableNamesUppercase:
    """Test suite for table_names_uppercase.py policy check."""

    # ========================================
    # POLICY COMPLIANCE TESTS (Should NOT fire)
    # ========================================
    
    def test_basic_uppercase_table_passes(self):
        """Valid: Basic uppercase table name should pass."""
        with LiquibaseCheck(
            "custom_policychecks/Python/Scripts/Any/table_names_uppercase.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            sql = "CREATE TABLE USERS (id INT, name VARCHAR(50));"
            result = check.run(sql=sql)
            assert not result.fired, "Uppercase table name should not trigger the check"
        
    def test_uppercase_with_underscore_passes(self):
        """Valid: Uppercase table name with underscore should pass."""
        with LiquibaseCheck(
            "custom_policychecks/Python/Scripts/Any/table_names_uppercase.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            sql = "CREATE TABLE USER_ACCOUNTS (id INT, balance DECIMAL(10,2));"
            result = check.run(sql=sql)
            assert not result.fired, "Uppercase table name with underscore should not trigger the check"
        
    def test_create_or_replace_uppercase_passes(self):
        """Valid: CREATE OR REPLACE with uppercase table should pass."""
        with LiquibaseCheck(
            "custom_policychecks/Python/Scripts/Any/table_names_uppercase.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            sql = "CREATE OR REPLACE TABLE CUSTOMERS (id INT, email VARCHAR(100));"
            result = check.run(sql=sql)
            assert not result.fired, "CREATE OR REPLACE with uppercase should not trigger the check"
        
    def test_non_table_statements_ignored(self):
        """Valid: Non-CREATE TABLE statements should be ignored."""
        with LiquibaseCheck(
            "custom_policychecks/Python/Scripts/Any/table_names_uppercase.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            sql = """
            INSERT INTO users VALUES (1, 'test');
            UPDATE users SET name = 'updated' WHERE id = 1;
            DELETE FROM users WHERE id = 1;
            """
            result = check.run(sql=sql)
            assert not result.fired, "Non-CREATE TABLE statements should be ignored"

    # ========================================
    # POLICY VIOLATION TESTS (Should fire)
    # ========================================
    
    def test_all_lowercase_table_fires(self):
        """Invalid: All lowercase table name should fire the check."""
        with LiquibaseCheck(
            "custom_policychecks/Python/Scripts/Any/table_names_uppercase.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            sql = "CREATE TABLE users (id INT, name VARCHAR(50));"
            result = check.run(sql=sql)
            assert result.fired, "Lowercase table name should trigger the check"
            assert "Table" in result.message and "users" in result.message, "Error message should contain template with table name"
        
    def test_mixed_case_table_fires(self):
        """Invalid: Mixed case table name should fire the check."""
        with LiquibaseCheck(
            "custom_policychecks/Python/Scripts/Any/table_names_uppercase.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            sql = "CREATE TABLE Users (id INT, name VARCHAR(50));"
            result = check.run(sql=sql)
            assert result.fired, "Mixed case table name should trigger the check"
            assert "Table" in result.message and "Users" in result.message, "Error message should contain template with table name"
        
    def test_camelcase_table_fires(self):
        """Invalid: camelCase table name should fire the check."""
        with LiquibaseCheck(
            "custom_policychecks/Python/Scripts/Any/table_names_uppercase.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            sql = "CREATE TABLE myTableName (id INT, data TEXT);"
            result = check.run(sql=sql)
            assert result.fired, "camelCase table name should trigger the check"
            assert "Table" in result.message and "myTableName" in result.message, "Error message should contain template with table name"

    # ========================================
    # EDGE CASE TESTS
    # ========================================
    
    def test_schema_prefix_lowercase_fires(self):
        """Edge case: Schema prefix with lowercase table should fire."""
        with LiquibaseCheck(
            "custom_policychecks/Python/Scripts/Any/table_names_uppercase.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            sql = "CREATE TABLE myschema.users (id INT);"
            result = check.run(sql=sql)
            # BUG ANALYSIS: Current implementation doesn't handle schema prefixes
            # The check will extract "myschema.users" as table name and check if it's uppercase
            # This should probably extract just "users" and check that
            assert result.fired, "Should fire for lowercase table name even with schema"
        
    def test_quoted_identifier_handling(self):
        """Edge case: Quoted identifiers should be handled appropriately."""
        with LiquibaseCheck(
            "custom_policychecks/Python/Scripts/Any/table_names_uppercase.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            sql = 'CREATE TABLE "users" (id INT);'
            result = check.run(sql=sql)
            # BUG ANALYSIS: Current implementation doesn't handle quoted identifiers
            # It will check if "users" (including quotes) is uppercase, which it's not
            assert result.fired, "Should handle quoted identifiers appropriately"
        
    def test_multiple_create_statements(self):
        """Edge case: Multiple CREATE TABLE statements in one changeset."""
        with LiquibaseCheck(
            "custom_policychecks/Python/Scripts/Any/table_names_uppercase.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            sql = """
            CREATE TABLE VALID_TABLE (id INT);
            CREATE TABLE invalid_table (id INT);
            """
            result = check.run(sql=sql)
            assert result.fired, "Should fire if any table name is not uppercase"
        
    def test_malformed_sql_handling(self):
        """Edge case: Malformed SQL should not crash the check."""
        with LiquibaseCheck(
            "custom_policychecks/Python/Scripts/Any/table_names_uppercase.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            sql = "CREATE TABLE (id INT);"  # Missing table name
            result = check.run(sql=sql)
            # BUG ANALYSIS: Current implementation may crash on IndexError
            # if sql_list[index_table + 1] doesn't exist
            # This test will reveal if proper bounds checking is implemented
        
    def test_create_table_without_parentheses(self):
        """Edge case: CREATE TABLE statement without column definitions."""  
        with LiquibaseCheck(
            "custom_policychecks/Python/Scripts/Any/table_names_uppercase.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            sql = "CREATE TABLE TEMP_TABLE"
            result = check.run(sql=sql)
            assert not result.fired, "Uppercase table name without columns should pass"

    # ========================================
    # PERFORMANCE TESTS
    # ========================================
    
    def test_large_sql_performance(self):
        """Performance: Large SQL with many statements should execute efficiently."""
        with LiquibaseCheck(
            "custom_policychecks/Python/Scripts/Any/table_names_uppercase.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            # Generate large SQL with many valid statements and one invalid table
            sql_parts = ["CREATE TABLE VALID_TABLE_{} (id INT);".format(i) for i in range(50)]
            sql_parts.append("CREATE TABLE invalid_table (id INT);")  # This should trigger
            sql = "\n".join(sql_parts)
            
            result = check.run(sql=sql)
            assert result.fired, "Should find the invalid table name in large SQL"
            assert "Table" in result.message and "invalid_table" in result.message

    # ========================================
    # LIQUIBASE INTEGRATION TESTS
    # ========================================
    
    def test_changeset_processing(self):
        """Integration: Test that changeset processing works correctly."""
        with LiquibaseCheck(
            "custom_policychecks/Python/Scripts/Any/table_names_uppercase.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            changeset_xml = """
            <changeSet id="1" author="test">
                <createTable tableName="lowercase_table">
                    <column name="id" type="int"/>
                </createTable>
            </changeSet>
            """
            result = check.run(changeset=changeset_xml)
            # This tests the integration with actual Liquibase changeset processing
            assert result.fired, "XML changeset with lowercase table should trigger check"

    # ========================================
    # BUG EXPOSURE TESTS
    # ========================================
    
    def test_index_out_of_bounds_protection(self):
        """Bug test: Verify protection against IndexError when parsing SQL."""
        with LiquibaseCheck(
            "custom_policychecks/Python/Scripts/Any/table_names_uppercase.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            sql = "CREATE TABLE"  # Incomplete statement
            result = check.run(sql=sql)
            # BUG ANALYSIS: Line 47-48 in original code:
            # if index_table + 1 < len(sql_list):
            #     table_name = sql_list[index_table + 1]  
            # This should handle the case where there's no table name after "TABLE"
        
    def test_empty_sql_handling(self):
        """Bug test: Empty SQL should not cause issues."""
        with LiquibaseCheck(
            "custom_policychecks/Python/Scripts/Any/table_names_uppercase.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            result = check.run(sql="")
            assert not result.fired, "Empty SQL should not fire the check"
        
    def test_whitespace_only_sql(self):
        """Bug test: Whitespace-only SQL should be handled gracefully."""  
        with LiquibaseCheck(
            "custom_policychecks/Python/Scripts/Any/table_names_uppercase.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            result = check.run(sql="   \n\t   ")
            assert not result.fired, "Whitespace-only SQL should not fire the check"

    # ========================================
    # BOUNDARY CONDITION TESTS
    # ========================================
    
    def test_single_character_table_name(self):
        """Boundary: Single character table names."""
        with LiquibaseCheck(
            "custom_policychecks/Python/Scripts/Any/table_names_uppercase.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            sql_uppercase = "CREATE TABLE A (id INT);"
            result_upper = check.run(sql=sql_uppercase)
            assert not result_upper.fired, "Single uppercase character should pass"
            
            sql_lowercase = "CREATE TABLE a (id INT);"
            result_lower = check.run(sql=sql_lowercase)
            assert result_lower.fired, "Single lowercase character should fire"
        
    def test_numeric_table_name(self):
        """Boundary: Table names with numbers."""
        with LiquibaseCheck(
            "custom_policychecks/Python/Scripts/Any/table_names_uppercase.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            sql = "CREATE TABLE TABLE123 (id INT);"
            result = check.run(sql=sql)
            assert not result.fired, "Uppercase table name with numbers should pass"
        
    def test_table_name_with_special_characters(self):
        """Boundary: Table names with special characters (underscores)."""
        with LiquibaseCheck(
            "custom_policychecks/Python/Scripts/Any/table_names_uppercase.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            sql = "CREATE TABLE USER_ACCOUNT_DATA (id INT);"
            result = check.run(sql=sql)
            assert not result.fired, "Uppercase with underscores should pass"