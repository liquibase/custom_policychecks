# 🔧 Configuration Steps
To utilize the checks provided, follow these configuration steps. The script path will have to be adjusted for your specific environment.

⚠️ *Script path includes name of the Python file*
1. [**VarcharMaxSize**](varchar_max_size.py)
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
1. [**TableColumnDisallow**](table_column_disallow.py)
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
1. [**CurrentSchemaOnly**](current_schema_only.py)
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
1. [**PKTablespace**](pk_tablespace.py)
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
1. [**ColumnDefaultValue**](column_default_value.py)
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
1. [**Varchar2MustUseChar**](varchar2_must_use_char.py)
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
1. [**VarcharPreferred**](varchar_preferred.py)
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
1. [**CreateTableTablespace**](create_table_tablespace.py)
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
1. [**IndexMustUseDifferentTablespace**](index_in_different_tablespace.py)
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
    | Path | index_in_different_tablespace.py |
    | Args | |
    | Snapshot | true |
