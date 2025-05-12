# 🔧 Configuration Steps
To utilize the checks provided, follow these configuration steps. The script path will have to be adjusted for your specific environment.

⚠️ *Script path includes name of the Python file*
1. [**ShowRollback**](Scripts/illegalAlter.py)
    | Key | Value |
    |--------|----------|
    | Database | MySQL |
    ```
    liquibase checks customize --check-name=CustomCheckTemplate
    ```
    | Prompt | Response |
    |--------|----------|
    | Short Name | IllegalAlter |
    | Severity | 0-4 |
    | Description | Sample to display rollback statements. |
    | Scope | changelog |
    | Message | Check addresses a MySQL 8.0 issue |
    | Path | Scripts/illegalAlter.py |
    | Args | |
    | Snapshot | true |    