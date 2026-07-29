import sqlite3
from Extension import Extension

conn = sqlite3.connect(':memory:')

c = conn.cursor()

c.execute("""CREATE TABLE extensions (
            id integer,
            approved integer
            )""")


def insert_ext(ext: Extension):
    with conn:
        c.execute("INSERT INTO extensions VALUES (:id, :approved)", {'id': ext.id, 'approved': int(ext.approved)})


def get_exts_by_approval(approval: bool):
    c.execute("SELECT * FROM extensions WHERE approved=:approved", {'approved': int(approval)})
    return c.fetchall()


def update_approval(ext: Extension, approval: bool):
    with conn:
        c.execute("""UPDATE extensions SET approved = :approved
                    WHERE id = :id""",
                  {'id': ext.id, 'approved': approval})


def remove_ext(ext: Extension):
    with conn:
        c.execute("DELETE from extensions WHERE id = :id AND approved = :approved",
                  {'id': ext.id, 'approved': ext.approved})

ext_1 = Extension('john')
ext_2 = Extension('jane')

insert_ext(ext_1)
insert_ext(ext_2)

exts = get_exts_by_approval(False)
print(exts)

update_approval(ext_2, True)
remove_ext(ext_1)

exts = get_exts_by_approval(False)
print(exts)

exts = get_exts_by_approval(True)
print(exts)

conn.close()