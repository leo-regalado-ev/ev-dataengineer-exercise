

class MigrateDal():
    """
    Handles database communications for table migration
    """

    def __init__(self, con):
        self.con = con
        self.scripts = Scripts()

    def migrate_tables(self):
        """
        Runs the scripts for creating tables on the PostgreSQL server
        """
        with self.con.cursor() as cur:
            # Migrate food_price_index table
            cur.execute(self.scripts.CREATE_FOOD_PRICE_INDEX_TABLE)


class Scripts():
    """
    Scripts to be used for database queries
    """

    CREATE_FOOD_PRICE_INDEX_TABLE = """
    CREATE TABLE IF NOT EXISTS food_price_index (
        id SERIAL PRIMARY KEY,
        series_reference VARCHAR(128) NOT NULL,
        period VARCHAR(20),
        data_value INTEGER,
        status VARCHAR(64) NOT NULL,
        units VARCHAR(64) NOT NULL,
        subject VARCHAR(255) NOT NULL,
        "group" VARCHAR(255) NOT NULL,
        series_title_1 VARCHAR(255) NOT NULL,
        created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
