"""
Comprehensive test suite for servicenow_chg_label.py custom policy check.

This check ensures that every changeset has a label that matches ServiceNow CHG format.
ServiceNow Change Request numbers follow the pattern: CHG followed by digits (e.g., CHG0010001).

Policy Purpose: Enforce traceability between Liquibase changesets and ServiceNow Change Management.
This ensures every database change is associated with an approved ServiceNow Change Request.

The policy:
- Checks all changesets in the changelog
- Looks for labels in each changeset
- Validates that at least one label matches the ServiceNow CHG pattern: CHG followed by 7 digits
- Pattern: CHG\d{7} (case-insensitive)
- Exits on first violation (sys.exit(1))

IMPORTANT: This policy check uses liquibase_utilities functions which require Liquibase execution.
All tests require actual Liquibase execution.
"""

import pytest
from liquibase_test_harness import LiquibaseCheck, CheckResult

# Message template from the policy check
MESSAGE_TEMPLATE = 'Changeset must have a ServiceNow CHG label (format: CHGxxxxxxx where x is a digit).'


# Mark all tests in this class as requiring Liquibase
@pytest.mark.requires_liquibase
class TestServiceNowCHGLabel:
    """Test suite for servicenow_chg_label.py policy check."""

    # ========================================
    # POLICY COMPLIANCE TESTS (Should NOT fire)
    # ========================================

    def test_changeset_with_valid_chg_label_passes(self):
        """Valid: Changeset with properly formatted CHG label should pass."""
        with LiquibaseCheck(
            "Python/Scripts/Any/servicenow_chg_label.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            sql = """
            CREATE TABLE users (
                id INT PRIMARY KEY,
                username VARCHAR(50),
                email VARCHAR(100)
            );
            """
            result = check.run(
                sql=sql,
                labels="CHG0010001"
            )
            assert not result.fired, "Changeset with valid CHG label should not trigger the check"

    def test_changeset_with_valid_chg_label_lowercase_passes(self):
        """Valid: CHG label in lowercase should pass (case-insensitive)."""
        with LiquibaseCheck(
            "Python/Scripts/Any/servicenow_chg_label.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            sql = """
            CREATE TABLE products (
                id INT PRIMARY KEY,
                name VARCHAR(100)
            );
            """
            result = check.run(
                sql=sql,
                labels="chg0010002"
            )
            assert not result.fired, "Changeset with lowercase CHG label should pass"

    def test_changeset_with_valid_chg_label_mixed_case_passes(self):
        """Valid: CHG label in mixed case should pass."""
        with LiquibaseCheck(
            "Python/Scripts/Any/servicenow_chg_label.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            sql = """
            CREATE TABLE orders (
                id BIGINT PRIMARY KEY,
                total DECIMAL(10,2)
            );
            """
            result = check.run(
                sql=sql,
                labels="ChG0010003"
            )
            assert not result.fired, "Changeset with mixed case CHG label should pass"

    def test_changeset_with_multiple_labels_including_chg_passes(self):
        """Valid: Changeset with multiple labels including a valid CHG should pass."""
        with LiquibaseCheck(
            "Python/Scripts/Any/servicenow_chg_label.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            sql = """
            CREATE TABLE inventory (
                id INT PRIMARY KEY,
                quantity INT
            );
            """
            result = check.run(
                sql=sql,
                labels="development,CHG0010004,hotfix"
            )
            assert not result.fired, "Changeset with multiple labels including CHG should pass"

    def test_changeset_with_chg_label_at_end_passes(self):
        """Valid: CHG label at the end of comma-separated labels should pass."""
        with LiquibaseCheck(
            "Python/Scripts/Any/servicenow_chg_label.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            sql = """
            ALTER TABLE users ADD COLUMN phone VARCHAR(20);
            """
            result = check.run(
                sql=sql,
                labels="production,urgent,CHG0010005"
            )
            assert not result.fired, "CHG label at end should pass"

    def test_changeset_with_chg_label_in_middle_passes(self):
        """Valid: CHG label in the middle of comma-separated labels should pass."""
        with LiquibaseCheck(
            "Python/Scripts/Any/servicenow_chg_label.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            sql = """
            CREATE INDEX idx_users_email ON users(email);
            """
            result = check.run(
                sql=sql,
                labels="migration,CHG0010006,approved"
            )
            assert not result.fired, "CHG label in middle should pass"

    def test_multiple_changesets_all_with_chg_labels_passes(self):
        """Valid: Multiple changesets each with CHG labels should all pass."""
        with LiquibaseCheck(
            "Python/Scripts/Any/servicenow_chg_label.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            # First changeset
            sql1 = """
            CREATE TABLE customers (
                id INT PRIMARY KEY,
                name VARCHAR(100)
            );
            """
            result1 = check.run(sql=sql1, labels="CHG0010007")
            assert not result1.fired, "First changeset should pass"

            # Second changeset
            sql2 = """
            CREATE TABLE orders (
                id INT PRIMARY KEY,
                customer_id INT
            );
            """
            result2 = check.run(sql=sql2, labels="CHG0010008")
            assert not result2.fired, "Second changeset should pass"

    # ========================================
    # POLICY VIOLATION TESTS (Should fire)
    # ========================================

    def test_changeset_without_labels_fires(self):
        """Invalid: Changeset without any labels should fire the check."""
        with LiquibaseCheck(
            "Python/Scripts/Any/servicenow_chg_label.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            sql = """
            CREATE TABLE events (
                id INT PRIMARY KEY,
                name VARCHAR(100)
            );
            """
            result = check.run(sql=sql)
            assert result.fired, "Changeset without labels should trigger the check"
            assert "CHG" in result.message or "ServiceNow" in result.message

    def test_changeset_with_empty_labels_fires(self):
        """Invalid: Changeset with empty labels attribute should fire."""
        with LiquibaseCheck(
            "Python/Scripts/Any/servicenow_chg_label.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            sql = """
            CREATE TABLE logs (
                id BIGINT PRIMARY KEY,
                message TEXT
            );
            """
            result = check.run(sql=sql, labels="")
            assert result.fired, "Changeset with empty labels should trigger the check"

    def test_changeset_with_non_chg_labels_fires(self):
        """Invalid: Changeset with labels that don't include CHG should fire."""
        with LiquibaseCheck(
            "Python/Scripts/Any/servicenow_chg_label.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            sql = """
            CREATE TABLE audit (
                id INT PRIMARY KEY,
                action VARCHAR(50)
            );
            """
            result = check.run(sql=sql, labels="development,production,hotfix")
            assert result.fired, "Changeset without CHG label should trigger the check"

    def test_changeset_with_invalid_chg_format_too_few_digits_fires(self):
        """Invalid: CHG label with too few digits should fire."""
        with LiquibaseCheck(
            "Python/Scripts/Any/servicenow_chg_label.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            sql = """
            CREATE TABLE metrics (
                id INT PRIMARY KEY,
                value DECIMAL(10,2)
            );
            """
            result = check.run(sql=sql, labels="CHG123")
            assert result.fired, "CHG label with too few digits should trigger the check"

    def test_changeset_with_invalid_chg_format_too_many_digits_fires(self):
        """Invalid: CHG label with too many digits should fire."""
        with LiquibaseCheck(
            "Python/Scripts/Any/servicenow_chg_label.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            sql = """
            CREATE TABLE settings (
                id INT PRIMARY KEY,
                config JSON
            );
            """
            result = check.run(sql=sql, labels="CHG00100011234")
            assert result.fired, "CHG label with too many digits should trigger the check"

    def test_changeset_with_chg_without_digits_fires(self):
        """Invalid: Label with 'CHG' but no digits should fire."""
        with LiquibaseCheck(
            "Python/Scripts/Any/servicenow_chg_label.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            sql = """
            CREATE TABLE notifications (
                id INT PRIMARY KEY,
                message TEXT
            );
            """
            result = check.run(sql=sql, labels="CHG")
            assert result.fired, "CHG without digits should trigger the check"

    def test_changeset_with_chg_with_letters_instead_of_digits_fires(self):
        """Invalid: CHG label with letters instead of digits should fire."""
        with LiquibaseCheck(
            "Python/Scripts/Any/servicenow_chg_label.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            sql = """
            CREATE TABLE reports (
                id INT PRIMARY KEY,
                title VARCHAR(200)
            );
            """
            result = check.run(sql=sql, labels="CHGABCDEFG")
            assert result.fired, "CHG with letters instead of digits should trigger the check"

    def test_changeset_with_partial_chg_match_fires(self):
        """Invalid: Label containing CHG but not matching pattern should fire."""
        with LiquibaseCheck(
            "Python/Scripts/Any/servicenow_chg_label.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            sql = """
            CREATE TABLE sessions (
                id INT PRIMARY KEY,
                token VARCHAR(255)
            );
            """
            result = check.run(sql=sql, labels="CHANGE0010001")
            assert result.fired, "Partial CHG match should trigger the check"

    def test_changeset_with_chg_in_middle_of_label_fires(self):
        """Invalid: CHG appearing in the middle of a label (not standalone) should fire."""
        with LiquibaseCheck(
            "Python/Scripts/Any/servicenow_chg_label.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            sql = """
            CREATE TABLE temp (
                id INT PRIMARY KEY
            );
            """
            result = check.run(sql=sql, labels="MYCHG0010001VALUE")
            assert result.fired, "CHG in middle of word should trigger the check"

    # ========================================
    # EDGE CASES
    # ========================================

    def test_changeset_with_whitespace_in_labels(self):
        """Edge case: Labels with whitespace should be handled correctly."""
        with LiquibaseCheck(
            "Python/Scripts/Any/servicenow_chg_label.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            sql = """
            CREATE TABLE whitespace_test (
                id INT PRIMARY KEY
            );
            """
            # With whitespace around valid CHG
            result = check.run(sql=sql, labels=" CHG0010009 ")
            assert not result.fired, "Whitespace around CHG label should be handled"

    def test_changeset_with_special_characters_in_labels(self):
        """Edge case: Labels with special characters alongside CHG."""
        with LiquibaseCheck(
            "Python/Scripts/Any/servicenow_chg_label.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            sql = """
            CREATE TABLE special_chars (
                id INT PRIMARY KEY
            );
            """
            result = check.run(sql=sql, labels="version-1.0,CHG0010010,feature/login")
            assert not result.fired, "Special characters in other labels should not affect CHG validation"

    def test_changeset_with_hyphenated_chg_fires(self):
        """Edge case: CHG with hyphens should fire (not valid format)."""
        with LiquibaseCheck(
            "Python/Scripts/Any/servicenow_chg_label.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            sql = """
            CREATE TABLE hyphen_test (
                id INT PRIMARY KEY
            );
            """
            result = check.run(sql=sql, labels="CHG-0010011")
            assert result.fired, "CHG with hyphen should trigger the check"

    def test_changeset_with_zero_padded_chg_passes(self):
        """Edge case: CHG with leading zeros (standard format) should pass."""
        with LiquibaseCheck(
            "Python/Scripts/Any/servicenow_chg_label.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            sql = """
            CREATE TABLE zero_padded (
                id INT PRIMARY KEY
            );
            """
            result = check.run(sql=sql, labels="CHG0000001")
            assert not result.fired, "CHG with leading zeros should pass"

    def test_multiple_chg_labels_in_same_changeset_passes(self):
        """Edge case: Multiple CHG labels in same changeset should pass."""
        with LiquibaseCheck(
            "Python/Scripts/Any/servicenow_chg_label.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            sql = """
            CREATE TABLE multi_chg (
                id INT PRIMARY KEY
            );
            """
            result = check.run(sql=sql, labels="CHG0010012,CHG0010013")
            assert not result.fired, "Multiple CHG labels should pass"

    # ========================================
    # BOUNDARY CONDITIONS
    # ========================================

    def test_chg_with_exactly_seven_digits_passes(self):
        """Boundary: CHG with exactly 7 digits should pass."""
        with LiquibaseCheck(
            "Python/Scripts/Any/servicenow_chg_label.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            sql = """
            CREATE TABLE boundary_test (
                id INT PRIMARY KEY
            );
            """
            result = check.run(sql=sql, labels="CHG1234567")
            assert not result.fired, "CHG with exactly 7 digits should pass"

    def test_chg_with_six_digits_fires(self):
        """Boundary: CHG with 6 digits should fire."""
        with LiquibaseCheck(
            "Python/Scripts/Any/servicenow_chg_label.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            sql = """
            CREATE TABLE six_digits (
                id INT PRIMARY KEY
            );
            """
            result = check.run(sql=sql, labels="CHG123456")
            assert result.fired, "CHG with only 6 digits should trigger the check"

    def test_chg_with_eight_digits_fires(self):
        """Boundary: CHG with 8 digits should fire."""
        with LiquibaseCheck(
            "Python/Scripts/Any/servicenow_chg_label.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            sql = """
            CREATE TABLE eight_digits (
                id INT PRIMARY KEY
            );
            """
            result = check.run(sql=sql, labels="CHG12345678")
            assert result.fired, "CHG with 8 digits should trigger the check"

    # ========================================
    # DIFFERENT SQL STATEMENT TYPES
    # ========================================

    def test_create_table_with_valid_chg_passes(self):
        """Valid: CREATE TABLE with valid CHG label should pass."""
        with LiquibaseCheck(
            "Python/Scripts/Any/servicenow_chg_label.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            sql = """
            CREATE TABLE test_create (
                id INT PRIMARY KEY,
                name VARCHAR(100)
            );
            """
            result = check.run(sql=sql, labels="CHG0020001")
            assert not result.fired

    def test_alter_table_with_valid_chg_passes(self):
        """Valid: ALTER TABLE with valid CHG label should pass."""
        with LiquibaseCheck(
            "Python/Scripts/Any/servicenow_chg_label.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            sql = """
            ALTER TABLE test_create ADD COLUMN email VARCHAR(100);
            """
            result = check.run(sql=sql, labels="CHG0020002")
            assert not result.fired

    def test_insert_with_valid_chg_passes(self):
        """Valid: INSERT with valid CHG label should pass."""
        with LiquibaseCheck(
            "Python/Scripts/Any/servicenow_chg_label.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            sql = """
            INSERT INTO test_create (id, name) VALUES (1, 'Test');
            """
            result = check.run(sql=sql, labels="CHG0020003")
            assert not result.fired

    def test_drop_table_with_valid_chg_passes(self):
        """Valid: DROP TABLE with valid CHG label should pass."""
        with LiquibaseCheck(
            "Python/Scripts/Any/servicenow_chg_label.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            sql = """
            DROP TABLE IF EXISTS old_table;
            """
            result = check.run(sql=sql, labels="CHG0020004")
            assert not result.fired

    def test_create_index_with_valid_chg_passes(self):
        """Valid: CREATE INDEX with valid CHG label should pass."""
        with LiquibaseCheck(
            "Python/Scripts/Any/servicenow_chg_label.py",
            message=MESSAGE_TEMPLATE
        ) as check:
            sql = """
            CREATE INDEX idx_test ON test_create(name);
            """
            result = check.run(sql=sql, labels="CHG0020005")
            assert not result.fired
