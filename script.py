import sqlite3 as sq


def check_table_allhistory_for_broughtacartridge(i):
    # Ищем дату и ID для сравнения строк из таблицы allhistory (данные для BroughtACartridge)

    cartridge_number_id = cursor.execute('SELECT cartridge_number_id FROM BroughtACartridge WHERE id = ?', (i,)).fetchone()[0]
    user = cursor.execute('SELECT user FROM BroughtACartridge WHERE id = ?', (i,)).fetchone()[0]
    date = cursor.execute('SELECT date FROM BroughtACartridge WHERE id = ?', (i,)).fetchone()[0][0:18]
    check_all_history = cursor.execute(
        "SELECT date, id FROM AllHistory WHERE action = ? and user = ? and cartridge_id = ?",
        ('Принят в заправку', user, cartridge_number_id)).fetchall()
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
    action = 'Принят в заправку'
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


def add_str_db_broughtaprinter(i):
    # добавляем новую строку в таблцие allhistory c информацией из BroughtAPrinter

    location = cursor.execute('SELECT location FROM BroughtAPrinter WHERE id = ?', (i,)).fetchone()[0]
    learning_campus = cursor.execute('SELECT learning_campus FROM BroughtAPrinter WHERE id = ?', (i,)).fetchone()[0]
    cabinet = cursor.execute('SELECT cabinet FROM BroughtAPrinter WHERE id = ?', (i,)).fetchone()[0]
    user = cursor.execute('SELECT user FROM BroughtAPrinter WHERE id = ?', (i,)).fetchone()[0]
    type_ = 'принтер'
    date = cursor.execute('SELECT date FROM BroughtAPrinter WHERE id = ?', (i,)).fetchone()[0]
    printer_id = cursor.execute('SELECT printer_id FROM BroughtAPrinter WHERE id = ?', (i,)).fetchone()[0]
    name = cursor.execute("SELECT name FROM printer WHERE id = ?", (printer_id, )).fetchone()[0]
    action = 'В подразделении'
    data = location, learning_campus, cabinet, user, date, type_, printer_id, name, action
    cursor.execute("INSERT INTO AllHistory "
                   "(location, learning_campus, cabinet, user, date, type, printer_id, name, action)"
                   " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", data)
    base.commit()
    print(f'\n Строка создана'
          f'\n ID в BroughtAPrinter: {i}\n')


def update_column_broughtaprinter(i, id_column):
    # изменяем строку в таблцие allhistory с информацией из broughtaprinter

    location = cursor.execute('SELECT location FROM BroughtAPrinter WHERE id = ?', (i,)).fetchone()[0]
    learning_campus = cursor.execute('SELECT learning_campus FROM BroughtAPrinter WHERE id = ?', (i,)).fetchone()[0]
    cabinet = cursor.execute('SELECT cabinet FROM BroughtAPrinter WHERE id = ?', (i,)).fetchone()[0]
    printer_id = cursor.execute('SELECT printer_id FROM BroughtAPrinter WHERE id = ?', (i,)).fetchone()[0]

    data = location, learning_campus, cabinet, printer_id, id_column
    cursor.execute("UPDATE AllHistory SET location = ?, learning_campus = ?, cabinet = ?, printer_id = ?"
                   "WHERE id = ?", data)
    base.commit()
    print(f'\n Колонки изменены\n'
          f'\n ID колонки в allhistory: {id_column}'
          f'\n ID колонки в BroughtAPrinter: {i}\n')


def check_table_allhistory_for_broughtaprinter(i):
    # Ищем дату и ID для сравнения строк из таблицы allhistory (данные для CartridgeIssuance)

    printer_id = cursor.execute('SELECT printer_id FROM BroughtAPrinter WHERE id = ?', (i,)).fetchone()[0]
    user = cursor.execute('SELECT user FROM BroughtAPrinter WHERE id = ?', (i,)).fetchone()[0]
    date = cursor.execute('SELECT date FROM BroughtAPrinter WHERE id = ?', (i,)).fetchone()[0][0:18]
    check_all_history = cursor.execute(
        "SELECT date, id FROM AllHistory WHERE action = ? and user = ? and printer_id = ?",
        ('В подразделении', user, printer_id)).fetchall()
    return check_all_history, date


