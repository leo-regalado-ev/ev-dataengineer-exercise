from psycopg2.extras import execute_values


class PeopleDal():
    """
    Handles database communications for table migration
    """

    def __init__(self, con):
        self.con = con
        self.scripts = Scripts()

    def migrate_data(self, data):
        """
        Insert data into corresponding database table\n
        Params:
        data - List of objects to insert
        """
        # TODO: Batch by 5000 entries
        with self.con.cursor() as cur:
            # Migrate food_price_index table
            execute_values(cur, self.scripts.INSERT_DATA, data, template=None, page_size=100)


class Scripts():
    """
    Scripts to be used for database queries
    """

    INSERT_DATA = """
    INSERT INTO table
    (
        series_reference,
        period,
        data_value,
        status,
        units,
        subject,
        "group",
        series_title_1
    )
    VALUES %s
    """
