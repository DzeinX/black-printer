import sqlite3 as sq


def add_column_bd():
    # Создание столбцов в таблице AllHistory
    cursor.execute('ALTER TABLE AllHistory ADD COLUMN location VARCHAR(15)')
    cursor.execute('ALTER TABLE AllHistory ADD COLUMN learning_campus VARCHAR(35)')
    cursor.execute('ALTER TABLE AllHistory ADD COLUMN cabinet VARCHAR(15)')


def check_table_allhistory_for_broughtacartridge(i):
    # Ищем дату и ID для сравнения строк из таблицы allhistory (данные для BroughtACartridge)

    cartridge_number_id = cursor.execute('SELECT cartridge_number_id FROM BroughtACartridge WHERE id = ?', (i,)).fetchone()[0]
    user = cursor.execute('SELECT user FROM BroughtACartridge WHERE id = ?', (i,)).fetchone()[0]
    date = cursor.execute('SELECT date FROM BroughtACartridge WHERE id = ?', (i,)).fetchone()[0][0:18]
    check_all_history = cursor.execute(
        "SELECT date, id FROM AllHistory WHERE action = ? and user = ? and cartridge_id = ?",
        ('В заправке', user, cartridge_number_id)).fetchall()
    return check_all_history, date


def update_column_broughtacartridge(i, id_column):
    # изменяем строку в таблцие allhistory с информацией из BroughtACartridge

    location = cursor.execute('SELECT location FROM BroughtACartridge WHERE id = ?', (i,)).fetchone()[0]
    learning_campus = cursor.execute('SELECT learning_campus FROM BroughtACartridge WHERE id = ?', (i,)).fetchone()[0]
    cabinet = cursor.execute('SELECT cabinet FROM BroughtACartridge WHERE id = ?', (i,)).fetchone()[0]
    cartridge_number_id = cursor.execute('SELECT cartridge_number_id FROM BroughtACartridge WHERE id = ?', (i,)).fetchone()[0]

    data = location, learning_campus, cabinet, cartridge_number_id, id_column
    cursor.execute("UPDATE AllHistory SET location = ?, learning_campus = ?, cabinet = ?, cartridge_id = ?"
                   "WHERE id = ?", data)
    base.commit()
    print(f'\n Колонки изменены\n'
          f'\n ID колонки в allhistory: {id_column}'
          f'\n ID колонки в BroughtACartridge: {i}\n')


def add_str_db_broughtacartridge(i):
    # добавляем новую строку в таблцие allhistory c информацией из BroughtACartridge

    location = cursor.execute('SELECT location FROM BroughtACartridge WHERE id = ?', (i,)).fetchone()[0]
    learning_campus = cursor.execute('SELECT learning_campus FROM BroughtACartridge WHERE id = ?', (i,)).fetchone()[0]
    cabinet = cursor.execute('SELECT cabinet FROM BroughtACartridge WHERE id = ?', (i,)).fetchone()[0]
    user = cursor.execute('SELECT user FROM BroughtACartridge WHERE id = ?', (i,)).fetchone()[0]
    type_ = 'Картридж'
    date = cursor.execute('SELECT date FROM BroughtACartridge WHERE id = ?', (i,)).fetchone()[0]
    cartridge_number_id = cursor.execute('SELECT cartridge_number_id FROM BroughtACartridge WHERE id = ?', (i,)).fetchone()[0]
    name = cursor.execute("SELECT number FROM cartridges WHERE id = ?", (cartridge_number_id,)).fetchone()[0]
    action = 'В заправке'
    data = location, learning_campus, cabinet, user, date, type_, cartridge_number_id, name, action
    cursor.execute("INSERT INTO AllHistory "
                   "(location, learning_campus, cabinet, user, date, type, cartridge_id, name, action)"
                   " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", data)
    base.commit()
    print(f'\n Строка создана'
          f'\n ID в BroughtACartridge: {i}\n')


def check_table_allhistory_for_cartridgeissuance(i):
    # Ищем дату и ID для сравнения строк из таблицы allhistory (данные для CartridgeIssuance)

    cartridge_number_id = cursor.execute('SELECT cartridge_number_id FROM CartridgeIssuance WHERE id = ?', (i,)).fetchone()[0]
    user = cursor.execute('SELECT user FROM CartridgeIssuance WHERE id = ?', (i,)).fetchone()[0]
    date = cursor.execute('SELECT date FROM CartridgeIssuance WHERE id = ?', (i,)).fetchone()[0][0:18]
    check_all_history = cursor.execute(
        "SELECT date, id FROM AllHistory WHERE action = ? and user = ? and cartridge_id = ?",
        ('В подразделении', user, cartridge_number_id)).fetchall()
    return check_all_history, date


