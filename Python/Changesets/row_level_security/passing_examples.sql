-- Row-Level Security: Passing Examples
-- These changesets demonstrate VALID operations that pass the row-level security checks

-- Changeset 1: Valid INSERT with team column
--changeset risk_team:1
INSERT INTO FRAMEWORK_CONFIG (job_name, SOURCE, enabled, created_date)
VALUES ('risk_daily_calc', 'RISK', 1, CURRENT_DATE);
--rollback DELETE FROM FRAMEWORK_CONFIG WHERE job_name = 'risk_daily_calc' AND SOURCE = 'RISK';

-- Changeset 2: Valid UPDATE with team filtering
--changeset risk_team:2
UPDATE FRAMEWORK_CONFIG
SET enabled = 1,
    last_modified = CURRENT_TIMESTAMP
WHERE job_name = 'risk_daily_calc'
  AND SOURCE = 'RISK';
--rollback UPDATE FRAMEWORK_CONFIG SET enabled = 0 WHERE job_name = 'risk_daily_calc' AND SOURCE = 'RISK';

-- Changeset 3: Valid DELETE with team filtering
--changeset risk_team:3
DELETE FROM JOB_DEFINITIONS
WHERE status = 'OBSOLETE'
  AND SOURCE = 'RISK';
--rollback -- Cannot rollback delete

-- Changeset 4: Multiple valid INSERTs
--changeset risk_team:4
INSERT INTO FRAMEWORK_CONFIG (job_name, SOURCE, enabled)
VALUES ('risk_job_1', 'RISK', 1);

INSERT INTO FRAMEWORK_CONFIG (job_name, SOURCE, enabled)
VALUES ('risk_job_2', 'RISK', 1);

INSERT INTO FRAMEWORK_CONFIG (job_name, SOURCE, enabled)
VALUES ('risk_job_3', 'RISK', 0);
--rollback DELETE FROM FRAMEWORK_CONFIG WHERE job_name IN ('risk_job_1', 'risk_job_2', 'risk_job_3') AND SOURCE = 'RISK';

-- Changeset 5: Valid UPDATE with complex conditions
--changeset risk_team:5
UPDATE FRAMEWORK_CONFIG
SET enabled = 0
WHERE SOURCE = 'RISK'
  AND job_name LIKE 'risk_%'
  AND created_date < DATE_SUB(CURRENT_DATE, INTERVAL 90 DAY);
--rollback -- Conditional rollback not shown

-- Changeset 6: Valid INSERT with all columns
--changeset risk_team:6
INSERT INTO SHARED_PARAMETERS (
    param_id,
    param_name,
    SOURCE,
    param_value,
    param_type,
    created_by,
    created_date
)
VALUES (
    1001,
    'max_threads',
    'RISK',
    '10',
    'INTEGER',
    'risk_admin',
    CURRENT_DATE
);
--rollback DELETE FROM SHARED_PARAMETERS WHERE param_id = 1001 AND SOURCE = 'RISK';

-- Changeset 7: Operations on non-protected tables (always pass)
--changeset risk_team:7
-- These operations don't require team filtering because the table isn't protected
INSERT INTO USER_PREFERENCES (user_id, preference_key, preference_value)
VALUES (123, 'theme', 'dark');

UPDATE USER_PREFERENCES
SET preference_value = 'light'
WHERE user_id = 123;

DELETE FROM TEMP_PROCESSING_DATA
WHERE processed_date < DATE_SUB(CURRENT_DATE, INTERVAL 7 DAY);
--rollback -- Not applicable
