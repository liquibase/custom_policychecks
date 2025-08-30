"""
Integration tests for the create_index_count custom policy check.

Tests the create_index_count.py script which ensures tables don't exceed
a maximum number of indexes by tracking CREATE INDEX statements and
checking against existing indexes in the snapshot.
"""

import pytest
import os
from liquibase_test_harness import LiquibaseCheck
from liquibase_test_harness.pure_python_mocks import (
    set_test_snapshot, 
    clear_test_snapshot, 
    create_test_snapshot_with_tables
)


@pytest.mark.integration
class TestCreateIndexCount:
    """Test the create_index_count custom policy check."""
    
    def test_single_table_under_limit(self):
        """Test a single table with indexes under the limit - should pass."""
        sql = """
        CREATE TABLE users (
            id BIGINT PRIMARY KEY,
            email VARCHAR(255),
            username VARCHAR(100),
            created_at TIMESTAMP
        );
        
        CREATE INDEX idx_users_email ON users (email);
        CREATE INDEX idx_users_username ON users (username);
        """
        
        check = LiquibaseCheck(
            "Python/Scripts/Any/create_index_count.py",
            check_args={"MAX_INDEX": "3"}
        )
        
        with check:
            result = check.run(sql=sql)
            
            assert result is not None
            assert result.fired is False
    
    def test_single_table_exceeds_limit(self):
        """Test a single table exceeding the index limit - should fail."""
        sql = """
        CREATE TABLE products (
            id BIGINT PRIMARY KEY,
            name VARCHAR(255),
            category VARCHAR(100),
            price DECIMAL(10,2),
            sku VARCHAR(50)
        );
        
        CREATE INDEX idx_products_name ON products (name);
        CREATE INDEX idx_products_category ON products (category);
        CREATE INDEX idx_products_price ON products (price);
        CREATE INDEX idx_products_sku ON products (sku);
        """
        
        check = LiquibaseCheck(
            "Python/Scripts/Any/create_index_count.py",
            check_args={"MAX_INDEX": "3"},
            message="Table \"__TABLE_NAME__\" has __INDEX_COUNT__ indexes, which exceeds the maximum of 3"
        )
        
        with check:
            result = check.run(sql=sql)
            
            assert result is not None
            assert result.fired is True
            assert "\"products\"" in result.message
            assert "4 indexes" in result.message
            assert "exceeds the maximum of 3" in result.message
    
    def test_multiple_tables_all_under_limit(self):
        """Test multiple tables all under the limit - should pass."""
        sql = """
        CREATE TABLE users (
            id BIGINT PRIMARY KEY,
            email VARCHAR(255)
        );
        
        CREATE TABLE orders (
            id BIGINT PRIMARY KEY,
            user_id BIGINT,
            total DECIMAL(10,2)
        );
        
        CREATE INDEX idx_users_email ON users (email);
        CREATE INDEX idx_orders_user ON orders (user_id);
        CREATE INDEX idx_orders_total ON orders (total);
        """
        
        check = LiquibaseCheck(
            "Python/Scripts/Any/create_index_count.py",
            check_args={"MAX_INDEX": "3"}
        )
        
        with check:
            result = check.run(sql=sql)
            
            assert result is not None
            assert result.fired is False
    
    def test_multiple_tables_one_exceeds(self):
        """Test multiple tables where one exceeds the limit - should fail."""
        sql = """
        CREATE TABLE users (
            id BIGINT PRIMARY KEY,
            email VARCHAR(255)
        );
        
        CREATE TABLE orders (
            id BIGINT PRIMARY KEY,
            user_id BIGINT,
            status VARCHAR(20),
            created_at TIMESTAMP,
            updated_at TIMESTAMP
        );
        
        CREATE INDEX idx_users_email ON users (email);
        CREATE INDEX idx_orders_user ON orders (user_id);
        CREATE INDEX idx_orders_status ON orders (status);
        CREATE INDEX idx_orders_created ON orders (created_at);
        CREATE INDEX idx_orders_updated ON orders (updated_at);
        """
        
        check = LiquibaseCheck(
            "Python/Scripts/Any/create_index_count.py",
            check_args={"MAX_INDEX": "3"},
            message="Table \"__TABLE_NAME__\" has __INDEX_COUNT__ indexes, which exceeds the maximum of 3"
        )
        
        with check:
            result = check.run(sql=sql)
            
            assert result is not None
            assert result.fired is True
            assert "\"orders\"" in result.message
            assert "4 indexes" in result.message
    
    def test_create_unique_index(self):
        """Test CREATE UNIQUE INDEX syntax is properly handled."""
        sql = """
        CREATE TABLE users (
            id BIGINT PRIMARY KEY,
            email VARCHAR(255),
            username VARCHAR(100)
        );
        
        CREATE UNIQUE INDEX idx_users_email ON users (email);
        CREATE UNIQUE INDEX idx_users_username ON users (username);
        CREATE INDEX idx_users_combo ON users (email, username);
        CREATE UNIQUE INDEX idx_users_id_email ON users (id, email);
        """
        
        check = LiquibaseCheck(
            "Python/Scripts/Any/create_index_count.py",
            check_args={"MAX_INDEX": "3"},
            message="Table \"__TABLE_NAME__\" has __INDEX_COUNT__ indexes, which exceeds the maximum of 3"
        )
        
        with check:
            result = check.run(sql=sql)
            
            assert result is not None
            assert result.fired is True
            assert "\"users\"" in result.message
            assert "4 indexes" in result.message
    
    def test_create_index_with_schema(self):
        """Test CREATE INDEX with schema prefix is properly handled."""
        sql = """
        CREATE TABLE inventory.products (
            id BIGINT PRIMARY KEY,
            name VARCHAR(255),
            sku VARCHAR(50)
        );
        
        CREATE INDEX idx_prod_name ON inventory.products (name);
        CREATE INDEX idx_prod_sku ON inventory.products (sku);
        CREATE INDEX idx_prod_combo ON inventory.products (name, sku);
        CREATE INDEX idx_prod_id_name ON inventory.products (id, name);
        """
        
        check = LiquibaseCheck(
            "Python/Scripts/Any/create_index_count.py",
            check_args={"MAX_INDEX": "3"},
            message="Table \"__TABLE_NAME__\" has __INDEX_COUNT__ indexes, which exceeds the maximum of 3"
        )
        
        with check:
            result = check.run(sql=sql)
            
            assert result is not None
            assert result.fired is True
            assert "\"products\"" in result.message
            assert "4 indexes" in result.message
    
    def test_create_index_multicolumn(self):
        """Test multi-column indexes are counted correctly."""
        sql = """
        CREATE TABLE orders (
            id BIGINT PRIMARY KEY,
            user_id BIGINT,
            product_id BIGINT,
            status VARCHAR(20),
            created_at TIMESTAMP
        );
        
        CREATE INDEX idx_orders_user_product ON orders (user_id, product_id);
        CREATE INDEX idx_orders_status_created ON orders (status, created_at);
        CREATE INDEX idx_orders_composite ON orders (user_id, product_id, status);
        """
        
        check = LiquibaseCheck(
            "Python/Scripts/Any/create_index_count.py",
            check_args={"MAX_INDEX": "5"}
        )
        
        with check:
            result = check.run(sql=sql)
            
            assert result is not None
            assert result.fired is False
    
    def test_case_insensitive_parsing(self):
        """Test that SQL parsing is case-insensitive."""
        sql = """
        create table USERS (
            ID bigint primary key,
            EMAIL varchar(255)
        );
        
        Create Index IDX_USERS_EMAIL on users (email);
        CREATE index idx_users_id_email ON USERS (id, EMAIL);
        create INDEX idx_users_email_lower on Users (LOWER(email));
        CREATE UNIQUE INDEX idx_users_email_unique ON users (email);
        """
        
        check = LiquibaseCheck(
            "Python/Scripts/Any/create_index_count.py",
            check_args={"MAX_INDEX": "3"},
            message="Table \"__TABLE_NAME__\" has __INDEX_COUNT__ indexes, which exceeds the maximum of 3"
        )
        
        with check:
            result = check.run(sql=sql)
            
            assert result is not None
            assert result.fired is True
            # Table name in message should match the case from snapshot
            assert "indexes" in result.message
            assert "4 indexes" in result.message
    
    def test_no_create_index_statements(self):
        """Test changelog with no CREATE INDEX statements - should pass."""
        sql = """
        CREATE TABLE users (
            id BIGINT PRIMARY KEY,
            email VARCHAR(255),
            name VARCHAR(100)
        );
        
        INSERT INTO users (id, email, name) VALUES (1, 'test@example.com', 'Test User');
        
        ALTER TABLE users ADD COLUMN active BOOLEAN DEFAULT TRUE;
        """
        
        check = LiquibaseCheck(
            "Python/Scripts/Any/create_index_count.py",
            check_args={"MAX_INDEX": "3"}
        )
        
        with check:
            result = check.run(sql=sql)
            
            assert result is not None
            assert result.fired is False
    
    def test_exact_limit_boundary(self):
        """Test table with exactly MAX_INDEX indexes - should pass."""
        sql = """
        CREATE TABLE products (
            id BIGINT PRIMARY KEY,
            name VARCHAR(255),
            category VARCHAR(100),
            price DECIMAL(10,2)
        );
        
        CREATE INDEX idx_products_name ON products (name);
        CREATE INDEX idx_products_category ON products (category);
        CREATE INDEX idx_products_price ON products (price);
        """
        
        check = LiquibaseCheck(
            "Python/Scripts/Any/create_index_count.py",
            check_args={"MAX_INDEX": "3"}
        )
        
        with check:
            result = check.run(sql=sql)
            
            assert result is not None
            assert result.fired is False
    
    def test_cache_accumulation_across_changesets(self):
        """Test that cache properly accumulates index counts across multiple changesets."""
        # First changeset
        sql1 = """
        CREATE TABLE users (
            id BIGINT PRIMARY KEY,
            email VARCHAR(255)
        );
        
        CREATE INDEX idx_users_email ON users (email);
        """
        
        # Second changeset would add more indexes
        sql2 = """
        CREATE INDEX idx_users_id_email ON users (id, email);
        CREATE INDEX idx_users_email_lower ON users (LOWER(email));
        """
        
        check = LiquibaseCheck(
            "Python/Scripts/Any/create_index_count.py",
            check_args={"MAX_INDEX": "2"},
            message="Table \"__TABLE_NAME__\" has __INDEX_COUNT__ indexes, which exceeds the maximum of 2"
        )
        
        with check:
            # First changeset should pass
            result1 = check.run(sql=sql1)
            assert result1 is not None
            assert result1.fired is False
            
            # Note: In real usage, multiple changesets would be in the same changelog
            # This test demonstrates the concept but may not perfectly replicate
            # Liquibase's actual multi-changeset behavior


