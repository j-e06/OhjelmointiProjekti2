import mariadb

# Database Context Manager
class Database:
    def __init__(self, **config):
        self.config = config
        self.connection = None

    def __enter__(self):
        try:
            self.connection = mariadb.connect(**self.config)
            self.cursor = self.connection.cursor(dictionary=True)  # Use dictionary cursor if needed
            return self.cursor  # Return the cursor for usage in the 'with' block
        except mariadb.Error as exception:
            raise Exception(f"Error connecting to MariaDB: {exception}")

    def __exit__(self, exc_type, exc_value, traceback):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()


def execute_query(cursor: mariadb.Cursor, query, params=None, fetch=True):
    """
    Executes a SQL query with optional parameters and fetches results if required.

    Args:
        cursor (mariadb.Cursor): The database cursor.
        query (str): SQL query to execute.
        params (tuple): Optional parameters for the query.
        fetch (bool): Whether to fetch results (default: True).

    Returns:
        list: Query results if fetch is True.
        None: If fetch is False.
    """
    try:
        cursor.execute(query, params)
        if fetch:
            return cursor.fetchall()
        else:
            cursor.connection.commit()
            return None
    except Exception as e:
        raise Exception(f"Database error: {e}")
