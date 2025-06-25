<p align="left">
  <img src="../img/liquibase.png" alt="Liquibase Logo" title="Liquibase Logo" width="324" height="72">
</p>

# 🔒 Liquibase Pro Python Policy Checks
This repository is a collection of Liquibase Pro Python Policy checks. These checks have been created by the Liquibase community, including our customers and field engineers. You are encouraged to use these rules in your own Liquibase Pro pipelines.

If you need any help with these rules, please contact support@liquibase.com and our team will be happy to assist you (Pro customers only).

| Database |
|----------|
| [All Databases](Any/README.md)|
| [DB2zOS](Db2zos/README.md) |
| [DynamoDB](DynamoDB/README.md) |
| [FormattedSQL](FormattedSQL/README.md) |
| [MongoDB](MongoDB/README.md) |
| [MySQL](MySQL/README.md) |
| [Oracle](Oracle/README.md) |
| [PostgreSQL](PostgreSQL/README.md) |

# 💡 Useful Links
| Description | Source |
|-------------|--------|
| Documentation| [Liquibase](https://docs.liquibase.com/liquibase-pro/policy-checks/custom-policy-checks/home.html)
| Python code reference | [W3Schools.com](https://www.w3schools.com/python/default.asp)
| SQL parse module reference | [ReadTheDocs.io](https://sqlparse.readthedocs.io/en/latest/)
| GraalPy (optional, required for custom virtual environments) | [GitHub.com](https://github.com/oracle/graalpython/releases)
| GraalPy reference | [Medium.com](https://medium.com/graalvm/graalpy-quick-reference-0488b661a57c)
| venv reference | [Python.org](https://docs.python.org/3/library/venv.html)

# ✔️ Pre-Execution Steps
1. Java 17 or higher is required. 
1. Download the latest version of [Liquibase](https://www.liquibase.com/download). Beginning with version 4.31.0, the policy check jar is included. Older versions require the latest [checks jar](https://repo1.maven.org/maven2/org/liquibase/ext/liquibase-checks/) to be placed inside the liquibase/lib folder.
1. Ensure this environment variable or setting is set to enable custom policy checks.<br>
    *Environment variable*
    ```
    LIQUIBASE_COMMAND_CHECKS_RUN_CHECKS_SCRIPTS_ENABLED='true'
    ```
    *liquibase.properties*
    ```
    checks-scripts-enabled=true
    ```

# 📒 Notes
1. To aid in debugging, it's useful to disable all other policy checks.
    ```
    liquibase checks bulk-set --disable
    ```
1. Sample relational and NoSQL changelogs are available in the [Changesets](Changesets/) folder.
1. Scripts are called once for each changeset (changelog scope) or once for each database object (database scope). Changesets may contain multiple SQL statements.
1. The print() function can be used to display debugging messages (instead of just liquibase_logger). This works regardless of log_level. Additionally, f strings automatically convert variables for printing and remove the need for concatenation to build a string of static and dynamic text.
    ```
    my_int = 123
    my_str = "Hello World!"
    print(f"{my_str} My variable is: {my_int}")
    ```
    f strings can also be used wherever strings are expected.
    ```
    my_int = 123
    liquibase_status.message = f"My variable is: {my_int}"
    ```
1. The latest [Liquibase provided modules](https://docs.liquibase.com/liquibase-pro/policy-checks/custom-policy-checks/api-helper-scripts.html) can be imported into your checks to access Liquibase provided functions.
    ```
    import liquibase_utilities
    import liquibase_changesets

    print(liquibase_changesets.get_labels(liquibase_utilities.get_changeset()))
    ```
1. LoadData change types are not currently supported. 
1. Having the commercial Mongo extension in the lib directory will cause some relational change types to behave incorrectly (e.g., createIndex). 
1. Environment variables can be accessed using the os module.
    ```
    import os

    print(os.environ.get("LIQUIBASE_COMMAND_URL"))
    ```

# 🔎 Specific Examples
1. Error messages can be customized by adding a string to be replaced when defining the custom policy check. See [TableNamesMustBeUppercase](Scripts/table_names_uppercase.py).
1. Arguments defined at check creation/modification can be passed in to scripts. See [TableRowCount](Scripts/count_rows.py).
1. Values can be saved/retrieved between check runs using a cache. See [CreateIndexCount](Scripts/create_index_count.py).
1. Most of the provided changelog checks use string parsing to process SQL and support only simple statements. The [sqlparse](https://pypi.org/project/sqlparse/) module can be used for more complex statements. See [NoDeleteWithoutWhere](Scripts/delete_without_where.py) and [TimestampColumnName](Scripts/timestamp_column_name.py).
1. SQL can be executed as part of a custom policy check. See [TableRowCount](Scripts/count_rows.py).
1. Test for required [Liquibase metadata](https://docs.liquibase.com/concepts/changelogs/sql-format.html). See [TestFormattedSQL](Scripts/test_formatted_sql.py).

# 🐍 Local Python Environment
⚠️ *Not required to use or develop custom policy checks*

Instead of the built-in Python virtual environment Liquibase provides, a custom one can be utilized. This is useful if there are additional Python modules you want to import into your custom policy checks. To create one, follow these steps:
1. Download and extract GraalPy.
1. Add \<install dir\>/bin (or \<install dir\>\bin for Windows) to your path.
1. Create a Python virtual environment and directory structure. Once created the environment can be moved to a different folder (provided the Liquibase environment variable is also updated).

    ⚠️ *Use GitBash for Windows to execute commands*

    ```
    graalpy -m venv <virtual env path>
    ```
1. Activate the environment to install modules to the local virtual environment.<br>
    *Linux*
    ```
    source <virtual env path>/bin/activate
    ```
    *Windows*
    ```
    source <virtual env path>/Scripts/activate
    ```
1. Install Python modules in the new environment.

    ⚠️ *Sqlparse is required*
    ```
    graalpy -m pip install sqlparse
    ```
1. Deactive the environment (exit or run bin/deactivate). Deactivate on Windows may throw an error (safe to close the GitBash window).
1. Configure Liquibase to point to the new virtual environment.<br>
    *Linux*
    ```
    LIQUIBASE_SCRIPT_PYTHON_EXECUTABLE_PATH="<virtual env path>/bin/python"
    ```
    *Windows*
     ```
    LIQUIBASE_SCRIPT_PYTHON_EXECUTABLE_PATH='<virtual env path>\Scripts\python.exe'
    ```
1. Run checks as normal. To revert back to the built-in environment, unset the environment variable.

# ☎️ Contact Liquibase
Liquibase sales: https://www.liquibase.com/contact-us<br>
Liquibase support (Pro customers only): https://support.liquibase.com
