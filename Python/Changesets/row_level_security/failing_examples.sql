-- Row-Level Security: Failing Examples
-- These changesets demonstrate INVALID operations that violate row-level security

-- IMPORTANT: These examples will FAIL the policy check and block deployment
-- They are provided for educational purposes to show what NOT to do

-- Changeset 1: INSERT missing team column (VIOLATION)
--changeset risk_team:fail_1
-- VIOLATION: SOURCE column is missing
INSERT INTO FRAMEWORK_CONFIG (job_name, enabled)
VALUES ('some_job', 1);
--rollback DELETE FROM FRAMEWORK_CONFIG WHERE job_name = 'some_job';

-- Changeset 2: INSERT with wrong team value (VIOLATION)
--changeset risk_team:fail_2
-- VIOLATION: SOURCE = 'TRADING' but environment variable TEAM_ID = 'RISK'
INSERT INTO FRAMEWORK_CONFIG (job_name, SOURCE, enabled)
VALUES ('trading_job', 'TRADING', 1);
--rollback DELETE FROM FRAMEWORK_CONFIG WHERE job_name = 'trading_job';

-- Changeset 3: UPDATE without team filtering (VIOLATION)
--changeset risk_team:fail_3
-- VIOLATION: WHERE clause doesn't include SOURCE = 'RISK'
UPDATE FRAMEWORK_CONFIG
SET enabled = 0
WHERE job_name = 'some_job';
--rollback UPDATE FRAMEWORK_CONFIG SET enabled = 1 WHERE job_name = 'some_job';

-- Changeset 4: UPDATE without WHERE clause (VIOLATION)
--changeset risk_team:fail_4
-- VIOLATION: No WHERE clause at all - would affect all rows!
UPDATE FRAMEWORK_CONFIG
SET last_checked = CURRENT_TIMESTAMP;
--rollback -- Cannot safely rollback

-- Changeset 5: DELETE without team filtering (VIOLATION)
--changeset risk_team:fail_5
-- VIOLATION: WHERE clause doesn't include SOURCE = 'RISK'
DELETE FROM JOB_DEFINITIONS
WHERE status = 'OBSOLETE';
--rollback -- Cannot rollback

-- Changeset 6: DELETE without WHERE clause (VIOLATION)
--changeset risk_team:fail_6
-- VIOLATION: No WHERE clause - would delete all rows!
DELETE FROM FRAMEWORK_CONFIG;
--rollback -- Cannot rollback

-- Changeset 7: INSERT with NULL team value (VIOLATION)
--changeset risk_team:fail_7
-- VIOLATION: SOURCE is NULL instead of 'RISK'
INSERT INTO JOB_DEFINITIONS (job_id, SOURCE, job_name)
VALUES (999, NULL, 'some_job');
--rollback DELETE FROM JOB_DEFINITIONS WHERE job_id = 999;

-- Changeset 8: INSERT with empty team value (VIOLATION)
--changeset risk_team:fail_8
-- VIOLATION: SOURCE is empty string instead of 'RISK'
INSERT INTO SHARED_PARAMETERS (param_id, SOURCE, param_name)
VALUES (1002, '', 'some_param');
--rollback DELETE FROM SHARED_PARAMETERS WHERE param_id = 1002;

-- Changeset 9: UPDATE with wrong team in WHERE (VIOLATION)
--changeset risk_team:fail_9
-- VIOLATION: SOURCE = 'IOT' but environment variable TEAM_ID = 'RISK'
UPDATE FRAMEWORK_CONFIG
SET enabled = 1
WHERE job_name = 'iot_job'
  AND SOURCE = 'IOT';
--rollback UPDATE FRAMEWORK_CONFIG SET enabled = 0 WHERE job_name = 'iot_job' AND SOURCE = 'IOT';

-- Changeset 10: UPDATE with OR condition (VIOLATION)
--changeset risk_team:fail_10
-- VIOLATION: OR condition could bypass team filtering
-- This would allow updating records that don't belong to RISK team
UPDATE FRAMEWORK_CONFIG
SET enabled = 0
WHERE job_name = 'specific_job'
   OR SOURCE = 'RISK';
--rollback UPDATE FRAMEWORK_CONFIG SET enabled = 1 WHERE job_name = 'specific_job' OR SOURCE = 'RISK';
