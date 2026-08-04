import sqlite3
from src.backend.Extension import Extension

class DatabaseConnection:
    def __init__(self, instructor):
        self.connection = sqlite3.connect('extensions.db')
        self.cursor = self.connection.cursor()
        self.instructor = instructor

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS extensions (
                            id integer primary key,
                            instructor integer,
                            approved integer,
                            note text
                            )""")

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS instructors (
                            id text primary key,
                            form_id text,
                            form_url text
                            )""")

    def insert_instructor(self, form_id, form_url):
        with self.connection:
            self.cursor.execute("""INSERT OR IGNORE INTO instructors VALUES (:id, :form_id, :form_url)""", 
            {'id': self.instructor, 'form_id': form_id, 'form_url': form_url})

    def get_instructor(self):
        self.cursor.execute("SELECT * FROM instructors WHERE id=:id", {'id': self.instructor})
        return self.cursor.fetchone()

    def insert_ext(self, ext: Extension):
        with self.connection:
            self.cursor.execute("""INSERT OR IGNORE INTO extensions VALUES (:id, :instructor, :approved, :note)""", 
            {'id': ext.id, 'instructor': self.instructor, 'approved': int(ext.approved), 'note': ext.note})

    def get_exts_by_approval(self, approval: bool):
        self.cursor.execute("SELECT * FROM extensions WHERE approved=:approved", {'approved': int(approval)})
        return self.cursor.fetchall()

    def get_all_exts(self):
        self.cursor.execute("SELECT * FROM extensions")
        return self.cursor.fetchall()

    def update_approval(self, ext: Extension, approval: bool, note: str = ""):
        with self.connection:
            self.cursor.execute("""UPDATE extensions SET approved = :approved, note = :note WHERE id = :id""",
                    {'id': ext.id, 'approved': approval, 'note': note})

    def remove_ext(self, ext: Extension):
        with self.connection:
            self.cursor.execute("DELETE from extensions WHERE id = :id", {'id': ext.id})

    def close(self):
        print(self.get_all_exts())
        self.connection.close()