import sqlite3


class DBHandler:

    """
        Provides connection to SQLite3 database called 'resturant_database.db
        if not found, creates one.

        Meant to be used as a context manager

        database: location of the sqlite3 database

        e.g:
            >>> with DBHandler() as cursor:
            ...     cursor.execute(SQL statement)

        returns a `cursor` object.
        """

    def __init__(self, database):
        self.db = database

    def __enter__(self):
        self.conn = sqlite3.connect(self.db)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_value, exc_tb):
        # Add transaction to the databas and close connection
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
