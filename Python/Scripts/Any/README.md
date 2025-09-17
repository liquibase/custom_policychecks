# 🔧 Configuration Steps
To utilize the checks provided, follow these configuration steps. The script path will have to be adjusted for your specific environment.

⚠️ *Script path includes name of the Python file*
1. [**NoDeleteWithoutWhere**](delete_without_where.py)
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
1. [**TableNamesMustBeUppercase**](table_names_uppercase.py)
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
1. [**TableNameMustBeCamelCase**](table_name_is_camelcase.py)
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
1. [**PKNamingConvention**](pk_names.py)
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
1. [**VarcharDataIntegrity**](varchar_data_integrity.py)
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
1. [**CreateIndexCount**](create_index_count.py)
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
1. [**TableColumnNameSize**](table_column_name_size.py)
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
1. [**FKNamingConvention**](fk_names.py)
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
1. [**IdentifiersWithoutQuotes**](identifiers_without_quotes.py)
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
1. [**TimestampColumnName**](timestamp_column_name.py)
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
1. [**TableRowCount**](count_rows.py)
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
1. [**ShowRollback**](show_rollback.py)
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
1. [**PIISSN**](pii_ssn.py)
    | Key | Value |
    |--------|----------|
    | Database | Relational |
    ```
    liquibase checks customize --check-name=CustomCheckTemplate
    ```
    | Prompt | Response |
    |--------|----------|
    | Short Name | PIISSN |
    | Severity | 0-4 |
    | Description | Ensure raw SSNs are not used. |
    | Scope | changelog |
    | Message | Ensure raw SSNs are not used. |
    | Type | python |
    | Path | Scripts/pii_ssn.py |
    | Args |  |
    | Snapshot | false |
1. [**PIIPAN**](pii_pan.py)
    | Key | Value |
    |--------|----------|
    | Database | Relational |
    ```
    liquibase checks customize --check-name=CustomCheckTemplate
    ```
    | Prompt | Response |
    |--------|----------|
    | Short Name | PIIPAN |
    | Severity | 0-4 |
    | Description | Ensure raw PANs are not used. |
    | Scope | changelog |
    | Message | Ensure raw PANs are not used. |
    | Type | python |
    | Path | Scripts/pii_pan.py |
    | Args |  |
    | Snapshot | false |
