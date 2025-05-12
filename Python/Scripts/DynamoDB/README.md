# 🔧 Configuration Steps
To utilize the checks provided, follow these configuration steps. The script path will have to be adjusted for your specific environment.

⚠️ *Script path includes name of the Python file*
1. [**NoDeleteWithoutWhere**](Scripts/delete_without_where.py)
    | Key | Value |
    |--------|----------|
    | Database | Any |
    ```
    liquibase checks customize --check-name=CustomCheckTemplate
    ```
    | Prompt | Response |
    |--------|----------|
    | Short Name | NoDeleteWithoutWhere |
    | Severity | 0-4 |
    | Description | DELETE statements must have a WHERE clause. |
    | Scope | changelog |
    | Message | All DELETE statements must have a WHERE clause. |
    | Path | Scripts/delete_without_where.py |
    | Args |  |
    | Snapshot | false |
1. [**TableNamesMustBeUppercase**](Scripts/table_names_uppercase.py)
    | Key | Value |
    |--------|----------|
    | Database | Relational |
    ```
    liquibase checks customize --check-name=CustomCheckTemplate
    ```
    | Prompt | Response |
    |--------|----------|
    | Short Name | TableNamesMustBeUppercase |
    | Severity | 0-4 |
    | Description | Table names must be UPPERCASE. |
    | Scope | changelog |
    | Message | Table \_\_TABLE_NAME\_\_ must be UPPERCASE. |
    | Path | Scripts/table_names_uppercase.py |
    | Args |  |
    | Snapshot | false |
1. [**TableNameMustBeCamelCase**](Scripts/table_name_is_camelcase.py)
    | Key | Value |
    |--------|----------|
    | Database | Relational |
    ```
    liquibase checks customize --check-name=CustomCheckTemplate
    ```
    | Prompt | Response |
    |--------|----------|
    | Short Name | TableNameMustBeCamelCase |
    | Severity | 0-4 |
    | Description | Table name must be camelCase. |
    | Scope | changelog |
    | Message | |
    | Path | Scripts/table_name_is_camelcase.py |
    | Args |  |
    | Snapshot | false |
1. [**CollectionNameMustBeCamelCase**](Scripts/collection_name_is_camelcase.py)
    | Key | Value |
    |--------|----------|
    | Database | MongoDB/DocumentDB |
    ```
    liquibase checks customize --check-name=CustomCheckTemplate
    ```
    | Prompt | Response |
    |--------|----------|
    | Short Name | CollectionNameMustBeCamelCase |
    | Severity | 0-4 |
    | Description | Collection name must be camelCase. |
    | Scope | changelog |
    | Message | |
    | Path | Scripts/collection_name_is_camelcase.py |
    | Args |  |
    | Snapshot | false |
1. [**VarcharMaxSize**](Scripts/varchar_max_size.py)
    | Key | Value |
    |--------|----------|
    | Database | Oracle |
    ```
    liquibase checks customize --check-name=CustomCheckTemplate
    ```
    | Prompt | Response |
    |--------|----------|
    | Short Name | VarcharMaxSize |
    | Severity | 0-4 |
    | Description | Column names must not exceed VARCHAR_MAX size. |
    | Scope | database |
    | Message | Column \_\_COLUMN_NAME\_\_ exceeds \_\_COLUMN_SIZE\_\_. |
    | Path | Scripts/varchar_max_size.py |
    | Args | VARCHAR_MAX=255 |
    | Snapshot | false |
1. [**PKNamingConvention**](Scripts/pk_names.py)
    | Key | Value |
    |--------|----------|
    | Database | Relational |
    ```
    liquibase checks customize --check-name=CustomCheckTemplate
    ```
    | Prompt | Response |
    |--------|----------|
    | Short Name | PKNamingConvention |
    | Severity | 0-4 |
    | Description | Primary key names must include table name. |
    | Scope | database |
    | Message | Primary key name \_\_CURRENT_NAME\_\_ must include table name (\_\_NAME_STANDARD\_\_). |
    | Path | Scripts/pk_names.py |
    | Args | |
    | Snapshot | false |
1. [**VarcharDataIntegrity**](Scripts/varchar_data_integrity.py)
    | Key | Value |
    |--------|----------|
    | Database | Relational |
    ```
    liquibase checks customize --check-name=CustomCheckTemplate
    ```
    | Prompt | Response |
    |--------|----------|
    | Short Name | VarcharDataIntegrity |
    | Severity | 0-4 |
    | Description | VARCHAR columns cannot accept numeric data. |
    | Scope | changelog |
    | Message | Inserting numeric data into column \_\_COLUMN_NAME\_\_ is not allowed. |
    | Path | Scripts/varchar_data_integrity.py |
    | Args | |
    | Snapshot | true |
