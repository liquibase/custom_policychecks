# 🔧 Configuration Steps
To utilize the checks provided, follow these configuration steps. The script path will have to be adjusted for your specific environment.

⚠️ *Script path includes name of the Python file*
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