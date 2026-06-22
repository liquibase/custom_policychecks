# NoGrantExceptGrantExecute

Only `GRANT EXECUTE` allowed. No other GRANT statements allowed.

regex: `(?i)\bgrant\b(?![^;]*\bexecute\b)`

> **Note:** An earlier version of this check used the pattern
> `(?is)(?=.*\b(grant)\b)(?!.*\b(execute)\b).*`.
> That pattern has two issues:
>
> 1. **Performance** — The `(?=.*\b…\b)` positive lookahead causes
>    [catastrophic backtracking](https://www.regular-expressions.info/catastrophic.html)
>    in Java's regex engine. On large changesets (thousands of rows)
>    it can take hours or crash the JVM.
> 2. **Correctness** — The `(?s)` (DOTALL) flag and `.*` lookaheads scan the
>    *entire changeset* content, not individual SQL statements. If a changeset
>    contains `GRANT SELECT … TO user;` alongside a separate
>    `GRANT EXECUTE … TO user;`, the `EXECUTE` in the second statement
>    satisfies the negative lookahead and the bare GRANT goes unflagged.
>
> The updated pattern anchors on the `GRANT` keyword and scopes the
> lookahead to the current SQL statement (up to the next `;`), fixing both
> issues.

# Sample Passing Scripts
``` sql
--changeset amalik:grant_execute
GRANT EXECUTE ON dbo::CustOrderHist TO appUser;
```

# Sample Failing Scripts
``` sql
--changeset amalik:grant_control
GRANT CONTROL ON dbo::CustOrderHist TO appUser;

--changeset amalik:grant_showplan
GRANT SHOWPLAN ON dbo::CustOrderHist TO appUser;

--changeset amalik:grant_createview
GRANT CREATE VIEW ON dbo::CustOrderHist TO appUser;
```
``` sql
--changeset amalik:grant_multi_statement
-- Bare GRANT SELECT is flagged even though GRANT EXECUTE appears in a different statement
GRANT SELECT ON dbo::CustOrderHist TO appUser;
GRANT EXECUTE ON dbo::CustOrderHist TO appUser;
```

# Sample Error Message
```
CHANGELOG CHECKS
----------------
Checks completed validation of the changelog and found the following issues:

Check Name:         Check for specific patterns in sql (NoGrantExceptGrantExecute)
Changeset ID:       grant_control
Changeset Filepath: changeLogs/2_objects/02_storedprocedure/grantcontrol.sql
Check Severity:     BLOCKER (Return code: 4)
Message:            Error! No GRANT statements allowed except GRANT EXECUTE.
```

# Step-by-Step
| Prompt | Command or User Input |
| ------ | ----------------------|
| > | `liquibase checks customize --check-name=SqlUserDefinedPatternCheck` |
| Give your check a short name for easier identification (up to 64 alpha-numeric characters only) [SqlUserDefinedPatternCheck1]: | `NoGrantExceptGrantExecute` |
| Set the Severity to return a code of 0-4 when triggered. (options: 'INFO'=0, 'MINOR'=1, 'MAJOR'=2, 'CRITICAL'=3, 'BLOCKER'=4)? [INFO]: | `<Choose a value: 0, 1, 2, 3, 4>` |
| Set 'SEARCH_STRING' (options: a string, or a valid regular expression): | `(?i)\bgrant\b(?![^;]*\bexecute\b)` |
| Set 'MESSAGE' [A match for regular expression <SEARCH_STRING> was detected in Changeset <CHANGESET>.]: | `Error! No GRANT statements allowed except GRANT EXECUTE.` |
| Set 'STRIP_COMMENTS' (options: true, false) [true]: | `true` |
