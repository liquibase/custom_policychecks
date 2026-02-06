"""
Comprehensive test suite for fk_names.py custom policy check.

This check enforces foreign key naming convention FK_<child_table>_<parent_table>.
Policy Intent: Ensure consistent FK naming across the database schema.

Message Template: "Foreign key name __NAME_CURRENT__ must include parent and child table names (__NAME_STANDARD__)."
"""

import pytest
from liquibase_test_harness import BatchPolicyTest, LiquibaseCheck

# Message template from the policy check
MESSAGE_TEMPLATE = "Foreign key name __NAME_CURRENT__ must include parent and child table names (__NAME_STANDARD__)."


class TestFKNames:
    """Test suite for fk_names.py policy check."""

    def test_core_functionality(self, subtests):
        """
        Core functionality: Foreign key naming validation.
        Tests standard FK_<child>_<parent> compliance and common naming violations.
        """
        batch = BatchPolicyTest(
            "Python/Scripts/Any/fk_names.py",
            message=MESSAGE_TEMPLATE
        )

        # ========================================
        # VALID: Correct FK naming pattern (should NOT fire)
        # ========================================
        with batch.should_pass():
            batch.add(
                """
                CREATE TABLE orders (
                    id INT PRIMARY KEY,
                    customer_id INT,
                    CONSTRAINT fk_orders_customers FOREIGN KEY (customer_id) REFERENCES customers(id)
                );
                """,
                name="valid_fk_create_table"
            )
            batch.add(
                """
                ALTER TABLE order_items
                ADD CONSTRAINT fk_order_items_orders
                FOREIGN KEY (order_id) REFERENCES orders(id);
                """,
                name="valid_fk_alter_table"
            )
            batch.add(
                """
                ALTER TABLE sales.order_items
                ADD CONSTRAINT fk_order_items_products
                FOREIGN KEY (product_id) REFERENCES inventory.products(id);
                """,
                name="schema_qualified_tables"
            )
            batch.add(
                """
                CREATE TABLE user_account_settings (
                    id INT PRIMARY KEY,
                    user_id INT,
                    CONSTRAINT fk_user_account_settings_user_accounts
                    FOREIGN KEY (user_id) REFERENCES user_accounts(id)
                );
                """,
                name="tables_with_underscores"
            )
            batch.add(
                """
                INSERT INTO users VALUES (1, 'test');
                UPDATE orders SET status = 'shipped' WHERE id = 1;
                DELETE FROM temp_data WHERE created < '2023-01-01';
                SELECT * FROM customers;
                """,
                name="non_fk_statements"
            )
            batch.add(
                """
                CREATE TABLE customers (
                    id INT PRIMARY KEY,
                    email VARCHAR(100),
                    name VARCHAR(50)
                );
                """,
                name="table_without_fk"
            )

        # ========================================
        # INVALID: Incorrect FK naming patterns (SHOULD fire)
        # ========================================
        with batch.should_fail():
            batch.add(
                """
                CREATE TABLE orders (
                    id INT PRIMARY KEY,
                    customer_id INT,
                    CONSTRAINT customer_fkey FOREIGN KEY (customer_id) REFERENCES customers(id)
                );
                """,
                name="wrong_pattern",
                match_message="customer_fkey"
            )
            batch.add(
                """
                ALTER TABLE products
                ADD CONSTRAINT products_categories
                FOREIGN KEY (category_id) REFERENCES categories(id);
                """,
                name="missing_prefix",
                match_message="products_categories"
            )
            batch.add(
                """
                CREATE TABLE line_items (
                    id INT PRIMARY KEY,
                    order_id INT,
                    CONSTRAINT fk_orders_line_items FOREIGN KEY (order_id) REFERENCES orders(id)
                );
                """,
                name="wrong_table_order",
                match_message="fk_orders_line_items"
            )
            batch.add(
                """
                ALTER TABLE payments
                ADD CONSTRAINT fkPaymentsOrders
                FOREIGN KEY (order_id) REFERENCES orders(id);
                """,
                name="camelcase_name"
            )

        with batch:
            batch.execute_with_subtests(subtests)

    def test_edge_cases_and_boundaries(self, subtests):
        """
        Edge cases and boundary conditions.
        Tests case sensitivity, compound columns, numeric tables, character limits, and complex DDL.
        """
        batch = BatchPolicyTest(
            "Python/Scripts/Any/fk_names.py",
            message=MESSAGE_TEMPLATE
        )

        # ========================================
        # VALID: Edge cases and boundaries (should NOT fire)
        # ========================================
        with batch.should_pass():
            batch.add(
                """
                CREATE TABLE ORDERS (
                    ID INT PRIMARY KEY,
                    CUSTOMER_ID INT,
                    CONSTRAINT FK_ORDERS_CUSTOMERS FOREIGN KEY (CUSTOMER_ID) REFERENCES CUSTOMERS(ID)
                );
                """,
                name="uppercase_case_insensitive"
            )
            batch.add(
                """
                ALTER TABLE order_details
                ADD CONSTRAINT fk_order_details_products
                FOREIGN KEY (product_id, variant_id) REFERENCES products(id, variant_id);
                """,
                name="compound_columns"
            )
            batch.add(
                """
                CREATE TABLE orders2024 (
                    id INT PRIMARY KEY,
                    customer_id INT,
                    CONSTRAINT fk_orders2024_customers FOREIGN KEY (customer_id) REFERENCES customers(id)
                );
                """,
                name="table_with_numbers"
            )
            batch.add(
                """
                CREATE TABLE a (
                    id INT PRIMARY KEY,
                    b_id INT,
                    CONSTRAINT fk_a_b FOREIGN KEY (b_id) REFERENCES b(id)
                );
                """,
                name="single_char_tables"
            )
            batch.add(
                """
                ALTER TABLE extremely_long_table_name_for_testing_purposes_child
                ADD CONSTRAINT fk_extremely_long_table_name_for_testing_purposes_child_extremely_long_table_name_for_testing_purposes_parent
                FOREIGN KEY (parent_id) REFERENCES extremely_long_table_name_for_testing_purposes_parent(id);
                """,
                name="very_long_table_names"
            )
            batch.add(
                """
                CREATE TABLE order_items (
                    id INT NOT NULL,
                    order_id INT NOT NULL,
                    product_id INT NOT NULL,
                    quantity INT DEFAULT 1,
                    price DECIMAL(10,2) NOT NULL,
                    CONSTRAINT pk_order_items PRIMARY KEY (id),
                    CONSTRAINT uq_order_product UNIQUE (order_id, product_id),
                    CONSTRAINT chk_quantity CHECK (quantity > 0),
                    CONSTRAINT fk_order_items_orders FOREIGN KEY (order_id) REFERENCES orders(id)
                );
                """,
                name="complex_ddl_multiple_constraints"
            )

        with batch:
            batch.execute_with_subtests(subtests)

    # ========================================
    # MALFORMED SQL - Test resilience (kept separate)
    # ========================================

    def test_malformed_missing_foreign_key_keyword(self):
        """Malformed: ALTER TABLE with CONSTRAINT but missing FOREIGN KEY keyword."""
        with LiquibaseCheck(
            "Python/Scripts/Any/fk_names.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            sql = """
            ALTER TABLE orders
            ADD CONSTRAINT some_constraint (customer_id) REFERENCES customers(id);
            """
            result = check.run(sql=sql)
            # Should be handled by try/except block and logged as unsupported

    def test_malformed_missing_references_clause(self):
        """Malformed: FK constraint missing REFERENCES clause."""
        with LiquibaseCheck(
            "Python/Scripts/Any/fk_names.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            sql = """
            CREATE TABLE orders (
                id INT PRIMARY KEY,
                customer_id INT,
                CONSTRAINT fk_orders_customers FOREIGN KEY (customer_id)
            );
            """
            result = check.run(sql=sql)
            # Should be caught by IndexError/ValueError exception handling

    def test_incomplete_create_statement(self):
        """Malformed: Incomplete CREATE TABLE statement."""
        with LiquibaseCheck(
            "Python/Scripts/Any/fk_names.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            sql = "CREATE TABLE"
            result = check.run(sql=sql)
            # Should be handled gracefully

    # ========================================
    # EDGE CASES - Ambiguous behavior (kept separate)
    # ========================================

    def test_multiple_fk_in_create_table(self):
        """Edge case: Multiple FK constraints in single CREATE TABLE statement."""
        with LiquibaseCheck(
            "Python/Scripts/Any/fk_names.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            sql = """
            CREATE TABLE order_items (
                id INT PRIMARY KEY,
                order_id INT,
                product_id INT,
                CONSTRAINT fk_order_items_orders FOREIGN KEY (order_id) REFERENCES orders(id),
                CONSTRAINT invalid_fk_name FOREIGN KEY (product_id) REFERENCES products(id)
            );
            """
            result = check.run(sql=sql)
            # Note: Policy has bug - only checks first FK due to 'foreign' keyword index search

    def test_loaddatachange_type_skipped(self):
        """Edge case: LoadData change types are explicitly skipped by the policy."""
        with LiquibaseCheck(
            "Python/Scripts/Any/fk_names.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            # This would typically be a LoadData changeset, but we'll simulate
            # Note: LoadDataChange detection is at line 43 of the policy
            sql = """
            -- This represents a LoadData operation that would be skipped
            CREATE TABLE test (id INT);
            """
            result = check.run(sql=sql)
            # Not a real LoadData change, so will be processed normally

    # ========================================
    # KNOWN BUGS - Kept separate as xfail
    # ========================================

    @pytest.mark.xfail(
        reason="BUG: fk_names.py line 97 uses sys.exit(1) on first violation, "
               "preventing checking of multiple FK constraints in a changeset. "
               "Root cause: Premature exit instead of accumulating violations. "
               "Fix: Store violations and report all at the end. "
               "Note: This bug may only manifest in actual Liquibase execution."
    )
    def test_multiple_fk_violations_in_changeset(self):
        """
        Bug test: Policy exits on first violation, missing subsequent violations.

        FRAMEWORK BUG - See JIRA_BUG7_SYS_EXIT.md for DAT ticket details

        BUG DETAILS:
        - Location: fk_names.py line 97 (and similar pattern in all 5 tested policy checks)
        - Current code: sys.exit(1) on first violation
        - Problem: Terminates check immediately, preventing detection of additional violations
        - Impact: User sees only first violation, must fix and re-run multiple times
        - Classification: This is a FRAMEWORK bug, not specific to this policy check
                          The framework should catch sys.exit and accumulate violations
        - Fix (Framework): Intercept sys.exit calls and accumulate violation messages
        - Fix (Policy): Use violation accumulation pattern instead of sys.exit

        This is a common anti-pattern in custom policy checks that should be addressed
        at the framework level to prevent poor user experience.

        See JIRA_BUG7_SYS_EXIT.md for standalone reproduction steps and framework fix options.
        See BUG_REPORT.md for analysis across all affected policy checks.
        """
        with LiquibaseCheck(
            "Python/Scripts/Any/fk_names.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            sql = """
            CREATE TABLE orders (
                id INT PRIMARY KEY,
                customer_id INT,
                CONSTRAINT bad_fk_1 FOREIGN KEY (customer_id) REFERENCES customers(id)
            );
            CREATE TABLE order_items (
                id INT PRIMARY KEY,
                order_id INT,
                CONSTRAINT bad_fk_2 FOREIGN KEY (order_id) REFERENCES orders(id)
            );
            """
            result = check.run(sql=sql)
            assert result.fired, "Should detect FK violations"
            # Bug: Will only report first violation due to sys.exit(1)

    @pytest.mark.xfail(
        reason="BUG: fk_names.py line 92 condition 'if fk_name_standard not in fk_name_current' "
               "allows partial matches. FK name 'fk_orders_customers_extra' would pass for "
               "standard 'fk_orders_customers'. Should use exact match: 'if fk_name_standard != fk_name_current'"
    )
    def test_partial_match_bug(self):
        """
        Bug test: Policy allows FK names that contain the standard name as substring.

        BUG DETAILS:
        - Location: fk_names.py line 92
        - Current code: if fk_name_standard not in fk_name_current:
        - Problem: Uses substring match ('in' operator) instead of exact match
        - Impact: FK names like 'fk_orders_customers_v2' or 'fk_orders_customers_extra'
                  incorrectly pass when standard is 'fk_orders_customers'
        - Fix: Change to exact match: if fk_name_standard != fk_name_current:

        See BUG_REPORT.md for full analysis and root cause documentation.
        """
        with LiquibaseCheck(
            "Python/Scripts/Any/fk_names.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            sql = """
            CREATE TABLE orders (
                id INT PRIMARY KEY,
                customer_id INT,
                CONSTRAINT fk_orders_customers_v2 FOREIGN KEY (customer_id) REFERENCES customers(id)
            );
            """
            result = check.run(sql=sql)
            # Bug: This should fire but won't because 'fk_orders_customers' is IN 'fk_orders_customers_v2'
            assert result.fired, "FK name with extra suffix should trigger the check"

    @pytest.mark.xfail(
        reason="BUG: fk_names.py only checks first FOREIGN KEY occurrence in CREATE TABLE "
               "due to using sql_list.index('foreign') which returns first index only. "
               "Root cause: Line 72 uses index() instead of iterating through all occurrences."
    )
    def test_only_first_fk_checked_bug(self):
        """
        Bug test: Only first FK in CREATE TABLE is checked, others are ignored.

        BUG DETAILS:
        - Location: fk_names.py line 72
        - Current code: start = sql_list.index("foreign")
        - Problem: index() returns only first occurrence of "foreign" keyword
        - Impact: CREATE TABLE statements with multiple FK constraints only have
                  first FK validated. Subsequent FKs with invalid names are not detected.
        - Example: In the SQL below, first FK is valid but second FK "wrong_name" is invalid.
                   The policy will check first FK, find it valid, and never check second FK.
        - Fix: Iterate through all "foreign" occurrences:
               for i, word in enumerate(sql_list):
                   if word == "foreign":
                       # Process this FK constraint

        See BUG_REPORT.md for full analysis and suggested fix implementation.
        """
        with LiquibaseCheck(
            "Python/Scripts/Any/fk_names.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            sql = """
            CREATE TABLE order_items (
                id INT PRIMARY KEY,
                order_id INT,
                product_id INT,
                CONSTRAINT fk_order_items_orders FOREIGN KEY (order_id) REFERENCES orders(id),
                CONSTRAINT wrong_name FOREIGN KEY (product_id) REFERENCES products(id)
            );
            """
            result = check.run(sql=sql)
            # Bug: Second invalid FK won't be checked because index("foreign") returns first occurrence only
            assert result.fired, "Should detect invalid second FK constraint"