1. [**CollectionMustHaveValidator**](Scripts/collection_without_validator.py)
    | Key | Value |
    |--------|----------|
    | Database | MongoDB |
    ```
    liquibase checks customize --check-name=CustomCheckTemplate
    ```
    | Prompt | Response |
    |--------|----------|
    | Short Name | CollectionMustHaveValidator |
    | Severity | 0-4 |
    | Description | New collections must include a validator. |
    | Scope | changelog |
    | Message | New collections must include a validator. |
    | Path | Scripts/collection_without_validator.py |
    | Args |  |
    | Snapshot | false |
1. [**PKNamingConvention**](Scripts/pk_names_pg.py)
    | Key | Value |
    |--------|----------|
    | Database | Relational |
    ```
    liquibase checks customize --check-name=CustomCheckTemplate
    ```
    | Prompt | Response |
    |--------|----------|
    | Short Name | PKNamingPostgreSQL |
    | Severity | 0-4 |
    | Description | Name must be in the form of tablename_pkey. |
    | Scope | DATABASE |
    | Message | Primary key name \_\_CURRENT_NAME\_\_ must include table name.  Please use (\_\_NAME_STANDARD\_\_) instead. |
    | Path | Scripts/pk_names_pg.py |
    | Args | STANDARD=pkey |
    | Snapshot | false |
1. [**CreateIndexCount**](Scripts/create_index_count.py)
    | Key | Value |
    |--------|----------|
    | Database | Relational |
    ```
    liquibase checks customize --check-name=CustomCheckTemplate
    ```
    | Prompt | Response |
    |--------|----------|
    | Short Name | CreateIndexCount |
    | Severity | 0-4 |
    | Description | Tables can have a maximum of MAX_INDEX indexes. |
    | Scope | changelog |
    | Message | Table \_\_TABLE_NAME\_\_ would have \_\_INDEX_COUNT\_\_ indexes. |
    | Path | Scripts/create_index_count.py |
    | Args | MAX_INDEX=2 |
    | Snapshot | true |
1. [**TableColumnDisallow**](Scripts/table_column_disallow.py)
    | Key | Value |
    |--------|----------|
    | Database | Oracle |
    ```
    liquibase checks customize --check-name=CustomCheckTemplate
    ```
    | Prompt | Response |
    |--------|----------|
    | Short Name | TableColumnDisallow |
    | Severity | 0-4 |
    | Description | Warn if DATA_TYPE columns are used. |
    | Scope | changelog |
    | Message | Datatype \_\_COLUMN_TYPE\_\_ is discouraged for column \_\_COLUMN_NAME\_\_. |
    | Path | Scripts/table_column_disallow.py |
    | Args | DATA_TYPE=CLOB |
    | Snapshot | false |
1. [**TableColumnNameSize**](Scripts/table_column_name_size.py)
    | Key | Value |
    |--------|----------|
    | Database | Relational |
    ```
    liquibase checks customize --check-name=CustomCheckTemplate
    ```
    | Prompt | Response |
    |--------|----------|
    | Short Name | TableColumnNameSize |
    | Severity | 0-4 |
    | Description | Column names must be MAX_SIZE or lower in length. |
    | Scope | database |
    | Message | Name of \_\_OBJECT_TYPE\_\_ \_\_OBJECT_NAME\_\_ is \_\_CURRENT_SIZE\_\_ characters. |
    | Path | Scripts/table_column_name_size.py |
    | Args | MAX_SIZE=10 |
    | Snapshot | false |
1. [**CurrentSchemaOnly**](Scripts/current_schema_only.py)
    | Key | Value |
    |--------|----------|
    | Database | Oracle |
    ```
    liquibase checks customize --check-name=CustomCheckTemplate
    ```
    | Prompt | Response |
    |--------|----------|
    | Short Name | CurrentSchemaOnly |
    | Severity | 0-4 |
    | Description | Only changes in current schema are allowed. |
    | Scope | changelog |
    | Message | Only changes to schema \_\_SCHEMA_NAME\_\_ are allowed. |
    | Path | Scripts/current_schema_only.py |
    | Args | |
    | Snapshot | true |
1. [**FKNamingConvention**](Scripts/fk_names.py)
    | Key | Value |
    |--------|----------|
    | Database | Relational |
    ```
    liquibase checks customize --check-name=CustomCheckTemplate
    ```
    | Prompt | Response |
    |--------|----------|
    | Short Name | FKNamingConvention |
    | Severity | 0-4 |
    | Description | Foreign keys must include parent and child table names. |
    | Scope | changelog |
    | Message | Foreign key name \_\_NAME_CURRENT\_\_ must include parent and child table names (\_\_NAME_STANDARD\_\_). |
    | Path | Scripts/fk_names.py |
    | Args | |
    | Snapshot | false |
