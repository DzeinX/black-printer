import sqlite3 as sq

from alembic import op


def get_data():
    base = sq.connect('printersDB.db')
    cursor = base.cursor()
    return cursor.execute(f"SELECT name, id FROM printer").fetchall()


def set_data(data):
    base = sq.connect('printersDB.db')
    cursor = base.cursor()
    for name, id in data:
        name = name.strip()
        model_name = cursor.execute("SELECT model FROM ListModelsPrinter WHERE LOWER(model) = LOWER(?)", (name,)).fetchone()
        if model_name is None:
            with op.get_context().autocommit_block():
                cursor.execute("INSERT INTO ListModelsPrinter (model) VALUES (?)", (name,))
            base.commit()
            print("[ДОБАВЛЕН ListModelsPrinter] model='" + str(name) + "'")
        with op.get_context().autocommit_block():
            cursor.execute("UPDATE printer SET name = ? WHERE id = ?", (name, id))
        base.commit()
        print("[ИЗМЕНЁН printer] name='" + str(name) + "'")
