# Step-by-step

On CLI, type this command:

`> liquibase checks customize --check-name=SqlUserDefinedPatternCheck`


```
Give your check a short name for easier identification (up to 64 alpha-numeric characters only) [SqlUserDefinedPatternCheck1]: 
```
`NoSelectStar`


```
Set the Severity to return a code of 0-4 when triggered. (options: 'INFO'|0, 'MINOR'|1, 'MAJOR'|2, 'CRITICAL'|3, 'BLOCKER'|4)? [INFO]: 
```
`<Choose a value: 0, 1, 2, 3, 4>`

### Prompt
```
Set 'SEARCH_STRING' (options: a string, or a valid regular expression):
```
`(?i:select \*)`

### Prompt
```
Set 'MESSAGE' [A match for regular expression <SEARCH_STRING> was detected in Changeset <CHANGESET>.]:
```
`Error! SELECT * not allowed.`

### Prompt
```
Set 'STRIP_COMMENTS' (options: true, false) [true]:
```
`true`
