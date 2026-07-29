import sqlite3
from src.backend.Extension import Extension

class DatabaseConnection:
    def __init__(self):
        self.connection = sqlite3.connect('extensions.db')
        self.cursor = self.connection.cursor()

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS extensions (
                    id integer primary key,
                    approved integer
                    )""")

    def insert_ext(self, ext: Extension):
        with self.connection:
            self.cursor.execute("INSERT OR IGNORE INTO extensions VALUES (:id, :approved)", {'id': ext.id, 'approved': int(ext.approved)})

    def get_exts_by_approval(self, approval: bool):
        self.cursor.execute("SELECT * FROM extensions WHERE approved=:approved", {'approved': int(approval)})
        return self.cursor.fetchall()

    def get_all_exts(self):
        self.cursor.execute("SELECT * FROM extensions")
        return self.cursor.fetchall()

    def update_approval(self, ext: Extension, approval: bool):
        with self.connection:
            self.cursor.execute("""UPDATE extensions SET approved = :approved
                        WHERE id = :id""",
                    {'id': ext.id, 'approved': approval})

    def remove_ext(self, ext: Extension):
        with self.connection:
            self.cursor.execute("DELETE from extensions WHERE id = :id AND approved = :approved",
                    {'id': ext.id, 'approved': ext.approved})

    def close(self):
        print(self.get_all_exts())
        self.connection.close()