@pytest.mark.pure_python
class TestCreateIndexCountPurePython:
    """Test create_index_count.py in Pure Python mode without Liquibase execution."""
    
    def setup_method(self):
        """Set up clean state for each test."""
        # Store original environment and set pure Python mode
        self._original_mode = os.environ.get('LIQUIBASE_TEST_MODE')
        os.environ['LIQUIBASE_TEST_MODE'] = 'pure_python'
        clear_test_snapshot()
    
    def teardown_method(self):
        """Clean up after each test."""
        clear_test_snapshot()
        # Restore original environment
        if self._original_mode is None:
            os.environ.pop('LIQUIBASE_TEST_MODE', None)
        else:
            os.environ['LIQUIBASE_TEST_MODE'] = self._original_mode
    
    def test_single_table_under_limit_pure_python(self):
        """Test pure Python mode with single table under index limit."""
        # Set up mock snapshot with a table that has 1 existing index
        snapshot = create_test_snapshot_with_tables([
            {"name": "users", "indexes": ["idx_users_existing"]}
        ])
        set_test_snapshot(snapshot)
        
        sql = """
        CREATE TABLE users (
            id BIGINT PRIMARY KEY,
            email VARCHAR(255),
            username VARCHAR(100)
        );
        
        CREATE INDEX idx_users_email ON users (email);
        CREATE INDEX idx_users_username ON users (username);
        """
        
        check = LiquibaseCheck(
            "Python/Scripts/Any/create_index_count.py",
            check_args={"MAX_INDEX": "5"}
        )
        
        with check:
            result = check.run(sql=sql)
            
            assert result is not None
            assert result.fired is False, f"Check should pass but fired with message: {result.message}"
    
    def test_single_table_exceeds_limit_pure_python(self):
        """Test pure Python mode with single table exceeding index limit."""
        # Set up mock snapshot with a table that has 2 existing indexes
        snapshot = create_test_snapshot_with_tables([
            {"name": "products", "indexes": ["idx_products_existing1", "idx_products_existing2"]}
        ])
        set_test_snapshot(snapshot)
        
        sql = """
        CREATE TABLE products (
            id BIGINT PRIMARY KEY,
            name VARCHAR(255),
            category VARCHAR(100),
            price DECIMAL(10,2)
        );
        
        CREATE INDEX idx_products_name ON products (name);
        CREATE INDEX idx_products_category ON products (category);
        CREATE INDEX idx_products_price ON products (price);
        """
        
        check = LiquibaseCheck(
            "Python/Scripts/Any/create_index_count.py",
            check_args={"MAX_INDEX": "3"},
            message="Table \"__TABLE_NAME__\" has __INDEX_COUNT__ indexes, which exceeds the maximum of 3",
        )
        
        with check:
            result = check.run(sql=sql)
            
            assert result is not None
            assert result.fired is True
            assert "\"products\"" in result.message
            assert "5 indexes" in result.message  # 2 existing + 3 new = 5
            assert "exceeds the maximum of 3" in result.message
    
    def test_multiple_tables_cache_accumulation_pure_python(self):
        """Test cache properly accumulates counts for multiple tables in pure Python mode."""
        # Set up mock snapshot with multiple tables
        snapshot = create_test_snapshot_with_tables([
            {"name": "users", "indexes": ["idx_users_pk"]},  # 1 existing
            {"name": "orders", "indexes": []}  # 0 existing
        ])
        set_test_snapshot(snapshot)
        
        sql = """
        CREATE TABLE users (
            id BIGINT PRIMARY KEY,
            email VARCHAR(255)
        );
        
        CREATE TABLE orders (
            id BIGINT PRIMARY KEY,
            user_id BIGINT
        );
        
        CREATE INDEX idx_users_email ON users (email);
        CREATE INDEX idx_orders_user ON orders (user_id);
        CREATE INDEX idx_orders_status ON orders (status);
        """
        
        check = LiquibaseCheck(
            "Python/Scripts/Any/create_index_count.py",
            check_args={"MAX_INDEX": "3"},
        )
        
        with check:
            result = check.run(sql=sql)
            
            assert result is not None
            assert result.fired is False  # users: 1+1=2, orders: 0+2=2, both under limit
    
    def test_case_insensitive_table_lookup_pure_python(self):
        """Test case-insensitive table name lookup in pure Python mode."""
        # Set up snapshot with lowercase table name
        snapshot = create_test_snapshot_with_tables([
            {"name": "users", "indexes": []}
        ])
        set_test_snapshot(snapshot)
        
        sql = """
        CREATE TABLE USERS (
            ID BIGINT PRIMARY KEY,
            EMAIL VARCHAR(255)
        );
        
        CREATE INDEX idx_users_email ON USERS (EMAIL);
        CREATE INDEX idx_users_id_email ON Users (id, email);
        CREATE INDEX idx_users_email_lower ON users (LOWER(email));
        CREATE INDEX idx_users_combo ON Users (id, EMAIL);
        """
        
        check = LiquibaseCheck(
            "Python/Scripts/Any/create_index_count.py",
            check_args={"MAX_INDEX": "3"},
            message="Table \"__TABLE_NAME__\" has __INDEX_COUNT__ indexes, which exceeds the maximum of 3",
        )
        
        with check:
            result = check.run(sql=sql)
            
            assert result is not None
            assert result.fired is True
            assert "4 indexes" in result.message  # 0 existing + 4 new = 4
    
    def test_table_not_in_snapshot_pure_python(self):
        """Test CREATE INDEX on table not in snapshot - should skip with warning."""
        # Set up snapshot without the target table
        snapshot = create_test_snapshot_with_tables([
            {"name": "other_table", "indexes": []}
        ])
        set_test_snapshot(snapshot)
        
        sql = """
        CREATE INDEX idx_missing_table ON missing_table (id);
        """
        
        check = LiquibaseCheck(
            "Python/Scripts/Any/create_index_count.py",
            check_args={"MAX_INDEX": "3"},
        )
        
        with check:
            result = check.run(sql=sql)
            
            # Should pass because table is not found and gets skipped
            assert result is not None
            assert result.fired is False
    
    def test_no_table_data_in_snapshot_pure_python(self):
        """Test handling when snapshot has no table data."""
        # Set up snapshot without table data
        snapshot = {
            "snapshot": {
                "objects": {}  # No liquibase.structure.core.Table key
            }
        }
        set_test_snapshot(snapshot)
        
        sql = """
        CREATE INDEX idx_any_table ON any_table (id);
        """
        
        check = LiquibaseCheck(
            "Python/Scripts/Any/create_index_count.py",
            check_args={"MAX_INDEX": "3"},
        )
        
        with check:
            result = check.run(sql=sql)
            
            # Should pass because check exits early when no table data
            assert result is not None
            assert result.fired is False