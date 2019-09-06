import sqlite3
import os

class DBHandler:

    def __enter__(self):
        self.conn = sqlite3.connect(os.path.relpath('resturant_database.db'))
        self.cursor = self.conn.cursor()
        return self.cursor
    
    def __exit__(self):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
        