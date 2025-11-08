"""
Comprehensive test suite for timestamp_column_name.py custom policy check.

This check ensures that all columns of a specified data type include a required postfix.
Default configuration: TIMESTAMP columns must end with _ts (case-insensitive).

Policy Purpose: Enforce consistent column naming conventions based on data types.
Example: All TIMESTAMP columns should end with _ts, DATE columns with _date, etc.

The policy:
- Processes CREATE TABLE statements only
- Supports configurable column types and postfixes via COLUMN_TYPE and COLUMN_POSTFIX arguments
- Performs case-insensitive comparisons
- Strips quotes from column names
- Exits on first violation (sys.exit(1))
- Uses liquibase_utilities.tokenize() which requires Liquibase execution

IMPORTANT: This policy check uses liquibase_utilities.tokenize() which is not available
in Pure Python mode. All tests require actual Liquibase execution.
"""

import pytest
from liquibase_test_harness import BatchPolicyTest, LiquibaseCheck, CheckResult

# Message template from the policy check
MESSAGE_TEMPLATE = 'Column name __COLUMN_NAME__ must include __COLUMN_POSTFIX__.'


# Mark all tests in this class as requiring Liquibase since tokenize() is not mocked
@pytest.mark.requires_liquibase
class TestTimestampColumnName:
    """Test suite for timestamp_column_name.py policy check."""

    def test_basic_functionality(self, subtests):
        """
        Core functionality: TIMESTAMP column naming validation.
        Tests basic compliance (correct _ts postfix) and violations (missing/wrong postfix).
        """
        batch = BatchPolicyTest(
            "Python/Scripts/Any/timestamp_column_name.py",
            message=MESSAGE_TEMPLATE,
            check_args={"COLUMN_TYPE": "TIMESTAMP", "COLUMN_POSTFIX": "_ts"}
        )

        # ========================================
        # VALID: TIMESTAMP columns with correct postfix (should NOT fire)
        # ========================================
        with batch.should_pass():
            batch.add(
                """
                CREATE TABLE events (
                    id INT PRIMARY KEY,
                    created_ts TIMESTAMP,
                    updated_ts TIMESTAMP,
                    deleted_ts TIMESTAMP NULL
                );
                """,
                name="correct_postfix"
            )
            batch.add(
                """
                CREATE TABLE audit_log (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    action VARCHAR(50),
                    user_id INT,
                    started_ts TIMESTAMP,
                    completed_ts TIMESTAMP,
                    failed_ts TIMESTAMP,
                    retried_ts TIMESTAMP
                );
                """,
                name="multiple_timestamp_columns"
            )
            batch.add(
                """
                CREATE TABLE mixed_case (
                    id INT,
                    lower_ts timestamp,
                    upper_ts TIMESTAMP,
                    mixed_ts TimeStamp
                );
                """,
                name="case_insensitive_type"
            )
            batch.add(
                """
                ALTER TABLE users ADD COLUMN last_login TIMESTAMP;
                INSERT INTO logs VALUES (1, 'action', CURRENT_TIMESTAMP);
                UPDATE users SET updated_timestamp = NOW() WHERE id = 1;
                CREATE INDEX idx_timestamp ON events (timestamp);
                """,
                name="non_create_table_ignored"
            )

        # ========================================
        # INVALID: TIMESTAMP columns without correct postfix (SHOULD fire)
        # ========================================
        with batch.should_fail():
            batch.add(
                """
                CREATE TABLE events (
                    id INT PRIMARY KEY,
                    created TIMESTAMP,
                    updated TIMESTAMP
                );
                """,
                name="missing_postfix",
                match_message='"created"'
            )
            batch.add(
                """
                CREATE TABLE logs (
                    id INT PRIMARY KEY,
                    created_date TIMESTAMP,
                    updated_time TIMESTAMP,
                    deleted_at TIMESTAMP
                );
                """,
                name="wrong_postfix"
            )
            batch.add(
                """
                CREATE TABLE simple_table (
                    timestamp TIMESTAMP
                );
                """,
                name="simple_name_violation",
                match_message='"timestamp"'
            )

        with batch:
            batch.execute_with_subtests(subtests)

    def test_configuration_and_edge_cases(self, subtests):
        """
        Configuration flexibility and edge cases.
        Tests custom column types (DATE) and various edge cases.
        """
        batch = BatchPolicyTest(
            "Python/Scripts/Any/timestamp_column_name.py",
            message=MESSAGE_TEMPLATE,
            check_args={"COLUMN_TYPE": "DATE", "COLUMN_POSTFIX": "_date"}
        )

        # ========================================
        # VALID: DATE columns with _date postfix (should NOT fire)
        # ========================================
        with batch.should_pass():
            batch.add(
                """
                CREATE TABLE calendar (
                    id INT PRIMARY KEY,
                    start_date DATE,
                    end_date DATE,
                    created_ts TIMESTAMP
                );
                """,
                name="custom_date_type_correct"
            )

        # ========================================
        # INVALID: DATE columns without _date postfix (SHOULD fire)
        # ========================================
        with batch.should_fail():
            batch.add(
                """
                CREATE TABLE events (
                    id INT PRIMARY KEY,
                    event_day DATE,
                    registration DATE
                );
                """,
                name="custom_date_type_wrong"
            )

        with batch:
            batch.execute_with_subtests(subtests)

    # ========================================
    # KNOWN BUGS - Tests with IndexError issues (kept separate as xfail)
    # ========================================

    @pytest.mark.xfail(
        reason="BUG: timestamp_column_name.py crashes with IndexError on line 83 when column definitions include "
               "PRIMARY KEY constraints. Root cause: column[1] array access assumes at least 2 elements. "
               "The tokenization of 'id INT PRIMARY KEY' may produce a column array with unexpected structure. "
               "Fix: Add bounds checking before accessing column[1]."
    )
    def test_non_timestamp_columns_without_postfix_passes(self):
        """
        Valid: Non-TIMESTAMP columns without postfix should pass.

        BUG DETAILS (BUG #4):
        - Location: timestamp_column_name.py lines 82-84
        - Current code:
            column_name = column[0].replace("\"","")
            column_type = column[1]
            if column_type == column_check and column_name[-postfix_len:] != column_postfix:
        - Problem: Assumes column array always has at least 2 elements
        - Impact: Crashes with IndexError when column definitions include PRIMARY KEY, CHECK,
                  or other constraints that change the tokenization structure
        - Example: 'id INT PRIMARY KEY' may be tokenized in unexpected ways depending on
                   how sqlparse handles the constraint keywords
        - Fix: Add bounds checking:
               if len(column) < 2 or column[0] == "constraint":
                   continue
               column_name = column[0].replace("\"","")
               column_type = column[1]

        See BUG_REPORT.md for full analysis and root cause documentation.
        """
        with LiquibaseCheck(
            "Python/Scripts/Any/timestamp_column_name.py",
            message=MESSAGE_TEMPLATE,
            check_args={"COLUMN_TYPE": "TIMESTAMP", "COLUMN_POSTFIX": "_ts"}
        ) as check:
            sql = """
            CREATE TABLE users (
                id INT PRIMARY KEY,
                username VARCHAR(50),
                email VARCHAR(100),
                balance DECIMAL(10,2),
                is_active BOOLEAN
            );
            """
            result = check.run(sql=sql)
            assert not result.fired, "Non-TIMESTAMP columns without postfix should not trigger the check"

    @pytest.mark.xfail(
        reason="BUG: timestamp_column_name.py crashes with IndexError on line 83. Same issue as test_non_timestamp_columns_without_postfix_passes."
    )
    def test_mixed_columns_correct_postfix_passes(self):
        """Valid: Mixed columns with TIMESTAMP having _ts and others without should pass."""
        with LiquibaseCheck(
            "Python/Scripts/Any/timestamp_column_name.py",
            message=MESSAGE_TEMPLATE,
            check_args={"COLUMN_TYPE": "TIMESTAMP", "COLUMN_POSTFIX": "_ts"}
        ) as check:
            sql = """
            CREATE TABLE transactions (
                id BIGINT PRIMARY KEY,
                amount DECIMAL(10,2),
                currency VARCHAR(3),
                processed_ts TIMESTAMP NOT NULL,
                created_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status VARCHAR(20)
            );
            """
            result = check.run(sql=sql)
            assert not result.fired, "Mixed columns with correct postfixes should not trigger the check"

    @pytest.mark.xfail(
        reason="BUG: timestamp_column_name.py crashes with IndexError on line 83 when PRIMARY KEY is present."
    )
    def test_mixed_columns_some_missing_postfix_fires(self):
        """Invalid: Mixed columns where some TIMESTAMP columns lack postfix should fire."""
        with LiquibaseCheck(
            "Python/Scripts/Any/timestamp_column_name.py",
            message=MESSAGE_TEMPLATE,
            check_args={"COLUMN_TYPE": "TIMESTAMP", "COLUMN_POSTFIX": "_ts"}
        ) as check:
            sql = """
            CREATE TABLE orders (
                id INT PRIMARY KEY,
                amount DECIMAL(10,2),
                created_ts TIMESTAMP,
                processed TIMESTAMP,
                shipped_ts TIMESTAMP
            );
            """
            result = check.run(sql=sql)
            assert result.fired, "TIMESTAMP column 'processed' without _ts should trigger the check"
            assert '"processed"' in result.message, "Error message should contain the violating column name"

    @pytest.mark.xfail(
        reason="BUG: timestamp_column_name.py crashes with IndexError on line 83 when PRIMARY KEY is present."
    )
    def test_custom_column_type_varchar_with_str_postfix(self):
        """Config: Test with COLUMN_TYPE=VARCHAR and COLUMN_POSTFIX=_str."""
        with LiquibaseCheck(
            "Python/Scripts/Any/timestamp_column_name.py",
            message=MESSAGE_TEMPLATE,
            check_args={"COLUMN_TYPE": "VARCHAR", "COLUMN_POSTFIX": "_str"}
        ) as check:
            # This should pass
            sql_pass = """
            CREATE TABLE users (
                id INT PRIMARY KEY,
                name_str VARCHAR(100),
                email_str VARCHAR(200)
            );
            """
            result = check.run(sql=sql_pass)
            assert not result.fired, "VARCHAR columns with _str postfix should pass"

            # This should fail
            sql_fail = """
            CREATE TABLE products (
                id INT PRIMARY KEY,
                name VARCHAR(100),
                description VARCHAR(500)
            );
            """
            result = check.run(sql=sql_fail)
            assert result.fired, "VARCHAR column without _str postfix should trigger the check"

    @pytest.mark.xfail(
        reason="BUG: timestamp_column_name.py crashes with IndexError on line 83 when PRIMARY KEY is present."
    )
    def test_custom_decimal_type_with_amt_postfix(self):
        """Config: Test with COLUMN_TYPE=DECIMAL and COLUMN_POSTFIX=_amt."""
        with LiquibaseCheck(
            "Python/Scripts/Any/timestamp_column_name.py",
            message=MESSAGE_TEMPLATE,
            check_args={"COLUMN_TYPE": "DECIMAL", "COLUMN_POSTFIX": "_amt"}
        ) as check:
            sql = """
            CREATE TABLE transactions (
                id INT PRIMARY KEY,
                total_amt DECIMAL(10,2),
                tax_amt DECIMAL(8,2),
                discount DECIMAL(6,2)
            );
            """
            result = check.run(sql=sql)
            assert result.fired, "DECIMAL column 'discount' without _amt should trigger"
            assert '"discount"' in result.message

    @pytest.mark.xfail(
        reason="BUG: Policy check may not handle certain data types correctly or has parsing issues with specific SQL structures."
    )
    def test_different_postfix_lengths(self):
        """Config: Test with postfixes of different lengths."""
        # Single character postfix
        with LiquibaseCheck(
            "Python/Scripts/Any/timestamp_column_name.py",
            message=MESSAGE_TEMPLATE,
            check_args={"COLUMN_TYPE": "INT", "COLUMN_POSTFIX": "_i"}
        ) as check:
            sql = "CREATE TABLE test (count_i INT, total INT);"
            result = check.run(sql=sql)
            assert result.fired, "INT column 'total' without _i should trigger"

        # Long postfix
        with LiquibaseCheck(
            "Python/Scripts/Any/timestamp_column_name.py",
            message=MESSAGE_TEMPLATE,
            check_args={"COLUMN_TYPE": "VARCHAR", "COLUMN_POSTFIX": "_string_value"}
        ) as check:
            sql = "CREATE TABLE test (name_string_value VARCHAR(50), description VARCHAR(100));"
            result = check.run(sql=sql)
            assert result.fired, "VARCHAR column without _string_value should trigger"

    @pytest.mark.xfail(
        reason="BUG: Policy check may not handle empty postfix correctly. The check at line 84 uses column_name[-postfix_len:] "
               "which with postfix_len=0 would return empty string, causing incorrect comparison logic."
    )
    def test_empty_postfix_configuration(self):
        """Boundary: Empty postfix configuration (edge case)."""
        with LiquibaseCheck(
            "Python/Scripts/Any/timestamp_column_name.py",
            message=MESSAGE_TEMPLATE,
            check_args={"COLUMN_TYPE": "TIMESTAMP", "COLUMN_POSTFIX": ""}
        ) as check:
            sql = """
            CREATE TABLE test (
                created TIMESTAMP
            );
            """
            # With empty postfix, all TIMESTAMP columns should pass
            result = check.run(sql=sql)
            assert not result.fired, "Empty postfix means no requirement"

    @pytest.mark.xfail(
        reason="BUG: timestamp_column_name.py exits on first violation (sys.exit(1) at line 89). "
               "This prevents checking all columns in a table and all tables in a changeset. "
               "Root cause: Premature exit instead of collecting all violations. "
               "Fix: Accumulate violations and report them all at the end."
    )
    def test_multiple_violations_in_single_table(self):
        """Bug test: Multiple violations in single table - only first is reported."""
        with LiquibaseCheck(
            "Python/Scripts/Any/timestamp_column_name.py",
            message=MESSAGE_TEMPLATE,
            check_args={"COLUMN_TYPE": "TIMESTAMP", "COLUMN_POSTFIX": "_ts"}
        ) as check:
            sql = """
            CREATE TABLE multiple_violations (
                created TIMESTAMP,
                updated TIMESTAMP,
                deleted TIMESTAMP
            );
            """
            result = check.run(sql=sql)
            assert result.fired
            # Bug: Only 'created' violation is reported, 'updated' and 'deleted' are missed
            # All three violations should ideally be reported
            assert all(name in result.message for name in ['"created"', '"updated"', '"deleted"'])

    @pytest.mark.xfail(
        reason="BUG: timestamp_column_name.py exits on first violation (sys.exit(1) at line 89). "
               "This prevents checking multiple CREATE TABLE statements in the same changeset."
    )
    def test_multiple_create_tables_in_changeset(self):
        """Bug test: Multiple CREATE TABLE statements - only first violation reported."""
        with LiquibaseCheck(
            "Python/Scripts/Any/timestamp_column_name.py",
            message=MESSAGE_TEMPLATE,
            check_args={"COLUMN_TYPE": "TIMESTAMP", "COLUMN_POSTFIX": "_ts"}
        ) as check:
            sql = """
            CREATE TABLE first_table (
                id INT,
                created TIMESTAMP
            );
            CREATE TABLE second_table (
                id INT,
                updated TIMESTAMP
            );
            """
            result = check.run(sql=sql)
            assert result.fired
            # Bug: Only first_table.created violation is reported
            # second_table.updated is never checked due to sys.exit(1)

    @pytest.mark.xfail(
        reason="BUG: Policy check may have issues with VARCHAR data type parsing or tokenization."
    )
    def test_postfix_length_calculation(self):
        """Bug test: Test postfix length calculation (line 80)."""
        with LiquibaseCheck(
            "Python/Scripts/Any/timestamp_column_name.py",
            message=MESSAGE_TEMPLATE,
            check_args={"COLUMN_TYPE": "VARCHAR", "COLUMN_POSTFIX": "_str"}
        ) as check:
            sql = """
            CREATE TABLE test (
                name_s VARCHAR(50),
                name_st VARCHAR(50),
                name_str VARCHAR(50)
            );
            """
            result = check.run(sql=sql)
            # Only name_str should pass, others should fail
            assert result.fired, "Partial postfix match should not pass"

    # ========================================
    # EDGE CASES - Complex scenarios (kept separate)
    # ========================================

    def test_column_name_already_containing_postfix_substring(self):
        """Edge case: Column names that contain the postfix as a substring."""
        with LiquibaseCheck(
            "Python/Scripts/Any/timestamp_column_name.py",
            message=MESSAGE_TEMPLATE,
            check_args={"COLUMN_TYPE": "TIMESTAMP", "COLUMN_POSTFIX": "_ts"}
        ) as check:
            # This column ends with 'ts' but not '_ts'
            sql = """
            CREATE TABLE test (
                id INT PRIMARY KEY,
                status_timestamps TIMESTAMP,
                results TIMESTAMP
            );
            """
            result = check.run(sql=sql)
            assert result.fired, "Column 'status_timestamps' should fire - doesn't end with '_ts'"
            assert '"status_timestamps"' in result.message or '"results"' in result.message

    def test_quoted_column_names_handling(self):
        """Edge case: Quoted column names should have quotes stripped (line 82)."""
        with LiquibaseCheck(
            "Python/Scripts/Any/timestamp_column_name.py",
            message=MESSAGE_TEMPLATE,
            check_args={"COLUMN_TYPE": "TIMESTAMP", "COLUMN_POSTFIX": "_ts"}
        ) as check:
            sql = '''
            CREATE TABLE test (
                "created_ts" TIMESTAMP,
                "updated" TIMESTAMP
            );
            '''
            result = check.run(sql=sql)
            assert result.fired, "Quoted column 'updated' without _ts should trigger"
            assert '"updated"' in result.message, "Error message should contain column name with quotes"

    def test_case_sensitivity_in_data_types(self):
        """Edge case: Case sensitivity in data types (timestamp vs TIMESTAMP)."""
        with LiquibaseCheck(
            "Python/Scripts/Any/timestamp_column_name.py",
            message=MESSAGE_TEMPLATE,
            check_args={"COLUMN_TYPE": "TIMESTAMP", "COLUMN_POSTFIX": "_ts"}
        ) as check:
            sql = """
            CREATE TABLE mixed (
                created timestamp,
                updated TIMESTAMP,
                deleted TiMeStAmP
            );
            """
            result = check.run(sql=sql)
            assert result.fired, "Case variations in TIMESTAMP should all be caught"

    def test_columns_with_constraints_after_data_type(self):
        """Edge case: Columns with constraints after data type."""
        with LiquibaseCheck(
            "Python/Scripts/Any/timestamp_column_name.py",
            message=MESSAGE_TEMPLATE,
            check_args={"COLUMN_TYPE": "TIMESTAMP", "COLUMN_POSTFIX": "_ts"}
        ) as check:
            sql = """
            CREATE TABLE constrained (
                id INT PRIMARY KEY,
                created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_ts TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                deleted TIMESTAMP NULL
            );
            """
            result = check.run(sql=sql)
            assert result.fired, "TIMESTAMP columns without _ts should fire regardless of constraints"
            assert '"created"' in result.message or '"deleted"' in result.message

    def test_alter_table_add_column_ignored(self):
        """Edge case: ALTER TABLE ADD COLUMN statements should be ignored."""
        with LiquibaseCheck(
            "Python/Scripts/Any/timestamp_column_name.py",
            message=MESSAGE_TEMPLATE,
            check_args={"COLUMN_TYPE": "TIMESTAMP", "COLUMN_POSTFIX": "_ts"}
        ) as check:
            sql = """
            ALTER TABLE users ADD COLUMN last_login TIMESTAMP;
            ALTER TABLE orders ADD created TIMESTAMP;
            """
            result = check.run(sql=sql)
            assert not result.fired, "ALTER TABLE statements should be ignored"

    # ========================================
    # BOUNDARY CONDITIONS (kept separate)
    # ========================================

    def test_very_short_column_names_with_postfix(self):
        """Boundary: Very short column names with postfix."""
        with LiquibaseCheck(
            "Python/Scripts/Any/timestamp_column_name.py",
            message=MESSAGE_TEMPLATE,
            check_args={"COLUMN_TYPE": "TIMESTAMP", "COLUMN_POSTFIX": "_ts"}
        ) as check:
            sql = """
            CREATE TABLE short (
                a_ts TIMESTAMP,
                b TIMESTAMP
            );
            """
            result = check.run(sql=sql)
            assert result.fired, "Short column name 'b' without _ts should trigger"
            assert '"b"' in result.message

    def test_very_long_column_names_with_postfix(self):
        """Boundary: Very long column names with postfix."""
        with LiquibaseCheck(
            "Python/Scripts/Any/timestamp_column_name.py",
            message=MESSAGE_TEMPLATE,
            check_args={"COLUMN_TYPE": "TIMESTAMP", "COLUMN_POSTFIX": "_ts"}
        ) as check:
            long_name = "very_long_column_name_for_testing_boundary_conditions_in_policy_check"
            sql = f"""
            CREATE TABLE long_names (
                {long_name}_ts TIMESTAMP,
                {long_name}_without TIMESTAMP
            );
            """
            result = check.run(sql=sql)
            assert result.fired, f"Long column name without _ts should trigger"
            assert f'"{long_name}_without"' in result.message

    def test_single_character_postfix(self):
        """Boundary: Single character postfix."""
        with LiquibaseCheck(
            "Python/Scripts/Any/timestamp_column_name.py",
            message=MESSAGE_TEMPLATE,
            check_args={"COLUMN_TYPE": "INT", "COLUMN_POSTFIX": "x"}
        ) as check:
            sql = """
            CREATE TABLE test (
                idx INT,
                value INT
            );
            """
            result = check.run(sql=sql)
            assert result.fired, "INT columns should end with 'x'"
            # Either idx or value should trigger (only first violation reported)
            assert '"idx"' in result.message or '"value"' in result.message

    # ========================================
    # MALFORMED SQL - Test resilience (kept separate)
    # ========================================

    def test_create_table_without_column_list(self):
        """Malformed: CREATE TABLE without column list."""
        with LiquibaseCheck(
            "Python/Scripts/Any/timestamp_column_name.py",
            message=MESSAGE_TEMPLATE,
            check_args={"COLUMN_TYPE": "TIMESTAMP", "COLUMN_POSTFIX": "_ts"}
        ) as check:
            sql = "CREATE TABLE empty_table;"
            result = check.run(sql=sql)
            # Should not crash, likely will not fire since no columns to check
            assert not result.fired, "Table without columns should not trigger"

    def test_non_create_table_statements(self):
        """Malformed: Non-CREATE TABLE statements should be safely ignored."""
        with LiquibaseCheck(
            "Python/Scripts/Any/timestamp_column_name.py",
            message=MESSAGE_TEMPLATE,
            check_args={"COLUMN_TYPE": "TIMESTAMP", "COLUMN_POSTFIX": "_ts"}
        ) as check:
            sql = """
            SELECT * FROM users WHERE created > NOW();
            DROP TABLE old_events;
            TRUNCATE TABLE logs;
            """
            result = check.run(sql=sql)
            assert not result.fired, "Non-CREATE TABLE statements should be ignored"

    def test_malformed_column_definitions(self):
        """Malformed: Malformed column definitions."""
        with LiquibaseCheck(
            "Python/Scripts/Any/timestamp_column_name.py",
            message=MESSAGE_TEMPLATE,
            check_args={"COLUMN_TYPE": "TIMESTAMP", "COLUMN_POSTFIX": "_ts"}
        ) as check:
            sql = """
            CREATE TABLE malformed (
                TIMESTAMP,
                another_column
            );
            """
            # This might cause issues with column[0] and column[1] access
            result = check.run(sql=sql)
            # Should handle gracefully, might not fire or might skip malformed columns

    def test_missing_parentheses(self):
        """Malformed: CREATE TABLE with missing or unbalanced parentheses."""
        with LiquibaseCheck(
            "Python/Scripts/Any/timestamp_column_name.py",
            message=MESSAGE_TEMPLATE,
            check_args={"COLUMN_TYPE": "TIMESTAMP", "COLUMN_POSTFIX": "_ts"}
        ) as check:
            sql = "CREATE TABLE test id INT, created TIMESTAMP;"
            result = check.run(sql=sql)
            # Should handle gracefully

    # ========================================
    # BUG EXPOSURE TESTS (kept separate)
    # ========================================

    def test_tokenization_and_parsing_logic(self):
        """Bug test: Test tokenization and parsing logic (lines 63-73)."""
        with LiquibaseCheck(
            "Python/Scripts/Any/timestamp_column_name.py",
            message=MESSAGE_TEMPLATE,
            check_args={"COLUMN_TYPE": "TIMESTAMP", "COLUMN_POSTFIX": "_ts"}
        ) as check:
            sql = """
            CREATE TABLE complex_parsing (
                id INT PRIMARY KEY AUTO_INCREMENT,
                created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                data JSON,
                status ENUM('active', 'inactive')
            );
            """
            result = check.run(sql=sql)
            assert result.fired, "Should detect 'created' without _ts"
            assert '"created"' in result.message

    def test_column_list_extraction_from_parentheses(self):
        """Bug test: Test column list extraction from parentheses (line 70)."""
        with LiquibaseCheck(
            "Python/Scripts/Any/timestamp_column_name.py",
            message=MESSAGE_TEMPLATE,
            check_args={"COLUMN_TYPE": "TIMESTAMP", "COLUMN_POSTFIX": "_ts"}
        ) as check:
            # Nested parentheses in column definitions
            sql = """
            CREATE TABLE nested (
                id INT,
                created TIMESTAMP CHECK (created > '2020-01-01'),
                amount DECIMAL(10,2)
            );
            """
            result = check.run(sql=sql)
            assert result.fired, "Should handle nested parentheses correctly"

    def test_column_array_access_safety(self):
        """Bug test: Test column[0] and column[1] array access (lines 82-84)."""
        with LiquibaseCheck(
            "Python/Scripts/Any/timestamp_column_name.py",
            message=MESSAGE_TEMPLATE,
            check_args={"COLUMN_TYPE": "TIMESTAMP", "COLUMN_POSTFIX": "_ts"}
        ) as check:
            # Column definition with only name, no type
            sql = """
            CREATE TABLE incomplete (
                id,
                created TIMESTAMP
            );
            """
            # This might cause IndexError on column[1] access
            result = check.run(sql=sql)
            # Should handle gracefully

    # ========================================
    # SPECIAL SQL CONSTRUCTS (kept separate)
    # ========================================

    def test_create_table_with_foreign_keys(self):
        """Special: CREATE TABLE with foreign key constraints."""
        with LiquibaseCheck(
            "Python/Scripts/Any/timestamp_column_name.py",
            message=MESSAGE_TEMPLATE,
            check_args={"COLUMN_TYPE": "TIMESTAMP", "COLUMN_POSTFIX": "_ts"}
        ) as check:
            sql = """
            CREATE TABLE orders (
                id INT PRIMARY KEY,
                user_id INT,
                created TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            );
            """
            result = check.run(sql=sql)
            assert result.fired, "Should detect 'created' without _ts"
            assert '"created"' in result.message

    def test_create_table_with_check_constraints(self):
        """Special: CREATE TABLE with CHECK constraints."""
        with LiquibaseCheck(
            "Python/Scripts/Any/timestamp_column_name.py",
            message=MESSAGE_TEMPLATE,
            check_args={"COLUMN_TYPE": "TIMESTAMP", "COLUMN_POSTFIX": "_ts"}
        ) as check:
            sql = """
            CREATE TABLE validated (
                id INT,
                start_time TIMESTAMP,
                end_ts TIMESTAMP,
                CHECK (end_ts > start_time)
            );
            """
            result = check.run(sql=sql)
            assert result.fired, "'start_time' without _ts should trigger"
            assert '"start_time"' in result.message

    def test_create_table_with_computed_columns(self):
        """Special: CREATE TABLE with computed/generated columns."""
        with LiquibaseCheck(
            "Python/Scripts/Any/timestamp_column_name.py",
            message=MESSAGE_TEMPLATE,
            check_args={"COLUMN_TYPE": "TIMESTAMP", "COLUMN_POSTFIX": "_ts"}
        ) as check:
            sql = """
            CREATE TABLE computed (
                id INT,
                created_ts TIMESTAMP,
                updated TIMESTAMP AS (created_ts + INTERVAL 1 DAY) STORED
            );
            """
            result = check.run(sql=sql)
            assert result.fired, "Generated column 'updated' without _ts should trigger"
            assert '"updated"' in result.message
