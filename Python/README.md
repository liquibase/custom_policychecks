<p align="left">
  <img src="../img/liquibase.png" alt="Liquibase Logo" title="Liquibase Logo" width="324" height="72">
</p>

# 🔒 Liquibase Pro Python Policy Checks
This repository is a collection of Liquibase Pro Python Policy checks. These checks have been created by the Liquibase community, including our customers and field engineers. You are encouraged to use these rules in your own Liquibase Pro pipelines.

If you need any help with these rules, please contact support@liquibase.com and our team will be happy to assist you (Pro customers only).

# 💡 Useful Links
| Description | Source |
|-------------|--------|
| Documentation| [Liquibase](https://docs.liquibase.com/liquibase-pro/policy-checks/custom-policy-checks/home.html)
| Python code reference | [W3Schools.com](https://www.w3schools.com/python/default.asp)
| SQL parse module reference | [ReadTheDocs.io](https://sqlparse.readthedocs.io/en/latest/)
| GraalPy (optional, required for custom virtual environments) | [GitHub.com](https://github.com/oracle/graalpython/releases)
| GraalPy reference | [Medium.com](https://medium.com/graalvm/graalpy-quick-reference-0488b661a57c)
| venv reference | [Python.org](https://docs.python.org/3/library/venv.html)

# ✔️ Pre-Execution Steps
1. Java 17 or higher is required. 
1. Download the latest version of [Liquibase](https://www.liquibase.com/download). Beginning with version 4.31.0, the policy check jar is included. Older versions require the latest [checks jar](https://repo1.maven.org/maven2/org/liquibase/ext/liquibase-checks/) to be placed inside the liquibase/lib folder.
1. Ensure this environment variable or setting is set to enable custom policy checks.<br>
    *Environment variable*
    ```
    LIQUIBASE_COMMAND_CHECKS_RUN_CHECKS_SCRIPTS_ENABLED='true'
    ```
    *liquibase.properties*
    ```
    checks-scripts-enabled=true
    ```

# 📒 Notes
1. To aid in debugging, it's useful to disable all other policy checks.
    ```
    liquibase checks bulk-set --disable
    ```
1. Sample relational and NoSQL changelogs are available in the [Changesets](Changesets/) folder.
1. Scripts are called once for each changeset (changelog scope) or once for each database object (database scope). Changesets may contain multiple SQL statements.
1. The print() function can be used to display debugging messages (instead of just liquibase_logger). This works regardless of log_level. Additionally, f strings automatically convert variables for printing and remove the need for concatenation to build a string of static and dynamic text.
    ```
    my_int = 123
    my_str = "Hello World!"
    print(f"{my_str} My variable is: {my_int}")
    ```
    f strings can also be used wherever strings are expected.
    ```
    my_int = 123
    liquibase_status.message = f"My variable is: {my_int}"
    ```
1. The latest [Liquibase provided modules](https://docs.liquibase.com/liquibase-pro/policy-checks/custom-policy-checks/api-helper-scripts.html) can be imported into your checks to access Liquibase provided functions.
    ```
    import liquibase_utilities
    import liquibase_changesets

    print(liquibase_changesets.get_labels(liquibase_utilities.get_changeset()))
    ```
1. LoadData change types are not currently supported. 
1. Having the commercial Mongo extension in the lib directory will cause some relational change types to behave incorrectly (e.g., createIndex). 
1. Environment variables can be accessed using the os module.
    ```
    import os

    print(os.environ.get("LIQUIBASE_COMMAND_URL"))
    ```

# 🔎 Specific Examples
1. Error messages can be customized by adding a string to be replaced when defining the custom policy check. See [TableNamesMustBeUppercase](Scripts/table_names_uppercase.py).
1. Arguments defined at check creation/modification can be passed in to scripts. See [TableRowCount](Scripts/count_rows.py).
1. Values can be saved/retrieved between check runs using a cache. See [CreateIndexCount](Scripts/create_index_count.py).
1. Most of the provided changelog checks use string parsing to process SQL and support only simple statements. The [sqlparse](https://pypi.org/project/sqlparse/) module can be used for more complex statements. See [NoDeleteWithoutWhere](Scripts/delete_without_where.py) and [TimestampColumnName](Scripts/timestamp_column_name.py).
1. SQL can be executed as part of a custom policy check. See [TableRowCount](Scripts/count_rows.py).
1. Test for required [Liquibase metadata](https://docs.liquibase.com/concepts/changelogs/sql-format.html). See [TestFormattedSQL](Scripts/test_formatted_sql.py).

# 🐍 Local Python Environment
⚠️ *Not required to use or develop custom policy checks*

Instead of the built-in Python virtual environment Liquibase provides, a custom one can be utilized. This is useful if there are additional Python modules you want to import into your custom policy checks. To create one, follow these steps:
1. Download and extract GraalPy.
1. Add \<install dir\>/bin (or \<install dir\>\bin for Windows) to your path.
1. Create a Python virtual environment and directory structure. Once created the environment can be moved to a different folder (provided the Liquibase environment variable is also updated).

    ⚠️ *Use GitBash for Windows to execute commands*

    ```
    graalpy -m venv <virtual env path>
    ```
1. Activate the environment to install modules to the local virtual environment.<br>
    *Linux*
    ```
    source <virtual env path>/bin/activate
    ```
    *Windows*
    ```
    source <virtual env path>/Scripts/activate
    ```
1. Install Python modules in the new environment.

    ⚠️ *Sqlparse is required*
    ```
    graalpy -m pip install sqlparse
    ```
1. Deactive the environment (exit or run bin/deactivate). Deactivate on Windows may throw an error (safe to close the GitBash window).
1. Configure Liquibase to point to the new virtual environment.<br>
    *Linux*
    ```
    LIQUIBASE_SCRIPT_PYTHON_EXECUTABLE_PATH="<virtual env path>/bin/python"
    ```
    *Windows*
     ```
    LIQUIBASE_SCRIPT_PYTHON_EXECUTABLE_PATH='<virtual env path>\Scripts\python.exe'
    ```
1. Run checks as normal. To revert back to the built-in environment, unset the environment variable.

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
# ☎️ Contact Liquibase
Liquibase sales: https://www.liquibase.com/contact-us<br>
Liquibase support (Pro customers only): https://support.liquibase.com