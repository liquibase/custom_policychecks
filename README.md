Note: You must have a valid Liquibase Pro license to use Quality Checks
# Custom Quality Checks

Quality Checks provided here are in addition to Quality Checks shipped with Liquibase. 

These quality checks are designed using regular expressions.

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
