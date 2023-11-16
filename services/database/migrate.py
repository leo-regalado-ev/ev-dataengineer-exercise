import json
from dal.migrate_dal import MigrateDal
from utilities.database import get_database_connection


def handler(event, context):
    """
    Handles migration of tables to use to new PostgreSQL server
    """
    con = get_database_connection()

    migrate_dal = MigrateDal(con)

    # Run DB migration of tables
    try:
        migrate_dal.migrate_tables()

        # Commit changes
        con.commit()

        body = {
            "message": "Migration successful!",
            "input": event
        }
    except Exception as e:
        print(str(e))
        body = {
            "message": "Migration failed!",
            "error": str(e),
            "input": event
        }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    con.close()

    return response

# Uncomment to test locally
# print(handler({}, None))
