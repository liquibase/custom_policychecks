# CreateObjectCheck

Create Object should be either Create Or Replace Object or Create Object If Not Exists

regex: `(?is)(?=.*\b(create\s*(table|procedure|function|view))\b)(?!.*\b(if\s*not\s*exists)\b).*`

# Sample Passing Scripts
``` --liquibase formatted sql
--changeset AmySmith:table_01 labels:JIRA-1234
CREATE OR REPLACE TABLE SALES (
	id numeric not null,
	name varchar (255), 
	toggle boolean default True, 
	date date default null 
);

--changeset AmySmith:function_01 endDelimiter:\*\*
create function if not exists function_01 (i int)
RETURNS INT
LANGUAGE PYTHON
RUNTIME_VERSION = '3.8'
HANDLER = 'addone_py'
as
$$
def addone_py(i):
  return i+1
$$;
```

# Sample Failing Scripts
``` --liquibase formatted sql
--changeset AmySmith:proc_01 endDelimiter:\*\*
 create procedure sp_pi_check ()
    returns float not null
    language javascript
    as
    $$
    return 3.1415926;
    $$
    ;
```

# Sample Error Message
``` 
CHANGELOG CHECKS
----------------
Checks completed validation of the changelog and found the following issues:

Check Name:         Check for specific patterns in sql (CreateObjectCheck)
Changeset ID:       customers_table
Changeset Filepath: scripts/releases/1.0/customers_data_load_01.sql
Check Severity:     MINOR (Return code: 1)
Message:            Create Object should be either Create Or Replace Object or
                    Create Object If Not Exists
```

# Step-by-Step
```
Command: liquibase checks copy --check-name=SqlUserDefinedPatternCheck
Short Name: CreateObjectCheck
Severity: <Choose a value: 0, 1, 2, 3, 4>
Search String: (?is)(?=.*\b(create\s*(table|procedure|function|view))\b)(?!.*\b(if\s*not\s*exists)\b).*
Message: Create Object should be either Create Or Replace Object or Create Object If Not Exists
Strip Comments: true
```