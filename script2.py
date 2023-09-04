import sqlite3 as sq


def setup():
    base = sq.connect('printersDB.db')
    cursor = base.cursor()

    replacing(cursor)
    base.commit()


def replacing(cursor):
    cursor.execute(f"UPDATE AllHistory SET status = ? WHERE status = ? or status = ?", ("В резерве", "Создан", "создан"))
