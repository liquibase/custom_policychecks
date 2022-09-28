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
| [Oracle](Oracle) |
| [SQL Server](SQL&#32;Server) |


# Usefule Liquibase Checks Commands

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
