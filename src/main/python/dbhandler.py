import sqlite3
import os


class DBHandler:

    """
        Provides connection to SQLite3 database called 'resturant_database.db
        if not found, creates one.

        Meant to be used as a context manager

        e.g:
            >>> with DBHandler() as cursor:
            ...     cursor.execute(SQL statement)

        returns a `cursor` object.
        """

    def __enter__(self):
        self.conn = sqlite3.connect(os.path.relpath('resturant_database.db'))
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_value, exc_tb):
        # Add transaction to the databas and close connection
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