1. [**PKTablespace**](Scripts/pk_tablespace.py)
    | Key | Value |
    |--------|----------|
    | Database | Oracle |
    ```
    liquibase checks customize --check-name=CustomCheckTemplate
    ```
    | Prompt | Response |
    |--------|----------|
    | Short Name | PKTablespace |
    | Severity | 0-4 |
    | Description | Primary keys must include a tablespace definition. |
    | Scope | changelog |
    | Message | Primary key name \_\_PK_NAME\_\_ must include explicit tablespace definition. |
    | Path | Scripts/pk_tablespace.py |
    | Args | |
    | Snapshot | false |
1. [**ColumnDefaultValue**](Scripts/column_default_value.py)
    | Key | Value |
    |--------|----------|
    | Database | Oracle |
    ```
    liquibase checks customize --check-name=CustomCheckTemplate
    ```
    | Prompt | Response |
    |--------|----------|
    | Short Name | ColumnDefaultValue |
    | Severity | 0-4 |
    | Description | New columns must not have a default value assigned. |
    | Scope | changelog |
    | Message | Column \_\_COLUMN_NAME\_\_ in table \_\_TABLE_NAME\_\_ should not have a default value. |
    | Path | Scripts/column_default_value.py |
    | Args | |
    | Snapshot | false |
1. [**Varchar2MustUseChar**](Scripts/varchar2_must_use_char.py)
    | Key | Value |
    |--------|----------|
    | Database | Oracle |
    ```
    liquibase checks customize --check-name=CustomCheckTemplate
    ```
    | Prompt | Response |
    |--------|----------|
    | Short Name | Varchar2MustUseChar |
    | Severity | 0-4 |
    | Description | Varchar2 column Must Define Char instead of Bytes |
    | Scope | changelog |
    | Message | VARCHAR2 column \_\_COLUMN_NAME\_\_ must use CHAR instead of default BYTES |
    | Path | Scripts/varchar2_must_use_char.py |
    | Args | |
    | Snapshot | false |
1. [**VarcharPreferred**](Scripts/varchar_preferred.py)
    | Key | Value |
    |--------|----------|
    | Database | Oracle |
    ```
    liquibase checks customize --check-name=CustomCheckTemplate
    ```
    | Prompt | Response |
    |--------|----------|
    | Short Name | VarcharPreferred |
    | Severity | 0-4 |
    | Description | Warn if CHAR data type is used. |
    | Scope | database |
    | Message | Column \_\_COLUMN_NAME\_\_ has type CHAR, VARCHAR preferred. |
    | Path | Scripts/varchar_preferred.py |
    | Args | |
    | Snapshot | false |
1. [**CreateTableTablespace**](Scripts/create_table_tablespace.py)
    | Key | Value |
    |--------|----------|
    | Database | Oracle |
    ```
    liquibase checks customize --check-name=CustomCheckTemplate
    ```
    | Prompt | Response |
    |--------|----------|
    | Short Name | CreateTableTablespace |
    | Severity | 0-4 |
    | Description | New tables must include a tablespace definition. |
    | Scope | changelog |
    | Message | Table \_\_TABLE_NAME\_\_ must include explicit tablespace definition. |
    | Path | Scripts/create_table_tablespace.py |
    | Args | |
    | Snapshot | false |
1. [**IdentifiersWithoutQuotes**](Scripts/identifiers_without_quotes.py)
    | Key | Value |
    |--------|----------|
    | Database | Relational |
    ```
    liquibase checks customize --check-name=CustomCheckTemplate
    ```
    | Prompt | Response |
    |--------|----------|
    | Short Name | IdentifiersWithoutQuotes |
    | Severity | 0-4 |
    | Description | Identifiers should not include quotes. |
    | Scope | changelog |
    | Message | Identifier \_\_ID_NAME\_\_ should not include quotes. |
    | Path | Scripts/identifiers_without_quotes.py |
    | Args | |
    | Snapshot | false |
1. [**IndexMustUseDifferentTablespace**](Scripts/index_in_different_tablespace.py)
    | Key | Value |
    |--------|----------|
    | Database | Oracle |
    | Example Changesets | [**createindex.sql**](Changesets/createindex.sql)
    ```
    liquibase checks customize --check-name=CustomCheckTemplate
    ```
    | Prompt | Response |
    |--------|----------|
    | Short Name | IndexMustUseDifferentTablespace |
    | Severity | 0-4 |
    | Description | Index of table must be in a different tablespace than table. |
    | Scope | changelog |
    | Message | Index \_\_INDEX_NAME\_\_ must be in a different tablespace than \_\_TABLE_NAME\_\_ tablespace \_\_TABLE_SPACE\_\_ |
    | Path | Scripts/index_in_different_tablespace.py |
    | Args | |
    | Snapshot | true |
