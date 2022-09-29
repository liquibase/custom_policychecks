Note: You must have a valid Liquibase Pro license to use Quality Checks
# Custom Quality Checks

Quality Checks provided here are in addition to Quality Checks shipped with Liquibase. 

These quality checks are designed using regular expressions.

# Repository Structure
The repository is aligned by database type.

* `AnyDB` folder contains custom Quality Checks applicable for all database script. 
* `Oracle` folder contains custom Quality Checks applicable for Oracle script. 
* `SQL Server` folder contains custom Quality Checks applicable for SQL Server script.

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
