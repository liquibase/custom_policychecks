<p align="left">
  <img src="../img/liquibase.png" alt="Liquibase Logo" title="Liquibase Logo" width="324" height="72">
</p>

# 🔒 Liquibase Pro Regex Policy Checks
This repository is a collection of Liquibase Pro Regex Policy checks. These checks have been created by the Liquibase community, including our customers and field engineers. You are encouraged to use these rules in your own Liquibase Pro pipelines. If you need any help with these rules, please contact support@liquibase.com and our team will be happy to assist you. 

# 📂 Repository Structure
This repository is organized according to the database that the policy checks are compatible with. These are listed below.

| Database |
|----------|
| [All Databases](AnyDB)|
| [MongoDB](MongoDB) |
| [Oracle](Oracle) |
| [SQL Server](SQL&#32;Server) |
| [Snowflake](Snowflake) |


# 📂 Repository Structure
The repository is aligned by database type.

* `AnyDB` folder contains regex Policy Checks applicable for all database script. 
* `MongoDB` folder contains regex Policy Checks applicable for MongoDB scripts. 
* `Oracle` folder contains regex Policy Checks applicable for Oracle script. 
* `SQL Server` folder contains regex Policy Checks applicable for SQL Server script.
* `Snowflake` folder contains regex Policy Checks applicable for Snowflake scripts.

Each file is a description of the regex Policy Check and contains step-by-step procedure for adding the check.

Each regex Policy Check is documented as follows: 
- Naming convention is used as a short description
- Regular expression is provided near the top in each file
- Sample failing script is provide and where applicable a sample passing script is also provided
- Sample error message is provided
- Step-by-step commands for how to configure each regex Policy Check

# ☎️ Contact Liquibase
Liquibase sales: https://www.liquibase.com/contact-us<br>
Liquibase support: https://support.liquibase.com