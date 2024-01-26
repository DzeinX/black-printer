import sqlite3 as sq


def setup():
    base = sq.connect('printersDB.db')
    cursor = base.cursor()

    replacing(cursor)
    base.commit()


def replacing(cursor):
    cursor.execute(f"UPDATE AllHistory SET status = ? WHERE status = ? and type='Принтер'",
                   ("В подразделении", "Получен из ремонта"))
    print("[INFO] Замена \"Получен из ремонта\" на \"В подразделении\" для принтеров выполнена")

    cursor.execute(f"UPDATE AllHistory SET status = ? WHERE status = ? and type='Принтер'",
                   ("Принят в ремонт", "Принят в заправку"))
    print("[INFO] Замена \"Принят в заправку\" на \"Принят в ремонт\" для принтеров выполнена")
