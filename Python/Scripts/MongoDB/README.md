# 🔧 Configuration Steps
To utilize the checks provided, follow these configuration steps. The script path will have to be adjusted for your specific environment.

⚠️ *Script path includes name of the Python file*
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