def main_func():
    global base, cursor
    # Подключение к БД
    base = sq.connect('printersDB.db')
    cursor = base.cursor()

    # работа с broughtcartridge
    max_number = cursor.execute('SELECT max(id) FROM BroughtACartridge').fetchone()[0]
    new_str = 0
    correct_str = 0
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
    new_str = 0
    correct_str = 0

    # работа с BroughtAPrinter
    max_number = cursor.execute('SELECT max(id) FROM BroughtAPrinter').fetchone()[0]
    for i in range(1, max_number + 1):
        check_all_history, date = check_table_allhistory_for_broughtaprinter(i)
        if len(check_all_history) != 0:
            for date_in_column, id_column in check_all_history:
                flag = True
                if date in date_in_column:
                    update_column_broughtaprinter(i, id_column)
                    correct_str += 1
                    flag = False
                    print(f'date historu: {date}'
                          f'date other: {date_in_column}')
                    break
            if flag:
                add_str_db_broughtaprinter(i)
                new_str += 1
        else:
            add_str_db_broughtaprinter(i)
            new_str += 1
    print(f'\n**********************\n'
          f'Новые строки: {new_str}\n'
          f'Отредаченные строки {correct_str}\n'
          f'Всего: {new_str + correct_str}\n')

    max_number = cursor.execute('SELECT max(id) FROM AllHistory').fetchone()[0]
    for id_bd in range(1, max_number + 1):
        user = cursor.execute('SELECT user FROM AllHistory WHERE id = ?', (id_bd, )).fetchone()[0]
        if "@" in user:
            print('Было - ', user)
            user = user.split('@')[0]
            cursor.execute(f"UPDATE AllHistory SET user = ? WHERE id = ?", (user, id_bd))
            print(f'Стало {id_bd} - ', user, '\n')
        type_machine = cursor.execute('SELECT type FROM AllHistory WHERE id = ?', (id_bd, )).fetchone()[0]
        if type_machine == "принтер":
            cursor.execute(f"UPDATE AllHistory SET type = ? WHERE id = ?", ("Принтер", id_bd))
        if type_machine == "картридж":
            cursor.execute(f"UPDATE AllHistory SET type = ? WHERE id = ?", ("Картридж", id_bd))

    base.commit()

    for id_db_allhistory in range(1, max_number + 1):
        action = cursor.execute('SELECT action FROM AllHistory WHERE id = ?', (id_db_allhistory,)).fetchone()[0]
        if action == "Создан" or action == "Восстановлен":
            cursor.execute(f'UPDATE AllHistory SET status = ? WHERE id = ?', ('В резерве', id_db_allhistory))
        elif action == "Изменён":
            type_machine = cursor.execute('SELECT type FROM AllHistory WHERE id = ?', (id_db_allhistory,)).fetchone()[0]
            if type_machine == "Картридж":
                cartridge_id = cursor.execute('SELECT cartridge_id FROM AllHistory WHERE id = ?', (id_db_allhistory,)).fetchone()[0]
                max_cartridge_id = cursor.execute('SELECT id  FROM AllHistory WHERE cartridge_id = ?', (cartridge_id,)).fetchall()
                if id_db_allhistory == max_cartridge_id[-1][0]:
                    if len(max_cartridge_id) == 2:
                        action = cursor.execute('SELECT action  FROM AllHistory WHERE cartridge_id = ? AND id = ?', (cartridge_id, max_cartridge_id[0][0])).fetchone()[0]
                        if action == "Создан" or action == "Восстановлен":
                            cursor.execute(f'UPDATE AllHistory SET status = ? WHERE id = ?',
                                           ('В резерве', max_cartridge_id[0][0]))
                            cursor.execute(f'UPDATE AllHistory SET status = ? WHERE id = ?',
                                           ('В резерве', max_cartridge_id[-1][0]))
                        elif action == "Изменён":
                            print(f"***\nНужно проверить\n"
                                  f"id_db_allhistory = {id_db_allhistory}")
                        else:
                            cursor.execute(f'UPDATE AllHistory SET status = ? WHERE id = ?', (action, max_cartridge_id[0][0]))
                    else:
                        print(f"***\nНужно проверить\n"
                              f"id_db_allhistory = {id_db_allhistory}")
            elif type_machine == "Принтер":
                printer_id = cursor.execute('SELECT printer_id FROM AllHistory WHERE id = ?', (id_db_allhistory,)).fetchone()[0]
                max_printer_id = cursor.execute('SELECT id FROM AllHistory WHERE printer_id = ?', (printer_id,)).fetchall()
                if id_db_allhistory == max_printer_id[-1][0]:
                    if len(max_printer_id) == 2:
                        action = cursor.execute('SELECT action  FROM AllHistory WHERE printer_id = ? AND id = ?', (printer_id, max_printer_id[0][0])).fetchone()[0]
                        if action == "Создан" or action == "Восстановлен":
                            cursor.execute(f'UPDATE AllHistory SET status = ? WHERE id = ?',
                                           ('В резерве', max_printer_id[0][0]))
                            cursor.execute(f'UPDATE AllHistory SET status = ? WHERE id = ?',
                                           ('В резерве', max_printer_id[-1][0]))
                        elif action == "Изменён":
                            print(f"***\nНужно проверить\n"
                                  f"id_db_allhistory = {id_db_allhistory}")
                        else:
                            cursor.execute(f'UPDATE AllHistory SET status = ? WHERE id = ?', (action, max_printer_id[0][0]))
                    else:
                        print(f"***\nНужно проверить\n"
                              f"id_db_allhistory = {id_db_allhistory}")
            else:
                print(f'Статус не Принтер и не Картридж - id_allhistory{id_db_allhistory}')
        else:
            cursor.execute(f'UPDATE AllHistory SET status = ? WHERE id = ?', (action, id_db_allhistory))
        base.commit()
