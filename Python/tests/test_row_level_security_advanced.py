"""
Comprehensive test suite for row_level_security_advanced.py custom policy check.

This is the advanced version that uses sqlparse for semantic SQL analysis rather than
pattern matching. It provides more accurate validation of DML operations in complex
SQL scenarios.

Policy Intent: Enforce row-level security on shared configuration tables using
SQL parsing (sqlparse) for semantic analysis. More accurate than the basic version.

Key Advantages Over Basic Check:
- Better handling of complex WHERE clauses with nested conditions
- Resilient to formatting and whitespace variations
- Accurate detection with parenthesized conditions
- Proper handling of subqueries and CTEs
- Semantic understanding of SQL structure

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


class TestRowLevelSecurityAdvanced:
    """Test suite for row_level_security_advanced.py policy check."""

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
    # INSERT STATEMENT VALIDATION (Basic functionality - same as basic check)
    # =========================================================================

    def test_insert_statement_validation(self, subtests):
        """
        Core functionality: INSERT statement validation.
        Tests that INSERT statements include the team column with correct value.
        Advanced check should handle these as well as the basic check.
        """
        batch = BatchPolicyTest(
            "Python/Scripts/Any/row_level_security_advanced.py",
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
    # UPDATE STATEMENT VALIDATION (Basic functionality)
    # =========================================================================

    def test_update_statement_validation(self, subtests):
        """
        Core functionality: UPDATE statement validation.
        Tests that UPDATE statements include team filtering in WHERE clause.
        """
        batch = BatchPolicyTest(
            "Python/Scripts/Any/row_level_security_advanced.py",
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
    # DELETE STATEMENT VALIDATION (Basic functionality)
    # =========================================================================

    def test_delete_statement_validation(self, subtests):
        """
        Core functionality: DELETE statement validation.
        Tests that DELETE statements include team filtering in WHERE clause.
        """
        batch = BatchPolicyTest(
            "Python/Scripts/Any/row_level_security_advanced.py",
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

            # DELETE with OR condition (potentially dangerous - advanced check should handle better)
            batch.add(
                "DELETE FROM FRAMEWORK_CONFIG WHERE job_name = 'job1' OR SOURCE = 'RISK';",
                name="delete_with_or_condition",
                match_message="DELETE.*FRAMEWORK_CONFIG.*SOURCE.*RISK"
            )

        with batch:
            batch.execute_with_subtests(subtests)

    # =========================================================================
    # ADVANCED SQL PARSING: COMPLEX WHERE CLAUSES
    # =========================================================================

    def test_complex_where_clauses(self, subtests):
        """
        Advanced SQL parsing: Complex WHERE clauses with nested conditions.
        The advanced check should handle these better than the basic check.
        """
        batch = BatchPolicyTest(
            "Python/Scripts/Any/row_level_security_advanced.py",
            message=MESSAGE_TEMPLATE,
            check_args={
                "ENV_VAR_NAME": "TEAM_ID",
                "PROTECTED_TABLES": "FRAMEWORK_CONFIG,JOB_DEFINITIONS",
                "TEAM_COLUMN": "SOURCE"
            }
        )

        with batch.should_pass():
            # Complex nested AND conditions
            batch.add(
                """UPDATE FRAMEWORK_CONFIG
                   SET enabled = 1
                   WHERE (SOURCE = 'RISK' AND job_name LIKE 'risk_%')
                     AND (status = 'ACTIVE' OR priority > 5)
                     AND created_date > '2024-01-01';""",
                name="complex_nested_and_conditions"
            )

            # Deeply nested parentheses with team filter
            batch.add(
                """DELETE FROM JOB_DEFINITIONS
                   WHERE ((SOURCE = 'RISK' AND status = 'INACTIVE')
                          OR (SOURCE = 'RISK' AND obsolete = 1))
                     AND (last_run < '2023-01-01' OR run_count = 0);""",
                name="deeply_nested_parentheses"
            )

            # Multiple conditions with IN, BETWEEN, LIKE
            batch.add(
                """UPDATE FRAMEWORK_CONFIG
                   SET priority = priority + 1
                   WHERE SOURCE = 'RISK'
                     AND job_id BETWEEN 100 AND 200
                     AND status IN ('ACTIVE', 'PENDING')
                     AND description LIKE '%critical%';""",
                name="multiple_operators_with_team"
            )

            # EXISTS subquery with team filter in main query
            batch.add(
                """UPDATE JOB_DEFINITIONS
                   SET active = 0
                   WHERE SOURCE = 'RISK'
                     AND EXISTS (SELECT 1 FROM job_history
                                 WHERE job_history.job_id = JOB_DEFINITIONS.job_id
                                   AND job_history.failed = 1);""",
                name="exists_subquery_with_team"
            )

        with batch.should_fail():
            # Complex WHERE without team filter
            batch.add(
                """UPDATE FRAMEWORK_CONFIG
                   SET enabled = 1
                   WHERE (job_name LIKE 'risk_%' AND status = 'ACTIVE')
                     OR (priority > 10 AND urgent = 1);""",
                name="complex_missing_team_filter",
                match_message="UPDATE.*FRAMEWORK_CONFIG.*SOURCE.*RISK"
            )

            # Nested conditions but team filter with wrong value
            batch.add(
                """DELETE FROM JOB_DEFINITIONS
                   WHERE ((SOURCE = 'TRADING' AND status = 'INACTIVE')
                          OR (obsolete = 1 AND last_run < '2023-01-01'))
                     AND priority < 3;""",
                name="nested_wrong_team_value",
                match_message="DELETE.*JOB_DEFINITIONS.*SOURCE.*RISK"
            )

        with batch:
            batch.execute_with_subtests(subtests)

    # =========================================================================
    # ADVANCED SQL PARSING: SUBQUERIES AND CTEs
    # =========================================================================

    def test_subqueries_and_ctes(self, subtests):
        """
        Advanced SQL parsing: Subqueries and Common Table Expressions.
        Tests semantic understanding of complex SQL structures.
        """
        batch = BatchPolicyTest(
            "Python/Scripts/Any/row_level_security_advanced.py",
            message=MESSAGE_TEMPLATE,
            check_args={
                "ENV_VAR_NAME": "TEAM_ID",
                "PROTECTED_TABLES": "FRAMEWORK_CONFIG,JOB_DEFINITIONS",
                "TEAM_COLUMN": "SOURCE"
            }
        )

        with batch.should_pass():
            # INSERT with SELECT subquery including team value
            batch.add(
                """INSERT INTO FRAMEWORK_CONFIG (job_id, job_name, SOURCE, config)
                   SELECT j.id, j.name, 'RISK', j.default_config
                   FROM job_templates j
                   WHERE j.category = 'risk_management'
                     AND j.active = 1;""",
                name="insert_select_with_team_literal"
            )

            # UPDATE with correlated subquery, team filter in main query
            batch.add(
                """UPDATE JOB_DEFINITIONS jd
                   SET priority = (SELECT AVG(priority) + 1
                                   FROM job_history jh
                                   WHERE jh.job_id = jd.job_id)
                   WHERE jd.SOURCE = 'RISK'
                     AND jd.status = 'ACTIVE';""",
                name="update_correlated_subquery"
            )

            # DELETE with IN subquery, team filter in main query
            batch.add(
                """DELETE FROM FRAMEWORK_CONFIG
                   WHERE SOURCE = 'RISK'
                     AND job_id IN (SELECT job_id
                                    FROM job_audit
                                    WHERE violation_count > 5);""",
                name="delete_with_in_subquery"
            )

            # CTE with team filtering in main query
            batch.add(
                """WITH high_priority_jobs AS (
                       SELECT job_id, job_name, priority
                       FROM job_registry
                       WHERE priority > 8
                   )
                   UPDATE JOB_DEFINITIONS jd
                   SET urgent = 1
                   WHERE jd.SOURCE = 'RISK'
                     AND jd.job_id IN (SELECT job_id FROM high_priority_jobs);""",
                name="cte_with_team_filter"
            )

        with batch.should_fail():
            # INSERT SELECT missing team column
            batch.add(
                """INSERT INTO FRAMEWORK_CONFIG (job_id, job_name, config)
                   SELECT id, name, default_config
                   FROM job_templates
                   WHERE category = 'risk';""",
                name="insert_select_missing_team",
                match_message="INSERT.*FRAMEWORK_CONFIG.*SOURCE.*RISK"
            )

            # CTE but missing team filter in main UPDATE
            batch.add(
                """WITH active_jobs AS (
                       SELECT job_id FROM job_registry WHERE active = 1
                   )
                   UPDATE JOB_DEFINITIONS
                   SET last_checked = CURRENT_TIMESTAMP
                   WHERE job_id IN (SELECT job_id FROM active_jobs);""",
                name="cte_missing_team_filter",
                match_message="UPDATE.*JOB_DEFINITIONS.*SOURCE.*RISK"
            )

        with batch:
            batch.execute_with_subtests(subtests)

    # =========================================================================
    # ADVANCED SQL PARSING: JOINs
    # =========================================================================

    def test_join_operations(self, subtests):
        """
        Advanced SQL parsing: JOIN operations with team filtering.
        Tests that the check properly validates team filtering in JOIN scenarios.
        """
        batch = BatchPolicyTest(
            "Python/Scripts/Any/row_level_security_advanced.py",
            message=MESSAGE_TEMPLATE,
            check_args={
                "ENV_VAR_NAME": "TEAM_ID",
                "PROTECTED_TABLES": "FRAMEWORK_CONFIG,JOB_DEFINITIONS",
                "TEAM_COLUMN": "SOURCE"
            }
        )

        with batch.should_pass():
            # UPDATE with JOIN and team filter
            batch.add(
                """UPDATE FRAMEWORK_CONFIG fc
                   INNER JOIN job_metadata jm ON fc.job_id = jm.job_id
                   SET fc.description = jm.description
                   WHERE fc.SOURCE = 'RISK'
                     AND jm.version = 'latest';""",
                name="update_with_join_team_filter"
            )

            # DELETE with JOIN and team filter
            batch.add(
                """DELETE fc FROM FRAMEWORK_CONFIG fc
                   INNER JOIN obsolete_jobs oj ON fc.job_id = oj.job_id
                   WHERE fc.SOURCE = 'RISK'
                     AND oj.marked_date < '2023-01-01';""",
                name="delete_with_join_team_filter"
            )

            # Complex multi-table JOIN with team filter
            batch.add(
                """UPDATE JOB_DEFINITIONS jd
                   LEFT JOIN job_statistics js ON jd.job_id = js.job_id
                   LEFT JOIN job_owners jo ON jd.job_id = jo.job_id
                   SET jd.performance_score = COALESCE(js.avg_runtime, 0)
                   WHERE jd.SOURCE = 'RISK'
                     AND (jo.owner_team = 'risk-analytics' OR jo.owner_team IS NULL);""",
                name="multi_join_with_team_filter"
            )

        with batch.should_fail():
            # UPDATE with JOIN but missing team filter
            batch.add(
                """UPDATE FRAMEWORK_CONFIG fc
                   INNER JOIN job_metadata jm ON fc.job_id = jm.job_id
                   SET fc.description = jm.description
                   WHERE jm.version = 'latest';""",
                name="update_join_missing_team",
                match_message="UPDATE.*FRAMEWORK_CONFIG.*SOURCE.*RISK"
            )

            # DELETE with JOIN and wrong team value
            batch.add(
                """DELETE fc FROM FRAMEWORK_CONFIG fc
                   INNER JOIN obsolete_jobs oj ON fc.job_id = oj.job_id
                   WHERE fc.SOURCE = 'TRADING'
                     AND oj.marked_date < '2023-01-01';""",
                name="delete_join_wrong_team",
                match_message="DELETE.*FRAMEWORK_CONFIG.*SOURCE.*RISK"
            )

        with batch:
            batch.execute_with_subtests(subtests)

    # =========================================================================
    # EDGE CASES: SQL WITH EXTENSIVE COMMENTS AND FORMATTING
    # =========================================================================

    def test_sql_with_comments_and_formatting(self, subtests):
        """
        Edge case: SQL with extensive comments and formatting variations.
        Advanced parser should handle these better than basic pattern matching.
        """
        batch = BatchPolicyTest(
            "Python/Scripts/Any/row_level_security_advanced.py",
            message=MESSAGE_TEMPLATE,
            check_args={
                "ENV_VAR_NAME": "TEAM_ID",
                "PROTECTED_TABLES": "FRAMEWORK_CONFIG",
                "TEAM_COLUMN": "SOURCE"
            }
        )

        with batch.should_pass():
            # SQL with multi-line comments
            batch.add(
                """/* This is a complex update statement
                      that spans multiple lines
                      for documentation purposes */
                   UPDATE FRAMEWORK_CONFIG
                   SET /* inline comment */ enabled = 1
                   WHERE SOURCE = 'RISK' -- team filter
                     AND job_name = 'risk_calculator'; -- specific job""",
                name="multi_line_comments"
            )

            # Heavily formatted SQL with unusual spacing
            batch.add(
                """INSERT
                        INTO
                            FRAMEWORK_CONFIG
                                (
                                    job_name    ,
                                    SOURCE      ,
                                    enabled
                                )
                        VALUES
                                (
                                    'risk_job'  ,
                                    'RISK'      ,
                                    1
                                );""",
                name="unusual_formatting"
            )

            # SQL with nested comments
            batch.add(
                """DELETE FROM FRAMEWORK_CONFIG
                   WHERE SOURCE = /* team column */ 'RISK'
                     AND job_id IN (
                         SELECT job_id
                         FROM job_audit
                         WHERE /* nested comment
                                  multi-line */ status = 'FAILED'
                     );""",
                name="nested_comments"
            )

        with batch.should_fail():
            # Comments but missing team filter
            batch.add(
                """/* Important update */
                   UPDATE FRAMEWORK_CONFIG
                   SET enabled = 1 -- enable the job
                   WHERE job_name = 'some_job'; -- missing team filter!""",
                name="comments_missing_team",
                match_message="UPDATE.*FRAMEWORK_CONFIG.*SOURCE.*RISK"
            )

        with batch:
            batch.execute_with_subtests(subtests)

    # =========================================================================
    # EDGE CASES: STRING LITERALS CONTAINING SQL KEYWORDS
    # =========================================================================

    def test_string_literals_with_sql_keywords(self, subtests):
        """
        Edge case: String literals containing SQL keywords.
        Tests that parser doesn't get confused by SQL keywords in strings.
        """
        batch = BatchPolicyTest(
            "Python/Scripts/Any/row_level_security_advanced.py",
            message=MESSAGE_TEMPLATE,
            check_args={
                "ENV_VAR_NAME": "TEAM_ID",
                "PROTECTED_TABLES": "FRAMEWORK_CONFIG",
                "TEAM_COLUMN": "SOURCE"
            }
        )

        with batch.should_pass():
            # String literals containing WHERE, AND, OR
            batch.add(
                """INSERT INTO FRAMEWORK_CONFIG (job_name, SOURCE, description)
                   VALUES ('risk_job', 'RISK', 'This job WHERE data AND logic OR rules apply');""",
                name="keywords_in_string_values"
            )

            # Update with SQL keywords in string
            batch.add(
                """UPDATE FRAMEWORK_CONFIG
                   SET description = 'UPDATE this description WHERE needed AND required'
                   WHERE SOURCE = 'RISK'
                     AND job_id = 101;""",
                name="update_keywords_in_strings"
            )

            # Complex string with quotes and keywords
            batch.add(
                """INSERT INTO FRAMEWORK_CONFIG (job_name, SOURCE, sql_template)
                   VALUES ('risk_analyzer', 'RISK',
                           'SELECT * FROM table WHERE col = ''value'' AND status = ''ACTIVE''');""",
                name="sql_template_in_string"
            )

        with batch.should_fail():
            # String with keywords but missing actual team filter
            batch.add(
                """INSERT INTO FRAMEWORK_CONFIG (job_name, description)
                   VALUES ('job1', 'This has SOURCE = RISK in description but not as column');""",
                name="keywords_in_string_no_team",
                match_message="INSERT.*FRAMEWORK_CONFIG.*SOURCE.*RISK"
            )

        with batch:
            batch.execute_with_subtests(subtests)

    # =========================================================================
    # EDGE CASES: VERY LONG SQL STATEMENTS
    # =========================================================================

    def test_very_long_sql_statements(self, subtests):
        """
        Edge case: Very long SQL statements.
        Tests parser performance and accuracy with large SQL.
        """
        batch = BatchPolicyTest(
            "Python/Scripts/Any/row_level_security_advanced.py",
            message=MESSAGE_TEMPLATE,
            check_args={
                "ENV_VAR_NAME": "TEAM_ID",
                "PROTECTED_TABLES": "FRAMEWORK_CONFIG",
                "TEAM_COLUMN": "SOURCE"
            }
        )

        with batch.should_pass():
            # Very long INSERT with many columns
            columns = [f"col_{i}" for i in range(50)]
            values = [f"'value_{i}'" for i in range(50)]
            columns[10] = "SOURCE"  # Insert team column
            values[10] = "'RISK'"   # With correct value

            long_insert = f"""INSERT INTO FRAMEWORK_CONFIG
                             ({', '.join(columns)})
                             VALUES ({', '.join(values)});"""
            batch.add(long_insert, name="very_long_insert_with_team")

            # Long UPDATE with many conditions
            conditions = ["SOURCE = 'RISK'"]
            for i in range(20):
                conditions.append(f"col_{i} != 'exclude_{i}'")

            long_update = f"""UPDATE FRAMEWORK_CONFIG
                             SET status = 'PROCESSED'
                             WHERE {' AND '.join(conditions)};"""
            batch.add(long_update, name="long_update_many_conditions")

        with batch.should_fail():
            # Very long INSERT missing team column
            columns = [f"col_{i}" for i in range(50)]
            values = [f"'value_{i}'" for i in range(50)]

            long_insert = f"""INSERT INTO FRAMEWORK_CONFIG
                             ({', '.join(columns)})
                             VALUES ({', '.join(values)});"""
            batch.add(
                long_insert,
                name="very_long_insert_no_team",
                match_message="INSERT.*FRAMEWORK_CONFIG.*SOURCE.*RISK"
            )

        with batch:
            batch.execute_with_subtests(subtests)

    # =========================================================================
    # EDGE CASES: MIXED OPERATORS (AND/OR) IN WHERE CLAUSES
    # =========================================================================

    def test_mixed_operators_in_where(self, subtests):
        """
        Edge case: Mixed AND/OR operators in WHERE clauses.
        Tests proper precedence and logical evaluation.
        """
        batch = BatchPolicyTest(
            "Python/Scripts/Any/row_level_security_advanced.py",
            message=MESSAGE_TEMPLATE,
            check_args={
                "ENV_VAR_NAME": "TEAM_ID",
                "PROTECTED_TABLES": "FRAMEWORK_CONFIG",
                "TEAM_COLUMN": "SOURCE"
            }
        )

        with batch.should_pass():
            # Proper AND/OR precedence with team filter
            batch.add(
                """UPDATE FRAMEWORK_CONFIG
                   SET priority = 10
                   WHERE SOURCE = 'RISK'
                     AND (status = 'ACTIVE' OR status = 'PENDING')
                     AND (priority < 5 OR urgent = 1);""",
                name="mixed_operators_proper_precedence"
            )

            # Complex OR groups all containing team filter
            batch.add(
                """DELETE FROM FRAMEWORK_CONFIG
                   WHERE (SOURCE = 'RISK' AND status = 'OBSOLETE')
                      OR (SOURCE = 'RISK' AND last_run < '2023-01-01')
                      OR (SOURCE = 'RISK' AND enabled = 0);""",
                name="or_groups_all_with_team"
            )

        with batch.should_fail():
            # OR condition that could bypass team filter
            batch.add(
                """UPDATE FRAMEWORK_CONFIG
                   SET enabled = 1
                   WHERE status = 'CRITICAL'
                      OR SOURCE = 'RISK';""",
                name="or_could_bypass_team",
                match_message="UPDATE.*FRAMEWORK_CONFIG.*SOURCE.*RISK"
            )

            # Mixed operators with team filter in wrong branch
            batch.add(
                """DELETE FROM FRAMEWORK_CONFIG
                   WHERE (status = 'OBSOLETE' AND priority < 1)
                      OR (job_name LIKE 'old_%' AND SOURCE = 'RISK');""",
                name="team_in_only_one_or_branch",
                match_message="DELETE.*FRAMEWORK_CONFIG.*SOURCE.*RISK"
            )

        with batch:
            batch.execute_with_subtests(subtests)

    # =========================================================================
    # EDGE CASES: FUNCTIONS IN WHERE CLAUSE
    # =========================================================================

    def test_functions_in_where_clause(self, subtests):
        """
        Edge case: Functions in WHERE clause comparisons.
        Tests that parser handles function calls correctly.
        """
        batch = BatchPolicyTest(
            "Python/Scripts/Any/row_level_security_advanced.py",
            message=MESSAGE_TEMPLATE,
            check_args={
                "ENV_VAR_NAME": "TEAM_ID",
                "PROTECTED_TABLES": "FRAMEWORK_CONFIG",
                "TEAM_COLUMN": "SOURCE"
            }
        )

        with batch.should_pass():
            # Functions with team filter
            batch.add(
                """UPDATE FRAMEWORK_CONFIG
                   SET last_modified = CURRENT_TIMESTAMP
                   WHERE UPPER(SOURCE) = 'RISK'
                     AND DATEDIFF(CURRENT_DATE, created_date) > 30;""",
                name="functions_with_team_filter"
            )

            # COALESCE and other functions
            batch.add(
                """DELETE FROM FRAMEWORK_CONFIG
                   WHERE COALESCE(SOURCE, 'DEFAULT') = 'RISK'
                     AND LENGTH(job_name) > 50;""",
                name="coalesce_with_team"
            )

            # CASE statement in WHERE
            batch.add(
                """UPDATE FRAMEWORK_CONFIG
                   SET active = 0
                   WHERE SOURCE = 'RISK'
                     AND CASE
                         WHEN priority > 10 THEN 1
                         WHEN urgent = 1 THEN 1
                         ELSE 0
                     END = 1;""",
                name="case_statement_in_where"
            )

        with batch.should_fail():
            # Functions but missing team filter
            batch.add(
                """UPDATE FRAMEWORK_CONFIG
                   SET last_checked = CURRENT_TIMESTAMP
                   WHERE DATEDIFF(CURRENT_DATE, last_run) > 7
                     AND UPPER(status) = 'ACTIVE';""",
                name="functions_no_team_filter",
                match_message="UPDATE.*FRAMEWORK_CONFIG.*SOURCE.*RISK"
            )

        with batch:
            batch.execute_with_subtests(subtests)

    # =========================================================================
    # ADVANCED: INSERT ... SELECT with CASE statements
    # =========================================================================

    def test_insert_select_with_case(self, subtests):
        """
        Advanced: INSERT ... SELECT with CASE statements.
        Tests complex INSERT SELECT patterns with conditional logic.
        """
        batch = BatchPolicyTest(
            "Python/Scripts/Any/row_level_security_advanced.py",
            message=MESSAGE_TEMPLATE,
            check_args={
                "ENV_VAR_NAME": "TEAM_ID",
                "PROTECTED_TABLES": "FRAMEWORK_CONFIG",
                "TEAM_COLUMN": "SOURCE"
            }
        )

        with batch.should_pass():
            # INSERT SELECT with CASE including team value
            batch.add(
                """INSERT INTO FRAMEWORK_CONFIG (job_id, job_name, SOURCE, priority)
                   SELECT
                       j.id,
                       j.name,
                       'RISK',
                       CASE
                           WHEN j.critical = 1 THEN 10
                           WHEN j.important = 1 THEN 5
                           ELSE 1
                       END
                   FROM job_templates j
                   WHERE j.team = 'risk';""",
                name="insert_select_case_with_team"
            )

            # Complex CASE with team literal
            batch.add(
                """INSERT INTO FRAMEWORK_CONFIG (job_name, SOURCE, status, config)
                   SELECT
                       CONCAT('risk_', j.base_name),
                       'RISK',
                       CASE j.template_type
                           WHEN 'batch' THEN 'SCHEDULED'
                           WHEN 'realtime' THEN 'ACTIVE'
                           ELSE 'PENDING'
                       END,
                       j.default_config
                   FROM job_catalog j
                   WHERE j.enabled = 1;""",
                name="complex_case_with_team_literal"
            )

        with batch.should_fail():
            # INSERT SELECT with CASE but missing team column
            batch.add(
                """INSERT INTO FRAMEWORK_CONFIG (job_id, job_name, priority)
                   SELECT
                       j.id,
                       j.name,
                       CASE
                           WHEN j.critical = 1 THEN 10
                           ELSE 1
                       END
                   FROM job_templates j;""",
                name="insert_select_case_no_team",
                match_message="INSERT.*FRAMEWORK_CONFIG.*SOURCE.*RISK"
            )

        with batch:
            batch.execute_with_subtests(subtests)

    # =========================================================================
    # ENVIRONMENT VARIABLE HANDLING
    # =========================================================================

    def test_environment_variable_handling(self, subtests):
        """
        Test environment variable handling and configuration.
        Same as basic check but ensures advanced check handles it properly.
        """
        # Test with different environment variable
        os.environ['DEPLOY_TEAM'] = 'TRADING'

        batch = BatchPolicyTest(
            "Python/Scripts/Any/row_level_security_advanced.py",
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
            "Python/Scripts/Any/row_level_security_advanced.py",
            message=MESSAGE_TEMPLATE,
            check_args={
                "ENV_VAR_NAME": "NONEXISTENT_VAR",
                "PROTECTED_TABLES": "FRAMEWORK_CONFIG",
                "TEAM_COLUMN": "SOURCE"
            }
        ) as check:
            # The check should handle missing env var gracefully
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
            "Python/Scripts/Any/row_level_security_advanced.py",
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
    # SPECIAL SQL CONSTRUCTS
    # =========================================================================

    def test_special_sql_constructs(self, subtests):
        """
        Test handling of special SQL constructs.
        Advanced parser should handle these better than basic check.
        """
        os.environ['TEAM_ID'] = 'RISK'

        batch = BatchPolicyTest(
            "Python/Scripts/Any/row_level_security_advanced.py",
            message=MESSAGE_TEMPLATE,
            check_args={
                "ENV_VAR_NAME": "TEAM_ID",
                "PROTECTED_TABLES": "FRAMEWORK_CONFIG",
                "TEAM_COLUMN": "SOURCE"
            }
        )

        with batch.should_pass():
            # MERGE statement with team filter (if supported)
            batch.add(
                """MERGE INTO FRAMEWORK_CONFIG fc
                   USING job_updates ju ON fc.job_id = ju.job_id
                   WHEN MATCHED AND fc.SOURCE = 'RISK' THEN
                       UPDATE SET fc.config = ju.new_config
                   WHEN NOT MATCHED THEN
                       INSERT (job_id, job_name, SOURCE, config)
                       VALUES (ju.job_id, ju.job_name, 'RISK', ju.new_config);""",
                name="merge_with_team_filter"
            )

            # REPLACE statement with team column (MySQL style)
            batch.add(
                """REPLACE INTO FRAMEWORK_CONFIG (job_id, job_name, SOURCE, config)
                   VALUES (100, 'risk_analyzer', 'RISK', '{"enabled": true}');""",
                name="replace_with_team"
            )

        with batch.should_fail():
            # MERGE without proper team handling
            batch.add(
                """MERGE INTO FRAMEWORK_CONFIG fc
                   USING job_updates ju ON fc.job_id = ju.job_id
                   WHEN MATCHED THEN
                       UPDATE SET fc.config = ju.new_config
                   WHEN NOT MATCHED THEN
                       INSERT (job_id, job_name, config)
                       VALUES (ju.job_id, ju.job_name, ju.new_config);""",
                name="merge_missing_team",
                match_message="FRAMEWORK_CONFIG.*SOURCE.*RISK"
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
            "Python/Scripts/Any/row_level_security_advanced.py",
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

            # Test complex SQL that advanced parser should handle
            result = check.run(sql="""
                UPDATE FRAMEWORK_CONFIG
                SET enabled = 1
                WHERE (SOURCE = 'RISK' AND status = 'ACTIVE')
                   OR (SOURCE = 'RISK' AND priority > 10);
            """)
            assert not result.fired, "Complex valid UPDATE should not fire"

    @pytest.mark.pure_python
    def test_pure_python_advanced_parsing(self):
        """
        Test advanced parsing features in pure Python mode.
        Validates that sqlparse-based parsing works without Liquibase.
        """
        os.environ['TEAM_ID'] = 'RISK'

        check = LiquibaseCheck(
            "Python/Scripts/Any/row_level_security_advanced.py",
            message=MESSAGE_TEMPLATE,
            check_args={
                "ENV_VAR_NAME": "TEAM_ID",
                "PROTECTED_TABLES": "FRAMEWORK_CONFIG",
                "TEAM_COLUMN": "SOURCE"
            }
        )

        with check:
            # Test CTE handling
            result = check.run(sql="""
                WITH temp AS (SELECT * FROM job_templates WHERE active = 1)
                UPDATE FRAMEWORK_CONFIG fc
                SET fc.template_id = (SELECT id FROM temp WHERE temp.name = fc.job_name)
                WHERE fc.SOURCE = 'RISK';
            """)
            assert not result.fired, "CTE with team filter should pass"

            # Test subquery handling
            result = check.run(sql="""
                DELETE FROM FRAMEWORK_CONFIG
                WHERE SOURCE = 'RISK'
                  AND job_id IN (SELECT job_id FROM obsolete_jobs);
            """)
            assert not result.fired, "Subquery with team filter should pass"

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
            "Python/Scripts/Any/row_level_security_advanced.py",
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
                enabled INTEGER,
                config TEXT
            );

            -- Complex valid INSERT with subquery
            INSERT INTO FRAMEWORK_CONFIG (job_name, SOURCE, config)
            SELECT CONCAT('risk_', name), 'RISK', default_config
            FROM job_templates
            WHERE category = 'risk';

            -- Valid UPDATE with complex WHERE
            UPDATE FRAMEWORK_CONFIG
            SET enabled = 1
            WHERE SOURCE = 'RISK'
              AND (job_name LIKE 'risk_%' OR job_name IN ('special_risk_job'));
            """

            result = check.run(sql=sql)
            assert result is not None
            assert not result.fired, f"Valid operations should pass. Got: {result.message if result.fired else 'passed'}"

    @pytest.mark.integration
    def test_integration_violation_detection(self):
        """
        Integration test for violation detection with Liquibase.
        Tests that advanced parsing correctly identifies violations.
        """
        os.environ['TEAM_ID'] = 'RISK'

        check = LiquibaseCheck(
            "Python/Scripts/Any/row_level_security_advanced.py",
            message=MESSAGE_TEMPLATE,
            check_args={
                "ENV_VAR_NAME": "TEAM_ID",
                "PROTECTED_TABLES": "FRAMEWORK_CONFIG",
                "TEAM_COLUMN": "SOURCE"
            }
        )

        with check:
            # SQL that should trigger violation (complex case)
            sql = """
            CREATE TABLE FRAMEWORK_CONFIG (
                job_name VARCHAR(100),
                SOURCE VARCHAR(50),
                enabled INTEGER
            );

            -- Complex invalid UPDATE - team filter in wrong OR branch
            UPDATE FRAMEWORK_CONFIG
            SET enabled = 1
            WHERE (status = 'CRITICAL' AND priority > 10)
               OR (job_name = 'special' AND SOURCE = 'RISK');
            """

            result = check.run(sql=sql)
            assert result is not None
            assert result.fired, "Complex invalid UPDATE should trigger violation"
            assert "FRAMEWORK_CONFIG" in result.message
            assert "SOURCE" in result.message

    @pytest.mark.integration
    def test_integration_advanced_features(self):
        """
        Integration test for advanced SQL features.
        Validates that sqlparse integration works with Liquibase.
        """
        os.environ['TEAM_ID'] = 'RISK'

        check = LiquibaseCheck(
            "Python/Scripts/Any/row_level_security_advanced.py",
            message=MESSAGE_TEMPLATE,
            check_args={
                "ENV_VAR_NAME": "TEAM_ID",
                "PROTECTED_TABLES": "FRAMEWORK_CONFIG",
                "TEAM_COLUMN": "SOURCE"
            }
        )

        with check:
            # Test with CTE and complex joins
            sql = """
            CREATE TABLE FRAMEWORK_CONFIG (
                job_id INTEGER,
                job_name VARCHAR(100),
                SOURCE VARCHAR(50),
                config TEXT
            );

            CREATE TABLE job_metadata (
                job_id INTEGER,
                description TEXT,
                version VARCHAR(20)
            );

            -- CTE with JOIN and team filter
            WITH latest_jobs AS (
                SELECT job_id, description
                FROM job_metadata
                WHERE version = 'latest'
            )
            UPDATE FRAMEWORK_CONFIG fc
            SET fc.config = (SELECT description FROM latest_jobs WHERE latest_jobs.job_id = fc.job_id)
            WHERE fc.SOURCE = 'RISK'
              AND fc.job_id IN (SELECT job_id FROM latest_jobs);
            """

            result = check.run(sql=sql)
            assert result is not None
            assert not result.fired, f"Advanced SQL with CTE should pass. Got: {result.message if result.fired else 'passed'}"