1. [**TestFormattedSQL**](Scripts/test_formatted_sql.py)
    | Key | Value |
    |--------|----------|
    | Changelog | Formatted SQL only |
    ```
    liquibase checks customize --check-name=CustomCheckTemplate
    ```
    | Prompt | Response |
    |--------|----------|
    | Short Name | TestFormattedSQL |
    | Severity | 0-4 |
    | Description | SQL files must include Liquibase meta data. |
    | Scope | changelog |
    | Message | SQL files must include Liquibase meta data. |
    | Path | Scripts/test_formatted_sql.py |
    | Args | |
    | Snapshot | false |
1. [**DynamoBillingModeCheck**](Scripts/billing_mode.py)
    | Key | Value |
    |--------|----------|
    | Database | DynamoDB |
    ```
    liquibase checks customize --check-name=CustomCheckTemplate
    ```
    | Prompt | Response |
    |--------|----------|
    | Short Name | DynamoBillingModeCheck |
    | Severity | 0-4 |
    | Description | Validate billinbg mode for new tables. |
    | Scope | changelog |
    | Message | Billing mode for new tables must be \_\_BILLING_MODE\_\_. |
    | Path | Scripts/billing_mode.py |
    | Args | BILLING_MODE=PROVISIONED |
    | Snapshot | false |
1. [**TimestampColumnName**](Scripts/timestamp_column_name.py)
    | Key | Value |
    |--------|----------|
    | Database | Relational |
    ```
    liquibase checks customize --check-name=CustomCheckTemplate
    ```
    | Prompt | Response |
    |--------|----------|
    | Short Name | TimestampColumnNamePython |
    | Severity | 0-4 |
    | Description | Timestamp column names must include _ts. |
    | Scope | changelog |
    | Message | Column name \_\_COLUMN_NAME\_\_ must include \_\_COLUMN_POSTFIX\_\_. |
    | Path | Scripts/timestamp_column_name.py |
    | Args | COLUMN_TYPE=TIMESTAMP, COLUMN_POSTFIX=_TS |
    | Snapshot | false |
1. [**TableRowCount**](Scripts/count_rows.py)
    | Key | Value |
    |--------|----------|
    | Database | Relational |
    ```
    liquibase checks customize --check-name=CustomCheckTemplate
    ```
    | Prompt | Response |
    |--------|----------|
    | Short Name | TableRowCount |
    | Severity | 0-4 |
    | Description | Count rows in a table. |
    | Scope | changelog |
    | Message | Total number of rows in the \_\_TABLE_NAME\_\_ table is: \_\_ROW_COUNT\_\_ |
    | Path | Scripts/count_rows.py |
    | Args | TABLE_NAME=databasechangelog |
    | Snapshot | false |
1. [**CheckBufferPool**](Scripts/check_buffer_pool.py)
    | Key | Value |
    |--------|----------|
    | Database | DB2 Z/OS |
    ```
    liquibase checks customize --check-name=CustomCheckTemplate
    ```
    | Prompt | Response |
    |--------|----------|
    | Short Name | CheckBufferPool |
    | Severity | 0-4 |
    | Description | Check Buffer Pool for a tablespace matches Default Buffer Pool for database. |
    | Scope | changelog |
	| Message | CREATE TABLESPACE Buffer Pool (\_\_BUFFER_POOL\_\_) must match the default Buffer Pool (\_\_DEFAULT_BUFFER_POOL\_\_) for the database (\_\_DATABASE_NAME\_\_). |
    | Path | Scripts/check_buffer_pool.py |
    | Args | |
    | Snapshot | false |
1. [**ShowRollback**](Scripts/show_rollback.py)
    | Key | Value |
    |--------|----------|
    | Database | Relational |
    ```
    liquibase checks customize --check-name=CustomCheckTemplate
    ```
    | Prompt | Response |
    |--------|----------|
    | Short Name | ShowRollback |
    | Severity | 0-4 |
    | Description | Sample to display rollback statements. |
    | Scope | changelog |
    | Message | Sample to display rollback statements. |
    | Path | Scripts/show_rollback.py |
    | Args | |
    | Snapshot | false |    
# ☎️ Contact Liquibase
Liquibase sales: https://www.liquibase.com/contact-us<br>
Liquibase support (Pro customers only): https://support.liquibase.com