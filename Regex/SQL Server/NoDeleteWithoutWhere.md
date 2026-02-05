# NoDeleteWithoutWhere

Every `DELETE` statement must also have a `WHERE` included.

regex: `(?is)(?=.*\b(delete)\b)(?!.*\b(restrict)\b)(?!.*\bno\s+action\b)(?!.*\bset\s+null\b)(?!.*\b(where)\b).*`

# Sample Passing Scripts
``` sql
--changeset amalik:delete
DELETE FROM dbo.Table01 WHERE ID='1';
```
``` sql
--changeset mikeo:delete-restrict
ALTER TABLE rental ADD CONSTRAINT rental_customer_id_fkey FOREIGN KEY (customer_id) REFERENCES customer (customer_id) ON UPDATE CASCADE ON DELETE RESTRICT;
```
``` sql
--changeset mikeo:delete-noaction
ALTER TABLE address ADD CONSTRAINT fk_address_city FOREIGN KEY (city_id) REFERENCES city (city_id) ON UPDATE NO ACTION ON DELETE NO ACTION;
```
``` sql
--changeset mikeo:delete-setnull
ALTER TABLE payment ADD CONSTRAINT payment_rental_id_fkey FOREIGN KEY (rental_id) REFERENCES rental (rental_id) ON UPDATE CASCADE ON DELETE SET NULL
```
# Sample Failing Scripts
``` sql
--changeset amalik:delete
DELETE FROM dbo.Table01;
```

# Sample Error Message
```
CHANGELOG CHECKS
----------------
Checks completed validation of the changelog and found the following issues:

Check Name:         Check for specific patterns in sql (NoDeleteWithoutWhere)
Changeset ID:       delete
Changeset Filepath: main/QCs/delete_from_table.sql
Check Severity:     BLOCKER (Return code: 4)
Message:            Error! All DELETE statements must have a WHERE clause.

```

# Step-by-Step
| Prompt | Command or User Input |
| ------ | ----------------------|
| > | `liquibase checks customize --check-name=SqlUserDefinedPatternCheck` |
| Give your check a short name for easier identification (up to 64 alpha-numeric characters only) [SqlUserDefinedPatternCheck1]: | `NoDeleteWithoutWhere` |
| Set the Severity to return a code of 0-4 when triggered. (options: 'INFO'=0, 'MINOR'=1, 'MAJOR'=2, 'CRITICAL'=3, 'BLOCKER'=4)? [INFO]: | `<Choose a value: 0, 1, 2, 3, 4>` |
| Set 'SEARCH_STRING' (options: a string, or a valid regular expression): | `(?is)(?=.*\b(delete)\b)(?!.*\b(restrict)\b)(?!.*\bno\s+action\b)(?!.*\bset\s+null\b)(?!.*\b(where)\b).*` |
| Set 'MESSAGE' [A match for regular expression <SEARCH_STRING> was detected in Changeset <CHANGESET>.]: | `Error! All DELETE statements must have a WHERE clause.` |
| Set 'STRIP_COMMENTS' (options: true, false) [true]: | `true` |
