# CreateTableMustHaveSystemKeyFile

Every `CREATE TABLE` statement must also have a `system_key_file` included.

regex: `(?is)(?=.*\b(create)\b)(?=.*\b(table)\b)(?!.*\b(system_key_file)\b).*`

# Sample Passing Script
``` sql
--changeset amalik:encryption_test
CREATE TABLE test.encryption_test (d int PRIMARY KEY) WITH COMPRESSION = {
      'class': 'EncryptingLZ4Compressor', 
      'cipher_algorithm' : 'DESede/CBC/PKCS5Padding', 
      'secret_key_strength' : 112,
      'system_key_file' : 'system_key' };
```
# Sample Failing Scripts
``` sql
--changeset amalik:encryption_test
CREATE TABLE test.encryption_test (d int PRIMARY KEY) WITH COMPRESSION = {
      'class': 'EncryptingLZ4Compressor', 
      'cipher_algorithm' : 'DESede/CBC/PKCS5Padding', 
      'secret_key_strength' : 112 };
```

# Sample Error Message
```
CHANGELOG CHECKS
----------------
Checks completed validation of the changelog and found the following issues:

Check Name:         Check for specific patterns in sql (CreateTableMustHaveSystemKeyFile)
Changeset ID:       encryption_test
Changeset Filepath: main/100_ddl/06_CassandraDDL.sql
Check Severity:     BLOCKER (Return code: 4)
Message:            Error! CREATE TABLE statement must have a TDE Encription enabled using "system_key_file".
```

# Step-by-Step
| Prompt | Command or User Input |
| ------ | ----------------------|
| > | `liquibase checks customize --check-name=SqlUserDefinedPatternCheck` |
| Give your check a short name for easier identification (up to 64 alpha-numeric characters only) [SqlUserDefinedPatternCheck1]: | `CreateTableMustHaveSystemKeyFile` |
| Set the Severity to return a code of 0-4 when triggered. (options: 'INFO'=0, 'MINOR'=1, 'MAJOR'=2, 'CRITICAL'=3, 'BLOCKER'=4)? [INFO]: | `<Choose a value: 0, 1, 2, 3, 4>` |
| Set 'SEARCH_STRING' (options: a string, or a valid regular expression): | `(?is)(?=.*\b(create)\b)(?=.*\b(table)\b)(?!.*\b(system_key_file)\b).*` |
| Set 'MESSAGE' [A match for regular expression <SEARCH_STRING> was detected in Changeset <CHANGESET>.]: | `Error! CREATE TABLE statement must have a TDE Encription enabled using "system_key_file".` |
| Set 'STRIP_COMMENTS' (options: true, false) [true]: | `true` |
