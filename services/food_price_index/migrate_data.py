import json
import csv
import traceback
from dal.food_price_index_dal import FoodPriceIndexDal
from utilities.database import get_database_connection
from utilities.s3_helper import S3Helper
from utilities.execution_time_logger import ExecutionTimeLogger


def handler(event, context):
    """
    Handles migration of tables to use to new PostgreSQL server
    """
    # Initialize connection to database
    con = get_database_connection()
    response = {}
    try:
        s3_key = event.get("s3_key", "food-price-index-september-2023-seasonally-adjusted.csv")

        # Create logger for logging execution time
        exec_time_logger = ExecutionTimeLogger()

        migrate_dal = FoodPriceIndexDal(con)

        # Load data for S3 file
        s3_helper = S3Helper()
        csv_data = s3_helper.get_csv(s3_key)
        csv_data_list = []

        csv_data_rows = csv_data.splitlines()

        exec_time_logger.log_current_time("Extracting CSV data from S3 to memory")

        lines = csv.reader(csv_data_rows, delimiter=",")
        first_row = True
        for row in lines:
            # Skip header row
            if first_row:
                first_row = False
                continue

            if len(row) != 8:
                continue

            # Append row data as tuple, with correct order to use in query
            csv_data_list.append((
                row[0],
                row[1],
                row[2] if len(str(row[2])) > 0 else None,
                row[3],
                row[4],
                row[5],
                row[6],
                row[7]
            ))

        exec_time_logger.log_current_time("Transforming CSV rows to dictionary")

        # Run DB migration of tables
        if len(csv_data_list) > 0:
            migrate_dal.migrate_data(csv_data_list)
            con.commit()

            exec_time_logger.log_current_time(
                f"Loading data to database server with {len(csv_data_list)} rows"
            )
        else:
            print("No data to migrate")

        body = {
            "message": "Migration successful",
            "input": event
        }

        response = {
            "statusCode": 200,
            "body": json.dumps(body)
        }
    except Exception as e:
        print(traceback.format_exc())
        print(str(e))
    finally:
        con.close()

    return response
