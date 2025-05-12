# 🔧 Configuration Steps
To utilize the checks provided, follow these configuration steps. The script path will have to be adjusted for your specific environment.

⚠️ *Script path includes name of the Python file*
1. [**PKNamingConvention**](Scripts/pk_names_pg.py)
    | Key | Value |
    |--------|----------|
    | Database | PostgreSQL |
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