def add_str_db_cartridgeissuance(i):
    # добавляем новую строку в таблцие allhistory c информацией из CartridgeIssuance

    location = cursor.execute('SELECT location FROM CartridgeIssuance WHERE id = ?', (i,)).fetchone()[0]
    learning_campus = cursor.execute('SELECT learning_campus FROM CartridgeIssuance WHERE id = ?', (i,)).fetchone()[0]
    cabinet = cursor.execute('SELECT cabinet FROM CartridgeIssuance WHERE id = ?', (i,)).fetchone()[0]
    user = cursor.execute('SELECT user FROM CartridgeIssuance WHERE id = ?', (i,)).fetchone()[0]
    type_ = 'Картридж'
    date = cursor.execute('SELECT date FROM CartridgeIssuance WHERE id = ?', (i,)).fetchone()[0]
    cartridge_number_id = cursor.execute('SELECT cartridge_number_id FROM CartridgeIssuance WHERE id = ?', (i,)).fetchone()[0]
    name = cursor.execute("SELECT number FROM cartridges WHERE id = ?", (cartridge_number_id, )).fetchone()[0]
    action = 'В подразделении'
    data = location, learning_campus, cabinet, user, date, type_, cartridge_number_id, name, action
    cursor.execute("INSERT INTO AllHistory "
                   "(location, learning_campus, cabinet, user, date, type, cartridge_id, name, action)"
                   " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", data)
    base.commit()
    print(f'\n Строка создана'
          f'\n ID в CartridgeIssuance: {i}\n')


def update_column_cartridgeissuance(i, id_column):
    # изменяем строку в таблцие allhistory с информацией из CartridgeIssuance

    location = cursor.execute('SELECT location FROM CartridgeIssuance WHERE id = ?', (i,)).fetchone()[0]
    learning_campus = cursor.execute('SELECT learning_campus FROM CartridgeIssuance WHERE id = ?', (i,)).fetchone()[0]
    cabinet = cursor.execute('SELECT cabinet FROM CartridgeIssuance WHERE id = ?', (i,)).fetchone()[0]
    cartridge_number_id = cursor.execute('SELECT cartridge_number_id FROM CartridgeIssuance WHERE id = ?', (i,)).fetchone()[0]

    data = location, learning_campus, cabinet, cartridge_number_id, id_column
    cursor.execute("UPDATE AllHistory SET location = ?, learning_campus = ?, cabinet = ?, cartridge_id = ?"
                   "WHERE id = ?", data)
    base.commit()
    print(f'\n Колонки изменены\n'
          f'\n ID колонки в allhistory: {id_column}'
          f'\n ID колонки в CartridgeIssuance: {i}\n')


def main_func():
    global base, cursor
    # Подключение к БД
    base = sq.connect('printersDB.db')
    cursor = base.cursor()

    add_column_bd()

    # работа с broughtcartridge
    max_number = cursor.execute('SELECT max(id) FROM BroughtACartridge').fetchone()[0]
    new_str = 0
    correct_str = 0
    if max_number is not None:
        for i in range(1, max_number + 1):
            check_all_history, date = check_table_allhistory_for_broughtacartridge(i)
            if len(check_all_history) != 0:
                for date_in_column, id_column in check_all_history:
                    print(f'{date} == {date_in_column}')
                    flag = True
                    if date in date_in_column:
                        update_column_broughtacartridge(i, id_column)
                        correct_str += 1
                        flag = False
                        print(f'date historu: {date}'
                              f'date other: {date_in_column}')
                        break
                if flag:
                    add_str_db_broughtacartridge(i)
                    new_str += 1
            else:
                add_str_db_broughtacartridge(i)
                new_str += 1
        print(f'\n**********************\n'
              f'Новые строки: {new_str}\n'
              f'Отредаченные строки {correct_str}\n'
              f'Всего: {new_str + correct_str}\n'
              f'************************\n')
        new_str = 0
        correct_str = 0

    # работа с cartridgeissuance
    max_number = cursor.execute('SELECT max(id) FROM CartridgeIssuance').fetchone()[0]
    min_number = cursor.execute('SELECT min(id) FROM CartridgeIssuance').fetchone()[0]
    if max_number is not None or min_number is not None:
        for i in range(min_number, max_number + 1):
            check_all_history, date = check_table_allhistory_for_cartridgeissuance(i)
            if len(check_all_history) != 0:
                for date_in_column, id_column in check_all_history:
                    flag = True
                    if date in date_in_column:
                        update_column_cartridgeissuance(i, id_column)
                        correct_str += 1
                        flag = False
                        print(f'date historu: {date}'
                              f'date other: {date_in_column}')
                        break
                if flag:
                    add_str_db_cartridgeissuance(i)
                    new_str += 1
            else:
                add_str_db_cartridgeissuance(i)
                new_str += 1
        print(f'\n**********************\n'
              f'Новые строки: {new_str}\n'
              f'Отредаченные строки {correct_str}\n'
              f'Всего: {new_str + correct_str}\n')
