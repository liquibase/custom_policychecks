# NoAddUpdateDeleteJob

Do not allow `sp_add_job`,`sp_update_job`, or `sp_delete_job` statements.

regex: `(?i)sp_(add|update|delete)_job`

# Sample Failing Scripts
``` sql
--changeset asmith:add_ad_hoc_job
EXECUTE dbo.sp_add_job
    @job_name = N'Ad hoc Sales Data Backup',
    @enabled = 1,
...	
```

# Sample Error Message
```
CHANGELOG CHECKS
----------------
Checks completed validation of the changelog and found the following issues:

Check Name:         Check for specific patterns in sql (NoAddUpdateDeleteJob)
Changeset ID:       create_ad_hoc_job
Changeset Filepath: changeLogs/logins/01_createAdHocJob.sql
Check Severity:     INFO (Return code: 0)
Message:            Error! No JOB statements allowed (eg. sp_add_job, sp_update_job, sp_delete_job).
```

# Step-by-Step
| Prompt | Command or User Input |
| ------ | ----------------------|
| > | `liquibase checks customize --check-name=SqlUserDefinedPatternCheck` |
| Give your check a short name for easier identification (up to 64 alpha-numeric characters only) [SqlUserDefinedPatternCheck1]: | `NoAddUpdateDeleteJob` |
| Set the Severity to return a code of 0-4 when triggered. (options: 'INFO'=0, 'MINOR'=1, 'MAJOR'=2, 'CRITICAL'=3, 'BLOCKER'=4)? [INFO]: | `<Choose a value: 0, 1, 2, 3, 4>` |
| Set 'SEARCH_STRING' (options: a string, or a valid regular expression): | `(?i)sp_(add\|update\|delete)_job` |
| Set 'MESSAGE' [A match for regular expression <SEARCH_STRING> was detected in Changeset <CHANGESET>.]: | `Error! No JOB statements allowed (eg. sp_add_job, sp_update_job, sp_delete_job).` |
| Set 'STRIP_COMMENTS' (options: true, false) [true]: | `true` |
