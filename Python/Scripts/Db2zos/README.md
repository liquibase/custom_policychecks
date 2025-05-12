# 🔧 Configuration Steps
To utilize the checks provided, follow these configuration steps. The script path will have to be adjusted for your specific environment.

⚠️ *Script path includes name of the Python file*
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
# ☎️ Contact Liquibase
Liquibase sales: https://www.liquibase.com/contact-us<br>
Liquibase support (Pro customers only): https://support.liquibase.com