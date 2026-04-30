# Example policy check that uses query_for_list to enforce that all tables                                                                                                                                                                   
 # in the target database have at least one row with a comment in a
 # TABLE_COMMENTS metadata table. This demonstrates how to run arbitrary SQL
 # against the target database from within a custom policy check.
 #
 # Usage: configure as a CustomCheck (changelog or database scope) and point
 # the script path to this file.

    # % liquibase checks customize --check-name=CustomCheckTemplate
    # Short name:  		InvalidCompiles
    # Severity: 			0-4
    # Script description: List all objects
    # Script scope: 		changelog
    # Script message: 	This check will never trigger. This is a first custom policy check.
    # Script type: 		python
    # Script path: 		Scripts/invalid_objects.py
    # Script_Args: 		<empty>
    # Requires snapshot: 	false
    # % liquibase checks show --check-status=enabled
    # % liquibase checks run --checks-scope=database

import sys
import liquibase_utilities

logger = liquibase_utilities.get_logger()
status = liquibase_utilities.get_status()

CACHE_KEY = "invalid_objects_result"
invalid_objects_in_cache = liquibase_utilities.get_cache(CACHE_KEY, None)

if invalid_objects_in_cache is None:
    # First invocation — run the query once and cache the results
    sql = """
        SELECT object_type, object_name, status, created
        FROM user_objects
        WHERE status = 'INVALID'
        ORDER BY object_type, object_name
    """
    invalid_objects = liquibase_utilities.query_for_list(sql, None, None)
    liquibase_utilities.put_cache(CACHE_KEY, invalid_objects)

if invalid_objects is not None and invalid_objects.size() > 0:
    # Only fire for the current database object if it's in the invalid list
    database_object = liquibase_utilities.get_database_object()
    current_name = database_object.getName()
    for row in invalid_objects:
        if str(row.get("OBJECT_NAME")) == current_name:
            status.fired = True
            status.message = ( str(row.get("OBJECT_TYPE")) + " '" + current_name + "' has INVALID status" )
            sys.exit(1)

False