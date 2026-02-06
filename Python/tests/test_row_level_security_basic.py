"""
Comprehensive test suite for row_level_security_basic.py custom policy check.

This check enforces row-level security on shared configuration tables by validating
that DML operations (INSERT, UPDATE, DELETE) only affect records belonging to the
deploying team.

Policy Intent: Ensure teams can only modify their own records in shared tables,
preventing accidental or intentional cross-team data modifications.

Configuration Parameters:
- ENV_VAR_NAME: Environment variable containing team identifier (e.g., "TEAM_ID")
- PROTECTED_TABLES: Comma-separated list of protected tables
- TEAM_COLUMN: Column name identifying record ownership (e.g., "SOURCE", "SUBSYSTEM")
"""

import os
import pytest
from liquibase_test_harness import BatchPolicyTest, LiquibaseCheck

# Message template for violations
MESSAGE_TEMPLATE = "Row-level security violation: __OPERATION__ on table __TABLE_NAME__ must filter by __TEAM_COLUMN__ = '__TEAM_VALUE__'"


class TestRowLevelSecurityBasic:
    """Test suite for row_level_security_basic.py policy check."""

    def setup_method(self):
        """Setup test environment with team ID."""
        # Set up default environment variable for tests
        os.environ['TEAM_ID'] = 'RISK'
        os.environ['DEPLOY_TEAM'] = 'TRADING'

    def teardown_method(self):
        """Clean up environment variables after each test."""
        # Clean up any test environment variables
        for var in ['TEAM_ID', 'DEPLOY_TEAM', 'TEST_TEAM']:
            if var in os.environ:
                del os.environ[var]

    # =========================================================================
    # INSERT STATEMENT VALIDATION
    # =========================================================================

    def test_insert_statement_validation(self, subtests):
        """
        Core functionality: INSERT statement validation.
        Tests that INSERT statements include the team column with correct value.
        """
        batch = BatchPolicyTest(
            "Python/Scripts/Any/row_level_security_basic.py",
            message=MESSAGE_TEMPLATE,
            check_args={
                "ENV_VAR_NAME": "TEAM_ID",
                "PROTECTED_TABLES": "FRAMEWORK_CONFIG,JOB_DEFINITIONS,TEAM_SETTINGS",
                "TEAM_COLUMN": "SOURCE"
            }
        )

        # ========================================
        # VALID: INSERT statements with correct team value
        # ========================================
        with batch.should_pass():
            # Standard INSERT with team column
            batch.add(
                "INSERT INTO FRAMEWORK_CONFIG (job_name, SOURCE, enabled) VALUES ('risk_job', 'RISK', 1);",
                name="insert_with_correct_team"
            )

            # INSERT with team column in different position
            batch.add(
                "INSERT INTO JOB_DEFINITIONS (SOURCE, job_id, description) VALUES ('RISK', 101, 'Risk calculation job');",
                name="insert_team_column_first"
            )

            # INSERT with lowercase column names (case insensitive)
            batch.add(
                "INSERT INTO FRAMEWORK_CONFIG (job_name, source, enabled) VALUES ('risk_job_2', 'RISK', 1);",
                name="insert_lowercase_column"
            )

            # INSERT into non-protected table (should not be validated)
            batch.add(
                "INSERT INTO OTHER_TABLE (job_name, SOURCE, enabled) VALUES ('any_job', 'OTHER', 1);",
                name="insert_non_protected_table"
            )

            # Multiple column INSERT with team value
            batch.add(
                """INSERT INTO TEAM_SETTINGS
                   (setting_id, setting_name, SOURCE, value, created_date)
                   VALUES (1, 'max_threads', 'RISK', '10', CURRENT_DATE);""",
                name="insert_multiple_columns"
            )

        # ========================================
        # INVALID: INSERT statements violating row-level security
        # ========================================
        with batch.should_fail():
            # INSERT missing team column entirely
            batch.add(
                "INSERT INTO FRAMEWORK_CONFIG (job_name, enabled) VALUES ('risk_job', 1);",
                name="insert_missing_team_column",
                match_message="INSERT.*FRAMEWORK_CONFIG.*SOURCE.*RISK"
            )

            # INSERT with wrong team value
            batch.add(
                "INSERT INTO FRAMEWORK_CONFIG (job_name, SOURCE, enabled) VALUES ('risk_job', 'TRADING', 1);",
                name="insert_wrong_team_value",
                match_message="INSERT.*FRAMEWORK_CONFIG.*SOURCE.*RISK"
            )

            # INSERT with NULL team value
            batch.add(
                "INSERT INTO JOB_DEFINITIONS (job_id, SOURCE, description) VALUES (102, NULL, 'Some job');",
                name="insert_null_team_value",
                match_message="INSERT.*JOB_DEFINITIONS.*SOURCE.*RISK"
            )

            # INSERT with empty team value
            batch.add(
                "INSERT INTO TEAM_SETTINGS (setting_id, SOURCE, value) VALUES (2, '', 'value');",
                name="insert_empty_team_value",
                match_message="INSERT.*TEAM_SETTINGS.*SOURCE.*RISK"
            )

        with batch:
            batch.execute_with_subtests(subtests)

    # =========================================================================
    # UPDATE STATEMENT VALIDATION
    # =========================================================================

    def test_update_statement_validation(self, subtests):
        """
        Core functionality: UPDATE statement validation.
        Tests that UPDATE statements include team filtering in WHERE clause.
        """
        batch = BatchPolicyTest(
            "Python/Scripts/Any/row_level_security_basic.py",
            message=MESSAGE_TEMPLATE,
            check_args={
                "ENV_VAR_NAME": "TEAM_ID",
                "PROTECTED_TABLES": "FRAMEWORK_CONFIG,JOB_DEFINITIONS",
                "TEAM_COLUMN": "SOURCE"
            }
        )

        # ========================================
        # VALID: UPDATE statements with team filtering
        # ========================================
        with batch.should_pass():
            # Standard UPDATE with team filter
            batch.add(
                "UPDATE FRAMEWORK_CONFIG SET enabled = 1 WHERE job_name = 'risk_job' AND SOURCE = 'RISK';",
                name="update_with_team_filter"
            )

            # UPDATE with team filter first in WHERE
            batch.add(
                "UPDATE JOB_DEFINITIONS SET status = 'ACTIVE' WHERE SOURCE = 'RISK' AND job_id = 101;",
                name="update_team_filter_first"
            )

            # UPDATE with lowercase column name
            batch.add(
                "UPDATE FRAMEWORK_CONFIG SET enabled = 0 WHERE source = 'RISK' AND job_name LIKE 'risk_%';",
                name="update_lowercase_team_column"
            )

            # UPDATE non-protected table (should not be validated)
            batch.add(
                "UPDATE OTHER_TABLE SET status = 'ACTIVE' WHERE id = 1;",
                name="update_non_protected_table"
            )

            # Complex UPDATE with multiple conditions
            batch.add(
                """UPDATE FRAMEWORK_CONFIG
                   SET enabled = 1, last_modified = CURRENT_TIMESTAMP
                   WHERE SOURCE = 'RISK'
                     AND job_name IN ('job1', 'job2')
                     AND status != 'DISABLED';""",
                name="update_complex_conditions"
            )

        # ========================================
        # INVALID: UPDATE statements without proper team filtering
        # ========================================
        with batch.should_fail():
            # UPDATE without any WHERE clause
            batch.add(
                "UPDATE FRAMEWORK_CONFIG SET enabled = 1;",
                name="update_no_where_clause",
                match_message="UPDATE.*FRAMEWORK_CONFIG.*SOURCE.*RISK"
            )

            # UPDATE with WHERE but missing team filter
            batch.add(
                "UPDATE FRAMEWORK_CONFIG SET enabled = 0 WHERE job_name = 'some_job';",
                name="update_missing_team_filter",
                match_message="UPDATE.*FRAMEWORK_CONFIG.*SOURCE.*RISK"
            )

            # UPDATE with wrong team value
            batch.add(
                "UPDATE JOB_DEFINITIONS SET status = 'INACTIVE' WHERE SOURCE = 'TRADING' AND job_id = 101;",
                name="update_wrong_team_value",
                match_message="UPDATE.*JOB_DEFINITIONS.*SOURCE.*RISK"
            )

            # UPDATE with team column in SET but not WHERE
            batch.add(
                "UPDATE FRAMEWORK_CONFIG SET SOURCE = 'RISK', enabled = 1 WHERE job_name = 'job1';",
                name="update_team_in_set_not_where",
                match_message="UPDATE.*FRAMEWORK_CONFIG.*SOURCE.*RISK"
            )

        with batch:
            batch.execute_with_subtests(subtests)

    # =========================================================================
    # DELETE STATEMENT VALIDATION
    # =========================================================================

    def test_delete_statement_validation(self, subtests):
        """
        Core functionality: DELETE statement validation.
        Tests that DELETE statements include team filtering in WHERE clause.
        """
        batch = BatchPolicyTest(
            "Python/Scripts/Any/row_level_security_basic.py",
            message=MESSAGE_TEMPLATE,
            check_args={
                "ENV_VAR_NAME": "TEAM_ID",
                "PROTECTED_TABLES": "FRAMEWORK_CONFIG,JOB_DEFINITIONS,AUDIT_LOG",
                "TEAM_COLUMN": "SOURCE"
            }
        )

        # ========================================
        # VALID: DELETE statements with team filtering
        # ========================================
        with batch.should_pass():
            # Standard DELETE with team filter
            batch.add(
                "DELETE FROM FRAMEWORK_CONFIG WHERE job_name = 'old_job' AND SOURCE = 'RISK';",
                name="delete_with_team_filter"
            )

            # DELETE with team filter only
            batch.add(
                "DELETE FROM JOB_DEFINITIONS WHERE SOURCE = 'RISK';",
                name="delete_team_filter_only"
            )

            # DELETE with complex conditions
            batch.add(
                """DELETE FROM AUDIT_LOG
                   WHERE SOURCE = 'RISK'
                     AND created_date < DATE_SUB(CURRENT_DATE, INTERVAL 90 DAY)
                     AND status = 'ARCHIVED';""",
                name="delete_complex_conditions"
            )

            # DELETE from non-protected table
            batch.add(
                "DELETE FROM TEMP_TABLE WHERE id > 100;",
                name="delete_non_protected_table"
            )

            # DELETE with case variation
            batch.add(
                "DELETE FROM FRAMEWORK_CONFIG WHERE source = 'RISK' AND enabled = 0;",
                name="delete_lowercase_team_column"
            )

        # ========================================
        # INVALID: DELETE statements without proper team filtering
        # ========================================
        with batch.should_fail():
            # DELETE without WHERE clause (dangerous!)
            batch.add(
                "DELETE FROM FRAMEWORK_CONFIG;",
                name="delete_no_where_clause",
                match_message="DELETE.*FRAMEWORK_CONFIG.*SOURCE.*RISK"
            )

            # DELETE missing team filter
            batch.add(
                "DELETE FROM JOB_DEFINITIONS WHERE job_id = 999;",
                name="delete_missing_team_filter",
                match_message="DELETE.*JOB_DEFINITIONS.*SOURCE.*RISK"
            )

            # DELETE with wrong team value
            batch.add(
                "DELETE FROM AUDIT_LOG WHERE SOURCE = 'COMPLIANCE' AND status = 'OLD';",
                name="delete_wrong_team_value",
                match_message="DELETE.*AUDIT_LOG.*SOURCE.*RISK"
            )

            # DELETE with OR condition (potentially dangerous)
            batch.add(
                "DELETE FROM FRAMEWORK_CONFIG WHERE job_name = 'job1' OR SOURCE = 'RISK';",
                name="delete_with_or_condition",
                match_message="DELETE.*FRAMEWORK_CONFIG.*SOURCE.*RISK"
            )

        with batch:
            batch.execute_with_subtests(subtests)

    # =========================================================================
    # ENVIRONMENT VARIABLE HANDLING
    # =========================================================================

    def test_environment_variable_handling(self, subtests):
        """
        Test environment variable handling and configuration.
        Validates behavior with different env var configurations.
        """
        # Test with different environment variable
        os.environ['DEPLOY_TEAM'] = 'TRADING'

        batch = BatchPolicyTest(
            "Python/Scripts/Any/row_level_security_basic.py",
            message=MESSAGE_TEMPLATE,
            check_args={
                "ENV_VAR_NAME": "DEPLOY_TEAM",  # Using different env var
                "PROTECTED_TABLES": "FRAMEWORK_CONFIG",
                "TEAM_COLUMN": "SUBSYSTEM"  # Using different column name
            }
        )

        with batch.should_pass():
            # Correct team value from DEPLOY_TEAM env var
            batch.add(
                "INSERT INTO FRAMEWORK_CONFIG (job_id, SUBSYSTEM, status) VALUES (1, 'TRADING', 'ACTIVE');",
                name="env_var_correct_team"
            )

            batch.add(
                "UPDATE FRAMEWORK_CONFIG SET status = 'INACTIVE' WHERE SUBSYSTEM = 'TRADING' AND job_id = 1;",
                name="env_var_update_correct"
            )

        with batch.should_fail():
            # Wrong team value
            batch.add(
                "INSERT INTO FRAMEWORK_CONFIG (job_id, SUBSYSTEM, status) VALUES (2, 'RISK', 'ACTIVE');",
                name="env_var_wrong_team",
                match_message="INSERT.*FRAMEWORK_CONFIG.*SUBSYSTEM.*TRADING"
            )

        with batch:
            batch.execute_with_subtests(subtests)

    def test_missing_environment_variable(self):
        """
        Test behavior when environment variable is not set.
        The check should handle this gracefully.
        """
        # Remove all test environment variables
        for var in ['TEAM_ID', 'DEPLOY_TEAM', 'TEST_TEAM']:
            if var in os.environ:
                del os.environ[var]

        with LiquibaseCheck(
            "Python/Scripts/Any/row_level_security_basic.py",
            message=MESSAGE_TEMPLATE,
            check_args={
                "ENV_VAR_NAME": "NONEXISTENT_VAR",
                "PROTECTED_TABLES": "FRAMEWORK_CONFIG",
                "TEAM_COLUMN": "SOURCE"
            }
        ) as check:
            # The check should handle missing env var gracefully
            # Either by passing (no validation) or firing with a clear message
            sql = "INSERT INTO FRAMEWORK_CONFIG (job_name, SOURCE) VALUES ('test', 'ANY');"
            result = check.run(sql=sql)
            # We expect the check to handle this case - either pass or provide clear error

    # =========================================================================
    # TABLE FILTERING LOGIC
    # =========================================================================

    def test_table_filtering_logic(self, subtests):
        """
        Test that only protected tables are validated.
        Non-protected tables should pass through without validation.
        """
        os.environ['TEAM_ID'] = 'RISK'

        batch = BatchPolicyTest(
            "Python/Scripts/Any/row_level_security_basic.py",
            message=MESSAGE_TEMPLATE,
            check_args={
                "ENV_VAR_NAME": "TEAM_ID",
                "PROTECTED_TABLES": "FRAMEWORK_CONFIG,JOB_DEFINITIONS",  # Only these are protected
                "TEAM_COLUMN": "SOURCE"
            }
        )

        with batch.should_pass():
            # Operations on non-protected tables should pass
            batch.add(
                "INSERT INTO USER_TABLE (name, SOURCE) VALUES ('test', 'OTHER');",
                name="insert_non_protected"
            )

            batch.add(
                "UPDATE AUDIT_TABLE SET status = 'DONE' WHERE id = 1;",
                name="update_non_protected"
            )

            batch.add(
                "DELETE FROM TEMP_DATA WHERE created < '2024-01-01';",
                name="delete_non_protected"
            )

            # Even operations that would violate if table was protected
            batch.add(
                "INSERT INTO OTHER_CONFIG (job, SOURCE) VALUES ('job1', 'WRONG_TEAM');",
                name="insert_wrong_team_non_protected"
            )

            # Operations on protected tables with correct filtering
            batch.add(
                "INSERT INTO FRAMEWORK_CONFIG (job, SOURCE) VALUES ('risk_job', 'RISK');",
                name="insert_protected_correct"
            )

        with batch.should_fail():
            # Operations on protected tables without correct filtering
            batch.add(
                "INSERT INTO FRAMEWORK_CONFIG (job) VALUES ('test');",
                name="insert_protected_missing_team",
                match_message="FRAMEWORK_CONFIG.*SOURCE.*RISK"
            )

            batch.add(
                "UPDATE JOB_DEFINITIONS SET status = 'ACTIVE' WHERE id = 1;",
                name="update_protected_missing_filter",
                match_message="JOB_DEFINITIONS.*SOURCE.*RISK"
            )

        with batch:
            batch.execute_with_subtests(subtests)

    # =========================================================================
    # EDGE CASES AND BOUNDARY CONDITIONS
    # =========================================================================

    def test_edge_cases_and_boundaries(self, subtests):
        """
        Test edge cases: case sensitivity, whitespace, comments, complex SQL.
        """
        os.environ['TEAM_ID'] = 'RISK'

        batch = BatchPolicyTest(
            "Python/Scripts/Any/row_level_security_basic.py",
            message=MESSAGE_TEMPLATE,
            check_args={
                "ENV_VAR_NAME": "TEAM_ID",
                "PROTECTED_TABLES": "FRAMEWORK_CONFIG,JOB_DEFINITIONS",
                "TEAM_COLUMN": "SOURCE"
            }
        )

        with batch.should_pass():
            # Case variations
            batch.add(
                "insert into framework_config (job_name, source) values ('job1', 'RISK');",
                name="lowercase_sql_keywords"
            )

            batch.add(
                "INSERT INTO framework_config (JOB_NAME, SoUrCe) VALUES ('job2', 'RISK');",
                name="mixed_case_table_column"
            )

            # Extra whitespace
            batch.add(
                """INSERT    INTO    FRAMEWORK_CONFIG
                   (  job_name  ,   SOURCE  )
                   VALUES   (  'job3'  ,   'RISK'  )  ;""",
                name="extra_whitespace"
            )

            # SQL with comments
            batch.add(
                """-- Insert new job configuration
                INSERT INTO FRAMEWORK_CONFIG /* inline comment */
                (job_name, SOURCE, enabled)
                VALUES ('job4', 'RISK', 1); -- end comment""",
                name="sql_with_comments"
            )

            # Table name with schema prefix
            batch.add(
                "INSERT INTO myschema.FRAMEWORK_CONFIG (job_name, SOURCE) VALUES ('job5', 'RISK');",
                name="schema_prefix"
            )

        with batch.should_fail():
            # Edge cases that should still fail
            batch.add(
                "INSERT INTO FRAMEWORK_CONFIG (job_name, \"SOURCE\") VALUES ('job6', 'WRONG');",
                name="quoted_column_wrong_value",
                match_message="FRAMEWORK_CONFIG.*SOURCE.*RISK"
            )

            # Table name in backticks
            batch.add(
                "INSERT INTO `FRAMEWORK_CONFIG` (job_name) VALUES ('job7');",
                name="backtick_table_missing_team",
                match_message="FRAMEWORK_CONFIG.*SOURCE.*RISK"
            )

        with batch:
            batch.execute_with_subtests(subtests)

    def test_multiple_statements_in_changeset(self, subtests):
        """
        Test multiple SQL statements in a single changeset.
        Each statement should be validated independently.
        """
        os.environ['TEAM_ID'] = 'RISK'

        batch = BatchPolicyTest(
            "Python/Scripts/Any/row_level_security_basic.py",
            message=MESSAGE_TEMPLATE,
            check_args={
                "ENV_VAR_NAME": "TEAM_ID",
                "PROTECTED_TABLES": "FRAMEWORK_CONFIG,JOB_DEFINITIONS",
                "TEAM_COLUMN": "SOURCE"
            }
        )

        with batch.should_pass():
            # Multiple valid statements
            batch.add(
                """
                INSERT INTO FRAMEWORK_CONFIG (job_name, SOURCE) VALUES ('job1', 'RISK');
                UPDATE FRAMEWORK_CONFIG SET enabled = 1 WHERE SOURCE = 'RISK' AND job_name = 'job1';
                DELETE FROM JOB_DEFINITIONS WHERE SOURCE = 'RISK' AND status = 'OBSOLETE';
                """,
                name="multiple_valid_statements"
            )

        with batch.should_fail():
            # One invalid statement among valid ones
            batch.add(
                """
                INSERT INTO FRAMEWORK_CONFIG (job_name, SOURCE) VALUES ('job1', 'RISK');
                UPDATE FRAMEWORK_CONFIG SET enabled = 1 WHERE job_name = 'job2';  -- Missing team filter
                DELETE FROM JOB_DEFINITIONS WHERE SOURCE = 'RISK' AND status = 'OLD';
                """,
                name="one_invalid_in_multiple",
                match_message="UPDATE.*FRAMEWORK_CONFIG.*SOURCE.*RISK"
            )

        with batch:
            batch.execute_with_subtests(subtests)

    # =========================================================================
    # SPECIAL SQL CONSTRUCTS
    # =========================================================================

    def test_special_sql_constructs(self, subtests):
        """
        Test handling of special SQL constructs like subqueries, CTEs, etc.
        """
        os.environ['TEAM_ID'] = 'RISK'

        batch = BatchPolicyTest(
            "Python/Scripts/Any/row_level_security_basic.py",
            message=MESSAGE_TEMPLATE,
            check_args={
                "ENV_VAR_NAME": "TEAM_ID",
                "PROTECTED_TABLES": "FRAMEWORK_CONFIG",
                "TEAM_COLUMN": "SOURCE"
            }
        )

        with batch.should_pass():
            # INSERT with SELECT subquery (if team column included)
            batch.add(
                """INSERT INTO FRAMEWORK_CONFIG (job_name, SOURCE, config)
                   SELECT name, 'RISK', default_config
                   FROM job_templates
                   WHERE category = 'risk';""",
                name="insert_select_with_team"
            )

            # INSERT with VALUES containing functions
            batch.add(
                """INSERT INTO FRAMEWORK_CONFIG (job_name, SOURCE, created_date)
                   VALUES (CONCAT('risk_', 'job'), 'RISK', CURRENT_DATE());""",
                name="insert_with_functions"
            )

        with batch.should_fail():
            # INSERT SELECT without team column
            batch.add(
                """INSERT INTO FRAMEWORK_CONFIG (job_name, config)
                   SELECT name, default_config
                   FROM job_templates
                   WHERE category = 'risk';""",
                name="insert_select_missing_team",
                match_message="INSERT.*FRAMEWORK_CONFIG.*SOURCE.*RISK"
            )

        with batch:
            batch.execute_with_subtests(subtests)

    # =========================================================================
    # PURE PYTHON MODE SPECIFIC TESTS
    # =========================================================================

    @pytest.mark.pure_python
    def test_pure_python_mode_compatibility(self):
        """
        Test that the check works correctly in pure Python mode.
        This validates mocking and execution without Liquibase.
        """
        os.environ['TEAM_ID'] = 'RISK'

        check = LiquibaseCheck(
            "Python/Scripts/Any/row_level_security_basic.py",
            message=MESSAGE_TEMPLATE,
            check_args={
                "ENV_VAR_NAME": "TEAM_ID",
                "PROTECTED_TABLES": "FRAMEWORK_CONFIG",
                "TEAM_COLUMN": "SOURCE"
            }
        )

        with check:
            # Test a passing case
            result = check.run(sql="INSERT INTO FRAMEWORK_CONFIG (job, SOURCE) VALUES ('test', 'RISK');")
            assert result is not None
            assert not result.fired, "Valid INSERT should not fire in pure Python mode"

            # Test a failing case
            result = check.run(sql="INSERT INTO FRAMEWORK_CONFIG (job) VALUES ('test');")
            assert result is not None
            assert result.fired, "Invalid INSERT should fire in pure Python mode"

    # =========================================================================
    # INTEGRATION TESTS
    # =========================================================================

    @pytest.mark.integration
    def test_integration_with_liquibase(self):
        """
        Integration test with actual Liquibase execution.
        Requires LIQUIBASE_LICENSE_KEY and Liquibase installation.
        """
        os.environ['TEAM_ID'] = 'RISK'

        check = LiquibaseCheck(
            "Python/Scripts/Any/row_level_security_basic.py",
            message=MESSAGE_TEMPLATE,
            check_args={
                "ENV_VAR_NAME": "TEAM_ID",
                "PROTECTED_TABLES": "FRAMEWORK_CONFIG,JOB_DEFINITIONS",
                "TEAM_COLUMN": "SOURCE"
            }
        )

        with check:
            # Test comprehensive SQL that should pass
            sql = """
            -- Create table first
            CREATE TABLE FRAMEWORK_CONFIG (
                job_name VARCHAR(100),
                SOURCE VARCHAR(50),
                enabled INTEGER
            );

            -- Valid INSERT with team column
            INSERT INTO FRAMEWORK_CONFIG (job_name, SOURCE, enabled)
            VALUES ('risk_calculator', 'RISK', 1);

            -- Valid UPDATE with team filter
            UPDATE FRAMEWORK_CONFIG
            SET enabled = 0
            WHERE job_name = 'risk_calculator' AND SOURCE = 'RISK';
            """

            result = check.run(sql=sql)
            assert result is not None
            assert not result.fired, f"Valid operations should pass. Got: {result.message if result.fired else 'passed'}"

    @pytest.mark.integration
    def test_integration_violation_detection(self):
        """
        Integration test for violation detection with Liquibase.
        """
        os.environ['TEAM_ID'] = 'RISK'

        check = LiquibaseCheck(
            "Python/Scripts/Any/row_level_security_basic.py",
            message=MESSAGE_TEMPLATE,
            check_args={
                "ENV_VAR_NAME": "TEAM_ID",
                "PROTECTED_TABLES": "FRAMEWORK_CONFIG",
                "TEAM_COLUMN": "SOURCE"
            }
        )

        with check:
            # SQL that should trigger violation
            sql = """
            CREATE TABLE FRAMEWORK_CONFIG (
                job_name VARCHAR(100),
                SOURCE VARCHAR(50),
                enabled INTEGER
            );

            -- Invalid INSERT - missing team column
            INSERT INTO FRAMEWORK_CONFIG (job_name, enabled)
            VALUES ('some_job', 1);
            """

            result = check.run(sql=sql)
            assert result is not None
            assert result.fired, "Missing team column should trigger violation"
            assert "FRAMEWORK_CONFIG" in result.message
            assert "SOURCE" in result.message
            assert "RISK" in result.message