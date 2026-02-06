"""
Comprehensive test suite for delete_without_where.py custom policy check.

This check enforces that DELETE statements must include a WHERE clause to prevent
accidental deletion of all data in a table.
Policy Intent: Prevent dangerous DELETE operations that could remove all table data.
"""

import pytest
from liquibase_test_harness import BatchPolicyTest


class TestDeleteWithoutWhere:
    """Test suite for delete_without_where.py policy check."""

    def test_core_functionality(self, subtests):
        """
        Core functionality: DELETE statements with/without WHERE clauses.
        Tests standard compliance (DELETE + WHERE) and violations (DELETE without WHERE).
        """
        batch = BatchPolicyTest("Python/Scripts/Any/delete_without_where.py")

        # ========================================
        # VALID: DELETE with WHERE clause (should NOT fire)
        # ========================================
        with batch.should_pass():
            batch.add(
                "DELETE FROM users WHERE id = 1;",
                name="simple_where"
            )
            batch.add(
                "DELETE FROM orders WHERE status = 'cancelled' AND created_date < '2023-01-01';",
                name="complex_where"
            )
            batch.add(
                "DELETE FROM products WHERE id IN (SELECT product_id FROM discontinued_products);",
                name="subquery_where"
            )
            batch.add(
                """DELETE u FROM users u
                   JOIN user_sessions s ON u.id = s.user_id
                   WHERE s.last_activity < '2023-01-01';""",
                name="join_with_where"
            )
            batch.add(
                """
                INSERT INTO users (id, name) VALUES (1, 'test');
                UPDATE users SET name = 'updated' WHERE id = 1;
                SELECT * FROM users;
                CREATE TABLE test_table (id INT);
                DROP TABLE temp_table;
                """,
                name="non_delete_statements"
            )
            batch.add(
                "delete from users where id = 1;",
                name="lowercase_where"
            )
            batch.add(
                "DELETE FROM t WHERE 1;",
                name="minimal_with_where"
            )
            batch.add(
                "DELETE FROM users WHERE FALSE;",
                name="where_false"
            )
            batch.add(
                "DELETE FROM users WHERE TRUE;",
                name="where_true"
            )
            batch.add(
                "DELETE FROM users WHERE id = ?;",
                name="parameterized_where"
            )
            batch.add(
                "DELETE FROM users WHERE status = :status AND created_date < :cutoff_date;",
                name="named_parameters"
            )
            batch.add(
                """
                BEGIN TRANSACTION;
                DELETE FROM users WHERE status = 'inactive';
                COMMIT;
                """,
                name="transaction_with_where"
            )

        # ========================================
        # INVALID: DELETE without WHERE (SHOULD fire)
        # ========================================
        with batch.should_fail():
            batch.add(
                "DELETE FROM users;",
                name="no_where"
            )
            batch.add(
                "DELETE FROM ORDERS;",
                name="uppercase_no_where"
            )
            batch.add(
                "Delete From products;",
                name="mixed_case_no_where"
            )
            batch.add(
                "DELETE FROM myschema.users;",
                name="schema_prefix_no_where"
            )
            batch.add(
                'DELETE FROM "users";',
                name="quoted_table_no_where"
            )
            batch.add(
                "DELETE FROM t;",
                name="minimal_no_where"
            )

        with batch:
            batch.execute_with_subtests(subtests)

    def test_edge_cases_and_advanced(self, subtests):
        """
        Edge cases, boundaries, database-specific syntax, and advanced features.
        Tests whitespace handling, comments, malformed SQL, DB-specific syntax, and transactions.
        """
        batch = BatchPolicyTest("Python/Scripts/Any/delete_without_where.py")

        # ========================================
        # VALID: Malformed SQL that shouldn't match pattern (should NOT fire)
        # ========================================
        with batch.should_pass():
            batch.add(
                "DELETE users WHERE id = 1;",
                name="delete_without_from"
            )

        # ========================================
        # INVALID: Edge cases without WHERE (SHOULD fire)
        # ========================================
        with batch.should_fail():
            batch.add(
                "DELETE    FROM    users   ;",
                name="extra_whitespace"
            )
            batch.add(
                """DELETE
                   FROM
                   users;""",
                name="with_newlines"
            )
            batch.add(
                """DELETE /* remove old data */ FROM users -- cleanup table
                   ;""",
                name="with_comments"
            )
            batch.add(
                """
                INSERT INTO users (id, name) VALUES (1, 'test');
                DELETE FROM temp_users WHERE created_date < '2023-01-01';
                UPDATE users SET status = 'active' WHERE id = 1;
                DELETE FROM users;
                INSERT INTO logs (message) VALUES ('cleanup complete');
                """,
                name="multiple_statements_one_bad"
            )
            batch.add(
                "DELETE FROM users; /* WHERE id = 1 */",
                name="where_only_in_comment"
            )
            batch.add(
                "DELETE FROM users LIMIT 10;",
                name="mysql_limit_no_where"
            )
            batch.add(
                "DELETE FROM users ORDER BY created_date LIMIT 5;",
                name="mysql_order_by_no_where"
            )
            batch.add(
                "DELETE FROM users USING users, orders;",
                name="using_clause_no_where"
            )
            batch.add(
                """
                BEGIN TRANSACTION;
                DELETE FROM users;
                COMMIT;
                """,
                name="transaction_no_where"
            )

        with batch:
            batch.execute_with_subtests(subtests)

    # ========================================
    # MALFORMED SQL - Test resilience (kept separate for clarity)
    # ========================================

    def test_incomplete_delete_statement_handling(self):
        """Malformed: Incomplete DELETE statement should not crash."""
        from liquibase_test_harness import LiquibaseCheck
        with LiquibaseCheck("Python/Scripts/Any/delete_without_where.py") as check:
            sql = "DELETE"
            result = check.run(sql=sql)
            # Should not crash, behavior depends on implementation

    def test_delete_from_without_table_handling(self):
        """Malformed: DELETE FROM without table name should not crash."""
        from liquibase_test_harness import LiquibaseCheck
        with LiquibaseCheck("Python/Scripts/Any/delete_without_where.py") as check:
            sql = "DELETE FROM WHERE id = 1;"
            result = check.run(sql=sql)
            # Should not crash, behavior depends on implementation

    # ========================================
    # PERFORMANCE TESTS - Test scalability (kept separate)
    # ========================================

    def test_large_sql_with_multiple_deletes_performance(self):
        """Performance: Large SQL with many DELETE statements should execute efficiently."""
        from liquibase_test_harness import LiquibaseCheck
        with LiquibaseCheck("Python/Scripts/Any/delete_without_where.py") as check:
            # Generate large SQL with many valid DELETE statements and one invalid
            sql_parts = ["DELETE FROM table_{} WHERE id = {};".format(i, i) for i in range(50)]
            sql_parts.append("DELETE FROM problem_table;")  # This should trigger
            sql = "\n".join(sql_parts)

            result = check.run(sql=sql)
            assert result.fired, "Should find the DELETE without WHERE in large SQL"

    def test_very_long_delete_statement_performance(self):
        """Performance: Very long DELETE statement should execute efficiently."""
        from liquibase_test_harness import LiquibaseCheck
        with LiquibaseCheck("Python/Scripts/Any/delete_without_where.py") as check:
            # Create a very long WHERE clause
            conditions = ["column_{} = {}".format(i, i) for i in range(100)]
            where_clause = " AND ".join(conditions)
            sql = "DELETE FROM users WHERE {};".format(where_clause)

            result = check.run(sql=sql)
            assert not result.fired, "Long DELETE with WHERE should not trigger the check"
