import os
import sqlite3

class DatabaseManager:
    def __init__(self, db_name="database.db"):
        self.db_path = os.path.join(os.path.dirname(__file__), db_name)
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

        self.create_tables()

    def create_tables(self):
        with open(os.path.join(os.path.dirname(__file__), "schema.sql"), "r") as f:
            self.cursor.executescript(f.read())
        self.conn.commit()

    def execute_query(self, query, params=()):
        self.cursor.execute(query, params)
        self.conn.commit()
    
    def fetch_all(self, query, params=()):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def close_connection(self):
        self.conn.close()

db = DatabaseManager()
result = db.fetch_all("SELECT exercises.name, muscle_groups.name FROM exercises JOIN muscle_groups ON exercises.muscle_group_id = muscle_groups.id")
print(result)