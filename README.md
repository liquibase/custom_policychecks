<p align="left">
  <img src="img/liquibase.png" alt="Liquibase Logo" title="Liquibase Logo" width="324" height="72">
</p>

# 🔒 Liquibase Pro Policy Checks
This repository contains example [Regex](Regex/) and [Python](Python/) Policy Checks.

[Liquibase Pro Policy Checks](https://www.liquibase.com/policy-checks) enable developers to write safe, compliant database code every time. You can enforce rules and best practices set by your DBAs, reducing security risks and costly manual errors. 

You can learn more about [Working with Policy Checks](https://docs.liquibase.com/liquibase-pro/policy-checks/workflows/home.html) in our documentation. The checks provided here are in addition to those shipped with Liquibase. 

We welcome any contributions from the community - just send us a pull request!

*Note: You must have a valid Liquibase Pro license to use Policy Checks*

# 💡 Useful Checks Commands

## "[checks show](https://docs.liquibase.com/commands/policy-checks/subcommands/show.html)"
`liquibase checks show`

`liquibase checks show --checks-settings-file=<checks-settings-file>`

## "[checks run](https://docs.liquibase.com/commands/policy-checks/subcommands/run.html)"
`liquibase checks run` 

`liquibase checks run --checks-settings-file=<checks-settings-file>`

## "[checks enable](https://docs.liquibase.com/commands/policy-checks/subcommands/enable.html)"
`liquibase checks enable --check-name=<check-name>`

`liquibase checks enable --check-name=<check-name> --checks-settings-file=<checks-settings-file>`

## "[checks disable](https://docs.liquibase.com/commands/policy-checks/subcommands/disable.html)"
`liquibase checks disable --check-name=<check-name>`

`liquibase checks disable --check-name=<check-name> --checks-settings-file=<checks-settings-file>`

## "[checks bulk-set --enable](https://docs.liquibase.com/commands/policy-checks/subcommands/bulk-set.html)"
`liquibase checks bulk-set --enable`

`liquibase checks bulk-set --enable --checks-settings-file=<checks-settings-file>`

## "[checks bulk-set --disable](https://docs.liquibase.com/commands/policy-checks/subcommands/bulk-set.html)"
`liquibase checks bulk-set --disable` 

`liquibase checks bulk-set --disable --checks-settings-file=<checks-settings-file>`

## "[checks customize](https://docs.liquibase.com/commands/policy-checks/subcommands/customize.html)"
`liquibase checks customize --check-name=<check-name>`

`liquibase checks customize --check-name=<check-name> --checks-settings-file=<checks-settings-file>`

# ☎️ Contact Liquibase
Liquibase sales: https://www.liquibase.com/contact-us<br>
Liquibase support: https://support.liquibase.com