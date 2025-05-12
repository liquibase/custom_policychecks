# 🔧 Configuration Steps
To utilize the checks provided, follow these configuration steps. The script path will have to be adjusted for your specific environment.

⚠️ *Script path includes name of the Python file*
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