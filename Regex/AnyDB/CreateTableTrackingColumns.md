# CreateTableTrackingColumns

Check that if a CREATE TABLE statement is found, the following Tracking Columns must be present:
SYSID, STT, UPD_TME, UPD_OPEID, INS_TME, and INS_OPEID

# Sample Passing Changesets
``` sql
--changeset ASmith:table01
CREATE TABLE TEST_TABLE_01
(
  SYSID                 NUMBER(10),
  STT                   NUMBER(10),
  COL1                  VARCHAR2(6 BYTE),
  COL2                  VARCHAR2(4 BYTE),
  UPD_TME               DATE,
  UPD_OPEID             NUMBER(10),
  INS_TME               DATE,
  INS_OPEID             NUMBER(10)
);
```

# Sample Failing Changeset
``` sql
--changeset ASmith:table01_missing_columns
CREATE TABLE TEST_TABLE_01
(
  SYSID                 NUMBER(10),
  STT                   NUMBER(10),
  COL1                  VARCHAR2(6 BYTE),
  COL2                  VARCHAR2(4 BYTE)
);
```

# Sample Error Message
```
DATABASE CHECKS
----------------
Checks completed validation of the changelog and found the following issues:

Check Name:         Pattern a not followed by pattern b (CreateTableTrackingColumns)
Changeset ID:       table01_missing_columns
Changeset Filepath: oracle/releases/v2025.X/script-1.0.0.sql
Check Severity:     MAJOR (Return code: 2)
Message:            CREATE TABLE statements must have tracking columns SYSID, STT, UPD_TME, UPD_OPEID, INS_TME, and INS_OPEID
```
# Step-by-Step

| Prompt | Command or User Input |
| ------ | ----------------------|
| > | `liquibase checks copy --check-name=PatternANotFollowedByPatternB` |
| Give your check a short name for easier identification (up to 64 alpha-numeric characters only) [UserDefinedContextCheck1]: | `CreateTableTrackingColumns` |
| Set the Severity to return a code of 0-4 when triggered. (options: 'INFO'=0, 'MINOR'=1, 'MAJOR'=2, 'CRITICAL'=3, 'BLOCKER'=4)? [INFO]: | `<Choose a value: 0, 1, 2, 3, 4>` |
| Set 'PATTERN_A' (options: a string, or a valid regular expression): | `(?i)create\s*table` |
| Set 'PATTERN_B' (options: a string, or a valid regular expression): | `(?i)(?=.*\bSYSID\b)(?=.*\bSTT\b)(?=.*\bUPD_TME\b)(?=.*\bUPD_OPEID\b)(?=.*\bINS_TME\b)(?=.*\bINS_OPEID\b).*` |
| Set 'CASE_SENSITIVE' (options: true, false) [true]: | false
| Set 'MESSAGE' [Match found: '<PATTERN_A>' is NOT followed by '<PATTERN_B>' in Changeset '<CHANGESET>'.]: | `CREATE TABLE statements must have tracking columns SYSID, STT, UPD_TME, UPD_OPEID, INS_TME, and INS_OPEID`
