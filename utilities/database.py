import psycopg2


def get_database_connection():
    """
    Returns database connection as object
    """
    return psycopg2.connect(
        database="postgres",
        host="database-1.chz8io3pekiy.ap-southeast-2.rds.amazonaws.com",
        user="postgres",
        password="sEppet-feqcis-gozvi7",
        port=5432
    )

def insert_many_value(cur, data, key_num):
    """
    Returns insert VALUES clause given array of objects
    Based on findings here:\n
    https://stackoverflow.com/questions/8134602/psycopg2-insert-multiple-rows-with-one-query\n
    Params:
    cur - Database connection cursor\n
    data - List of data to mogrify\n
    key_num - Nunmber of %s to add
    """
    args_str = ""
    keys = ""
    
    for _ in range(key_num):
        keys += "%s,"
    
    if len(keys) > 0:
        keys = keys[:-1]
        args_str = ','.join(cur.mogrify(f"({keys})", x) for x in data)

    return args_str
