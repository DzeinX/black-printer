import pandas as pd
from flask import flash, redirect, request, url_for

from Validate.ScanFunctions import TypeVar
from Model.ModelController import ModelController

model_controller = ModelController()


def prevent_valid(var_type: str, variables):
    """
    Проверка на валидность переменной. Если всё хорошо, то приводит её к переданному типу (var_type: str)
    :param var_type: Тип приводимой переменой.
    :param variables: Проверяемая переменная.
                      Если передаётся list, то после работы функции проверить можно таким способом:
                                  'if type(`variables`) is not list:
                                        return `variables`',
                      Иначе можно проверить следующим образом:
                                  'if type(`variables`) is not `var_type`:
                                        return `variables`',
                      То есть, если передаётся одна переменная, которую нужно проверить,
                      то в проверке будет проверка на ёё тип приведения.
    :return: В случае успеха возвращает переменную, иначе возвращает ссылку с ошибкой.
    """
    var_check = TypeVar(variables, var_type=var_type)
    if var_check[1]:
        return var_check[0][0]
    else:
        if isinstance(var_check[0], str):
            flash(var_check[0])
            return redirect(request.referrer)
        else:
            flash('Недопустимое значение в форме', 'error')
            return redirect(request.referrer)


def try_to_commit(redirect_to: str):
    """
    Функция пытается сохранить все изменения, которые были совершены в последней сессии базы данных.
    :param redirect_to: Имя метода отслеживания URI запросов. Пишется подобным образом '`name_file`.`name_method`'
    :return: Переадресация на главную страницу, в случае ошибки, и на страницу, введённую пользователем, в случае успеха
    """
    try:
        model_controller.commit_session()
        flash(f'Успешно сохранено', 'success')
        if 'http' in redirect_to:
            return redirect(redirect_to)
        return redirect(url_for(redirect_to))
    except Exception as e:
        flash(f'Не удалось сохранить изменения. Ошибка: {e}', 'error')
        return redirect(url_for('main_urls.main_page'))


def save_in_history(**kwargs):
    """
    Оболочка для сохранения в таблицу AllHistory.
    Проверить подобным образом:
            'if `request_redirect` is not None:
                return `request_redirect`.
    В `request_redirect` записывается значение, которое вернёт функция.
    :param kwargs: Переменные и значения, которые нужны для создания записи в таблице AllHistory.
    :return: None в случае успеха, иначе вернёт переадресацию на главную страницу с ошибкой.
    """
    try:
        history = model_controller.create(model_name='AllHistory',
                                          **kwargs)

        return model_controller.add_in_session(history)
    except Exception as e:
        flash(f'При создании статуса произошла ошибка. Ошибка: {e}', 'error')
        return redirect(url_for('main_urls.main_page'))


def get_entries_for_work_list_cartridges(work_list_cartridges):
    wlc = []
    for work_cartridge in work_list_cartridges:
        cartridge = model_controller.get_model_by_id(model_name="Cartridges",
                                                     pk=work_cartridge.cartridge_id)
        price = model_controller.filter_by_model(model_name="WorksPricesCartridges",
                                                 mode="first",
                                                 work_lists_cartridges_id=work_cartridge.id)
        action = model_controller.get_model_by_id(model_name="AllWorksCartridges",
                                                  pk=price.all_works_cartridges_id)
        wlc.append([price.price, action.work, cartridge, work_cartridge.id])
    return wlc


def get_entries_for_work_list_printers(work_list_printers):
    wlp = []
    for work_printer in work_list_printers:
        printer = model_controller.get_model_by_id(model_name="Printer",
                                                   pk=work_printer.printer_id)
        price = model_controller.filter_by_model(model_name="WorksPricesPrinters",
                                                 mode="first",
                                                 work_lists_printers_id=work_printer.id)
        action = model_controller.get_model_by_id(model_name="AllWorksPrinters",
                                                  pk=price.all_works_printers_id)
        wlp.append([price.price, action.work, printer, work_printer.id])
    return wlp


def scan_list_of_completed_works(file, all_works_cartridges, all_works_printers):
    entries_cartridges_data = []
    entries_printers_data = []
    printer_hints = []
    cartridge_hints = []
    refueling = None
    for cartridge_works in all_works_cartridges:
        if "заправка" in cartridge_works.work.lower():
            refueling = cartridge_works.work
            break

    for item in range(21, len(file)):
        column_data = []
        for data in dict(file[file.index == item]):
            text_in_cell = str(list(dict(file[file.index == item])[data])[0])
            if text_in_cell != "nan":
                column_data.append(text_in_cell)

        for counter in range(int(column_data[2])):
            if "принт" in column_data[1]:
                entries_printers_data.append([int(column_data[4]),
                                              None,
                                              None,
                                              None])
                printer_hints.append(column_data[1])
            else:
                work_for_cartridge = None
                if "заправка" in column_data[1].lower():
                    work_for_cartridge = refueling

                entries_cartridges_data.append([int(column_data[4]),
                                                work_for_cartridge,
                                                None,
                                                None])
                cartridge_hints.append(column_data[1])
    return [entries_cartridges_data, cartridge_hints, entries_printers_data, printer_hints]


def all_checks_is_active(contract) -> bool:
    for check in contract.check_lists_id:
        if not check.active:
            return False
    return True


def get_check_price(check) -> float:
    check_price = 0
    for wl in check.work_lists_id:
        for wl_c in wl.work_list_cartridges_id:
            for wp_c in wl_c.works_prices_cartridges_id:
                check_price += wp_c.price
        for wl_p in wl.work_list_printers_id:
            for wp_p in wl_p.works_prices_printers_id:
                check_price += wp_p.price
    return round(check_price)


def get_work_done_price(work_list) -> float:
    check_price = 0
    for wl_c in work_list.work_list_cartridges_id:
        for wp_c in wl_c.works_prices_cartridges_id:
            check_price += wp_c.price
    for wl_p in work_list.work_list_printers_id:
        for wp_p in wl_p.works_prices_printers_id:
            check_price += wp_p.price
    return round(check_price)


def get_contract_price(contract) -> float:
    check_price = 0
    for check in contract.check_lists_id:
        for wl in check.work_lists_id:
            for wl_c in wl.work_list_cartridges_id:
                for wp_c in wl_c.works_prices_cartridges_id:
                    check_price += wp_c.price
            for wl_p in wl.work_list_printers_id:
                for wp_p in wl_p.works_prices_printers_id:
                    check_price += wp_p.price
    return round(check_price)


def check_extensions(file_name: str, extensions: list) -> bool:
    file_extension = file_name.split('.')[-1].lower()
    return True if file_extension in extensions else False
