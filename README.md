# Liquibase Pro Custom Quality Checks
This repository is a collection of Liquibase Pro Custom Quality checks. These checks have been created by the Liquibase community, including our customers and field engineers. You are encouraged to use these rules in your own Liquibase Pro pipelines. If you need any help with these rules, please contact support@liquibase.com and our team will be happy to assist you. 

[Liquibase Pro Quality Checks](https://www.liquibase.com/quality-checks) enable developers to write safe, compliant database code every time. You can enforce rules and best practices set by your DBAs, reducing security risks and costly manual errors. 

You can learn more about [Working with Quality Checks](https://docs.liquibase.com/commands/quality-checks/working-with-quality-checks.html) in our documentation.
The checks provided here are in addition to those shipped with Liquibase. 

We welcome any contributions from the community - just send us a pull request!

*Note: You must have a valid Liquibase Pro license to use Quality Checks*

# Repository Structure

This repository is organized according to the database that the quality checks are compatible with. These are listed below.

| Database |
|----------|
| [All Databases](AnyDB)|
| [MongoDB](MongoDB) |
| [Oracle](Oracle) |
| [SQL Server](SQL&#32;Server) |
| [Snowflake](Snowflake) |


# Repository Structure
The repository is aligned by database type.

* `AnyDB` folder contains custom Quality Checks applicable for all database script. 
* `MongoDB` folder contains custom Quality Checks applicable for MongoDB scripts. 
* `Oracle` folder contains custom Quality Checks applicable for Oracle script. 
* `SQL Server` folder contains custom Quality Checks applicable for SQL Server script.
* `Snowflake` folder contains custom Quality Checks applicable for Snowflake scripts.

Use the [Issues](https://github.com/liquibase/custom_qualitychecks/issues) link to request additional custom Quality Checks. Also provide sample failing scripts with each issue.

Each file is a description of the custom Quality Check and contains step-by-step procedure for adding the check.

Each custom Quality Check is documented as follows: 
- Naming convention is used as a short description
- Regular expression is provided near the top in each file
- Sample failing script is provide and where applicable a sample passing script is also provided
- Sample error message is provided
- Step-by-step commands for how to configure each custom Quality Check

# Useful Liquibase Checks Commands

## "checks show" command:
`liquibase checks show`

`liquibase checks show --checks-settings-file=<checks-settings-file>`

## "checks run" command:
`liquibase checks run` 

`liquibase checks run --checks-settings-file=<checks-settings-file>`

## "checks enable" command
`liquibase checks enable --check-name=<check-name>`

`liquibase checks enable --check-name=<check-name> --checks-settings-file=<checks-settings-file>`

## "checks disable" command
`liquibase checks disable --check-name=<check-name>`

`liquibase checks disable --check-name=<check-name> --checks-settings-file=<checks-settings-file>`

## "checks bulk-set --enable" command
`liquibase checks bulk-set --enable`

`liquibase checks bulk-set --enable --checks-settings-file=<checks-settings-file>`

## "checks bulk-set --disable" command
`liquibase checks bulk-set --disable` 

`liquibase checks bulk-set --disable --checks-settings-file=<checks-settings-file>`

## "checks customize" command
`liquibase checks customize --check-name=<check-name>`

`liquibase checks customize --check-name=<check-name> --checks-settings-file=<checks-settings-file>`
