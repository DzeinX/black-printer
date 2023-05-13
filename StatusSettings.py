class StatusSettings(object):
    class Types(object):
        printer = "Принтер"
        cartridge = "Картридж"
        work_list = "Список работ"
        check = "Счёт"
        contract = "Договор"

    class Printer(object):
        created = "Создан"
        updated = "Изменён"
        restored = "Восстановлен"
        deleted = "Удалён"
        in_division = "В подразделении"
        accepted_for_repair = "Принят в ремонт"
        in_repair = "В ремонте"
        in_reserve = "В резерве"

    class Cartridge(object):
        created = "Создан"
        updated = "Изменён"
        restored = "Восстановлен"
        deleted = "Удалён"
        in_division = "В подразделении"
        in_reserve = "В резерве"
        in_refueling = "В заправке"
        accepted_for_refuel = "Принят в заправку"

    class WorkList(object):
        created = "Создан"
        updated = "Изменён"

    class Check(object):
        created = "Создан"
        replenished = "Пополнен"
        reopen = "Переоткрыт"
        close = "Закрыт"

    class Contract(object):
        created = "Создан"
        close = "Закрыт"
