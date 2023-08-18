from flask import render_template
from flask import url_for
from flask import redirect
from flask import request
from datetime import datetime
from flask import flash
from flask_login import login_required

from Controller.SupportFunctions import prevent_valid, try_to_commit, save_in_history
from Model.ModelController import ModelController
from Settings.StatusSettings import StatusSettings
from flask_login import current_user

from Settings.Blueprint import PrinterBlueprint

blueprint = PrinterBlueprint()
printer_urls = blueprint.get_url()

# Управление базой данных
model_controller = ModelController()


class PrinterURLs:
    @staticmethod
    @printer_urls.route('/add_works_printers', methods=['GET', 'POST'])
    @login_required
    def add_works_printers():
        if not current_user.is_boss:
            return redirect(url_for('main_urls.main_page'))

        if request.method == "GET":
            all_works_printers = model_controller.get_all_entries(model_name='AllWorksPrinters')
            counter_works = len(all_works_printers)
            return render_template("Printer_urls/AddWorksPrinters.html",
                                   all_works_printers=all_works_printers,
                                   counter_works=counter_works)

        if request.method == "POST":
            all_works_printers = request.form.getlist('works')

            if len(all_works_printers) == 0:
                flash('Нельзя удалить все модели')
                return redirect(url_for('printer_urls.add_works_printers'))

            model_controller.delete_all_entries_in_model(model_name="AllWorksPrinters")

            try:
                for work in all_works_printers:
                    work = work.strip()
                    is_not_available = model_controller.filter_by_model(model_name="AllWorksPrinters",
                                                                        mode="first",
                                                                        work=work) is None
                    if work != '' and is_not_available:
                        model = model_controller.create(model_name="AllWorksPrinters",
                                                        work=work)
                        model_controller.add_in_session(model)
            except Exception as e:
                flash(f'Не удалось сохранить изменения. Ошибка: {e}')
                return redirect(url_for('main_urls.main_page'))

            return try_to_commit(redirect_to='printer_urls.add_works_printers')

        flash(f'Не определён метод запроса!')
        return redirect(url_for('main_urls.main_page'))

    @staticmethod
    @printer_urls.route('/printer/<int:pk>/update', methods=['GET', 'POST'])
    @login_required
    def update_printer(pk):
        if request.method == "GET":
            printer = model_controller.get_model_by_id(model_name='Printer',
                                                       pk=pk)
            divisions = model_controller.get_all_entries(model_name='Division')
            buildings = model_controller.get_all_entries(model_name='Buildings')
            return render_template("Printer_urls/printer_update.html",
                                   printer=printer,
                                   divisions=divisions,
                                   buildings=buildings)

        if request.method == "POST":
            printer = model_controller.get_model_by_id(model_name='Printer',
                                                       pk=pk)
            name = request.form['name'].strip()
            num_inventory = request.form['num_inventory'].strip()
            location = request.form['location'].strip()
            learning_campus = request.form['learning_campus'].strip()
            cabinet = request.form['cabinet'].strip()

            model_controller.update(model_entry=printer,
                                    name=name,
                                    num_inventory=num_inventory,
                                    location_now=location,
                                    learning_campus_now=learning_campus,
                                    cabinet_now=cabinet)

            action_history = StatusSettings.Printer.updated
            type_history = StatusSettings.Types.printer
            name_history = printer.num_inventory
            user = current_user.username
            last_all_history = model_controller.filter_by_model(model_name='AllHistory',
                                                                mode='all',
                                                                printer_id=printer.id)[-1]
            request_redirect = save_in_history(action=action_history,
                                               type=type_history,
                                               name=name_history,
                                               user=user,
                                               date=datetime.now(),
                                               printer_id=printer.id,
                                               status=last_all_history.status,
                                               location=last_all_history.location,
                                               learning_campus=last_all_history.learning_campus,
                                               cabinet=last_all_history.cabinet)
            if request_redirect is not None:
                return request_redirect

            return try_to_commit(redirect_to='printer_urls.printers')

        flash(f'Не определён метод запроса!')
        return redirect(url_for('main_urls.main_page'))

    @staticmethod
    @printer_urls.route('/printers/', methods=['GET', 'POST'], defaults={'is_show_own': 1})
    @printer_urls.route('/printers/show=<int:is_show_own>', methods=['GET', 'POST'])
    @login_required
    def printers(is_show_own=1):
        if request.method == "GET":
            printers = model_controller.get_all_entries(model_name="Printer")

            if printers is not None:
                printers.sort(key=lambda c: c.date_added,
                              reverse=True)

            buildings = current_user.buildings_id
            current_buildings = []
            for building in buildings:
                current_buildings.append(building.building)

            printers_data = []
            is_not_find = False
            if is_show_own and current_buildings:
                amount_finding = 0
                for printer in printers:
                    if printer.learning_campus_now in current_buildings:
                        amount_finding += 1
                        history = model_controller.filter_by_model(model_name="AllHistory",
                                                                   mode="all",
                                                                   printer_id=printer.id)
                        history.sort(key=lambda h: h.date,
                                     reverse=True)
                        status = history[0].status
                        printers_data.append([printer, status])

                if amount_finding == 0:
                    is_not_find = True
            else:
                for printer in printers:
                    history = model_controller.filter_by_model(model_name="AllHistory",
                                                               mode="all",
                                                               printer_id=printer.id)
                    history.sort(key=lambda h: h.date,
                                 reverse=True)
                    status = history[0].status
                    printers_data.append([printer, status])

            buildings = model_controller.get_all_entries(model_name="Buildings")
            divisions = model_controller.get_all_entries(model_name="Division")
            return render_template("Printer_urls/Printers.html",
                                   printers_data=printers_data,
                                   buildings=buildings,
                                   divisions=divisions,
                                   StatusSettings=StatusSettings,
                                   is_show_own=is_show_own,
                                   is_not_find=is_not_find)

        if request.method == 'POST':
            name = request.form['name'].strip()
            num_inventory = request.form['num_inventory'].strip()

            check_num_inv_printer = model_controller.filter_by_model(model_name="Printer",
                                                                     mode="all",
                                                                     num_inventory=num_inventory)
            # запрос в таблицу printer выведет строки, в которых инвентарник совпадает с инвентарником введенным юзером
            if len(check_num_inv_printer) != 0:
                # если строка/и с введенным пользователем инвентарником будут найдены сообщаем об этом пользователю
                flash('Принтер с таким инвентарным номером уже существует!')
                return redirect(request.referrer)

            location_now = request.form['location'].strip()
            learning_campus_now = request.form['learning_campus'].strip()
            cabinet_now = request.form['cabinet'].strip()

            status = StatusSettings.Printer.in_division
            printer = model_controller.create(model_name="Printer",
                                              name=name,
                                              num_inventory=num_inventory,
                                              location_now=location_now,
                                              learning_campus_now=learning_campus_now,
                                              cabinet_now=cabinet_now,
                                              date_added=datetime.now())
            model_controller.add_in_session(printer)
            model_controller.commit_session()

            action_history = StatusSettings.Printer.created
            type_history = StatusSettings.Types.printer
            name_history = num_inventory
            user = current_user.username
            request_redirect = save_in_history(action=action_history,
                                               type=type_history,
                                               name=name_history,
                                               date=datetime.now(),
                                               user=user,
                                               printer_id=printer.id,
                                               status=status,
                                               location=location_now,
                                               learning_campus=learning_campus_now,
                                               cabinet=cabinet_now)
            if request_redirect is not None:
                return request_redirect

            return try_to_commit(redirect_to='printer_urls.printers')

        flash(f'Не определён метод запроса!')
        return redirect(url_for('main_urls.main_page'))

    @staticmethod
    @printer_urls.route('/printer/<int:pk>/statuses')
    @login_required
    def printers_status(pk):
        if request.method == "GET":
            statuses = model_controller.filter_by_model(model_name="AllHistory",
                                                        mode="all",
                                                        printer_id=pk)
            statuses.sort(key=lambda all_history: all_history.date,
                          reverse=True)

            printer = model_controller.get_model_by_id(model_name="Printer",
                                                       pk=pk)
            return render_template("Printer_urls/PrinterStatuses.html",
                                   statuses=statuses,
                                   printer=printer,
                                   StatusSettings=StatusSettings)

        flash(f'Не определён метод запроса!')
        return redirect(url_for('main_urls.main_page'))

    @staticmethod
    @printer_urls.route('/printer/<int:pk>/delete')
    @login_required
    def delete_printer(pk):
        if request.method == "GET":
            printer = model_controller.get_model_by_id(model_name="Printer",
                                                       pk=pk)
            try:
                action_history = StatusSettings.Printer.deleted
                type_history = StatusSettings.Types.printer
                name_history = printer.num_inventory
                user = current_user.username
                last_all_history = model_controller.filter_by_model(model_name='AllHistory',
                                                                    mode='all',
                                                                    printer_id=printer.id)[-1]
                request_redirect = save_in_history(action=action_history,
                                                   type=type_history,
                                                   name=name_history,
                                                   date=datetime.now(),
                                                   user=user,
                                                   printer_id=printer.id,
                                                   status=last_all_history.status,
                                                   location=last_all_history.location,
                                                   learning_campus=last_all_history.learning_campus,
                                                   cabinet=last_all_history.cabinet)
                if request_redirect is not None:
                    return request_redirect

                model_controller.update(model_entry=printer,
                                        efficiency=0)

                return try_to_commit(redirect_to='printer_urls.printers')

            except Exception as e:
                flash(f'Ошибка удаления картриджа. Ошибка: {e}')
                return redirect(url_for('main_urls.main_page'))

        flash(f'Не определён метод запроса!')
        return redirect(url_for('main_urls.main_page'))

    @staticmethod
    @printer_urls.route('/printer/<int:pk>/resume')
    @login_required
    def resume_printer(pk):
        if request.method == "GET":
            printer = model_controller.get_model_by_id(model_name="Printer",
                                                       pk=pk)
            try:
                action_history = StatusSettings.Printer.restored
                type_history = StatusSettings.Types.printer
                name_history = printer.num_inventory
                user = current_user.username

                last_all_history = model_controller.filter_by_model(model_name='AllHistory',
                                                                    mode='all',
                                                                    printer_id=printer.id)[-1]
                request_redirect = save_in_history(action=action_history,
                                                   type=type_history,
                                                   name=name_history,
                                                   date=datetime.now(),
                                                   user=user,
                                                   printer_id=printer.id,
                                                   status=last_all_history.status,
                                                   location=last_all_history.location,
                                                   learning_campus=last_all_history.learning_campus,
                                                   cabinet=last_all_history.cabinet)
                if request_redirect is not None:
                    return request_redirect

                model_controller.update(model_entry=printer,
                                        efficiency=1)

                return try_to_commit(redirect_to='printer_urls.deleted_printers')

            except Exception as e:
                flash(f'Ошибка удаления картриджа. Ошибка: {e}')
                return redirect(url_for('main_urls.main_page'))

        flash(f'Не определён метод запроса!')
        return redirect(url_for('main_urls.main_page'))

    @staticmethod
    @printer_urls.route('/deleted_printers')
    @login_required
    def deleted_printers():
        if request.method == "GET":
            printers = model_controller.filter_by_model(model_name="Printer",
                                                        mode="all",
                                                        efficiency=0)

            return render_template('Printer_urls/DeletedPrinters.html',
                                   printers=printers)

        flash(f'Не определён метод запроса!')
        return redirect(url_for('main_urls.main_page'))

    @staticmethod
    @printer_urls.route('/brought_a_printer', methods=['GET', 'POST'])
    @login_required
    def brought_a_printer():
        if request.method == "GET":
            printers = model_controller.filter_by_model(model_name="Printer",
                                                        mode="all",
                                                        efficiency=1)

            printers_data = []
            for printer in printers:
                all_history = model_controller.filter_by_model(model_name='AllHistory',
                                                               mode='all',
                                                               printer_id=printer.id)
                status = all_history[-1].status
                printers_data.append([printer, status])

            buildings = model_controller.get_all_entries(model_name="Buildings")
            divisions = model_controller.get_all_entries(model_name="Division")
            return render_template('Printer_urls/BroughtAPrinter.html',
                                   printers_data=printers_data,
                                   buildings=buildings,
                                   divisions=divisions,
                                   StatusSettings=StatusSettings)

        if request.method == "POST":
            printer_num = request.form.getlist('num_inventory')
            id_form = request.form['id_form'].strip()

            if len(printer_num) == 0:
                flash('Не выбрана ни одна модель')
                return redirect(url_for('printer_urls.brought_a_printer'))

            if id_form == "1":
                location = request.form['location'].strip()
                learning_campus = request.form['learning_campus'].strip()
                cabinet = request.form['cabinet'].strip()
                user = current_user.username

                for number in printer_num:
                    printer = model_controller.filter_by_model(model_name="Printer",
                                                               mode="first",
                                                               num_inventory=number)
                    name_history = number
                    action_history = StatusSettings.Printer.accepted_for_repair
                    type_history = StatusSettings.Types.printer
                    request_redirect = save_in_history(action=action_history,
                                                       type=type_history,
                                                       name=name_history,
                                                       date=datetime.now(),
                                                       user=user,
                                                       printer_id=printer.id,
                                                       status=action_history,
                                                       location=location,
                                                       learning_campus=learning_campus,
                                                       cabinet=cabinet)
                    if request_redirect is not None:
                        return request_redirect

                return try_to_commit(redirect_to='printer_urls.brought_a_printer')

            if id_form == "2":
                for number in printer_num:
                    location = request.form[f'location{number}'].strip()
                    learning_campus = request.form[f'learning_campus{number}'].strip()
                    cabinet = request.form[f'cabinet{number}'].strip()
                    user = current_user.username
                    printer = model_controller.filter_by_model(model_name="Printer",
                                                               mode="first",
                                                               num_inventory=number)

                    name_history = number

                    action_history = StatusSettings.Printer.accepted_for_repair
                    type_history = StatusSettings.Types.printer
                    request_redirect = save_in_history(action=action_history,
                                                       type=type_history,
                                                       name=name_history,
                                                       date=datetime.now(),
                                                       user=user,
                                                       printer_id=printer.id,
                                                       status=action_history,
                                                       location=location,
                                                       learning_campus=learning_campus,
                                                       cabinet=cabinet)
                    if request_redirect is not None:
                        return request_redirect

                return try_to_commit(redirect_to='printer_urls.brought_a_printer')

            flash(f'Не верная идентификация формы!')
            return redirect(url_for('main_urls.main_page'))

        flash(f'Не определён метод запроса!')
        return redirect(url_for('main_urls.main_page'))

    @staticmethod
    @printer_urls.route('/repairing', methods=['GET', 'POST'])
    @login_required
    def repairing():
        if request.method == "GET":
            printers = model_controller.filter_by_model(model_name="Printer",
                                                        mode="all",
                                                        efficiency=1)
            printers_data = []
            for printer in printers:
                all_history = model_controller.filter_by_model(model_name='AllHistory',
                                                               mode='all',
                                                               printer_id=printer.id)
                status = all_history[-1].status
                printers_data.append([printer, status])

            return render_template('Printer_urls/Repairing.html',
                                   printers_data=printers_data,
                                   StatusSettings=StatusSettings)

        if request.method == "POST":
            id_form = request.form['id_form'].strip()
            printer_num = request.form.getlist('num_inventory')
            user = current_user.username

            if len(printer_num) == 0:
                flash('Не выбрана ни одна модель')
                return redirect(url_for('printer_urls.repairing'))

            if id_form == "1":
                for number in printer_num:
                    printer = model_controller.filter_by_model(model_name="Printer",
                                                               mode="first",
                                                               num_inventory=number)
                    repair = model_controller.create(model_name="Repair",
                                                     user=user,
                                                     date=datetime.now(),
                                                     printer_id=printer.id)
                    model_controller.add_in_session(repair)

                    action_history = StatusSettings.Printer.in_repair
                    type_history = StatusSettings.Types.printer
                    name_history = printer.num_inventory
                    request_redirect = save_in_history(action=action_history,
                                                       type=type_history,
                                                       name=name_history,
                                                       date=datetime.now(),
                                                       user=user,
                                                       printer_id=printer.id,
                                                       status=action_history,
                                                       location=printer.location_now,
                                                       learning_campus=printer.learning_campus_now,
                                                       cabinet=printer.cabinet_now)
                    if request_redirect is not None:
                        return request_redirect

                return try_to_commit(redirect_to='printer_urls.repairing')

            if id_form == "2":
                for number in printer_num:
                    printer = model_controller.filter_by_model(model_name="Printer",
                                                               mode="first",
                                                               num_inventory=number)
                    repair = model_controller.create(model_name="Repair",
                                                     user=user,
                                                     date=datetime.now(),
                                                     printer_id=printer.id)
                    model_controller.add_in_session(repair)

                    action_history = StatusSettings.Printer.in_repair
                    type_history = StatusSettings.Types.printer
                    name_history = printer.num_inventory
                    request_redirect = save_in_history(action=action_history,
                                                       type=type_history,
                                                       name=name_history,
                                                       date=datetime.now(),
                                                       user=user,
                                                       printer_id=printer.id,
                                                       status=action_history,
                                                       location=printer.location_now,
                                                       learning_campus=printer.learning_campus_now,
                                                       cabinet=printer.cabinet_now)
                    if request_redirect is not None:
                        return request_redirect

                return try_to_commit(redirect_to='printer_urls.repairing')

            flash(f'Не верная идентификация формы!')
            return redirect(url_for('main_urls.main_page'))

        flash(f'Не определён метод запроса!')
        return redirect(url_for('main_urls.main_page'))

    @staticmethod
    @printer_urls.route('/reception_from_a_repairing', methods=['GET', 'POST'])
    @login_required
    def reception_from_a_repairing():
        if request.method == "GET":
            printers = model_controller.filter_by_model(model_name="Printer",
                                                        mode="all",
                                                        efficiency=1)
            printers_data = []
            for printer in printers:
                all_history = model_controller.filter_by_model(model_name='AllHistory',
                                                               mode='all',
                                                               printer_id=printer.id)
                status = all_history[-1].status
                printers_data.append([printer, status])

            return render_template('Printer_urls/ReceptionFromARepair.html',
                                   printers_data=printers_data,
                                   StatusSettings=StatusSettings)

        if request.method == "POST":
            id_form = request.form['id_form'].strip()
            printer_num = request.form.getlist('num_inventory')
            user = current_user.username

            if len(printer_num) == 0:
                flash('Не выбрана ни одна модель')
                return redirect(url_for('printer_urls.reception_from_a_repairing'))

            if id_form == "1":
                for number in printer_num:
                    printer = model_controller.filter_by_model(model_name="Printer",
                                                               mode="first",
                                                               num_inventory=number)
                    reception_from_a_repairing = model_controller.create(model_name="ReceptionFromARepairing",
                                                                         user=user,
                                                                         date=datetime.now(),
                                                                         printer_id=printer.id)
                    model_controller.add_in_session(reception_from_a_repairing)

                    action_history = StatusSettings.Printer.in_reserve
                    type_history = StatusSettings.Types.printer
                    name_history = printer.num_inventory
                    request_redirect = save_in_history(action=action_history,
                                                       type=type_history,
                                                       name=name_history,
                                                       date=datetime.now(),
                                                       user=user,
                                                       printer_id=printer.id,
                                                       status=action_history,
                                                       location=printer.location_now,
                                                       learning_campus=printer.learning_campus_now,
                                                       cabinet=printer.cabinet_now)
                    if request_redirect is not None:
                        return request_redirect

                    new_work_done = printer.work_done + 1
                    model_controller.update(model_entry=printer,
                                            work_done=new_work_done)

                return try_to_commit(redirect_to='printer_urls.reception_from_a_repairing')

            if id_form == "2":
                for number in printer_num:
                    printer = model_controller.filter_by_model(model_name="Printer",
                                                               mode="first",
                                                               num_inventory=number)
                    reception_from_a_repairing = model_controller.create(model_name="Repair",
                                                                         user=user,
                                                                         date=datetime.now(),
                                                                         printer_id=printer.id)
                    model_controller.add_in_session(reception_from_a_repairing)

                    action_history = StatusSettings.Printer.in_reserve
                    type_history = StatusSettings.Types.printer
                    name_history = printer.num_inventory
                    request_redirect = save_in_history(action=action_history,
                                                       type=type_history,
                                                       name=name_history,
                                                       date=datetime.now(),
                                                       user=user,
                                                       printer_id=printer.id,
                                                       status=action_history,
                                                       location=printer.location_now,
                                                       learning_campus=printer.learning_campus_now,
                                                       cabinet=printer.cabinet_now)
                    if request_redirect is not None:
                        return request_redirect

                    new_work_done = printer.work_done + 1
                    model_controller.update(model_entry=printer,
                                            work_done=new_work_done)

                return try_to_commit(redirect_to='printer_urls.reception_from_a_repairing')

            flash(f'Не верная идентификация формы!')
            return redirect(url_for('main_urls.main_page'))

        flash(f'Не определён метод запроса!')
        return redirect(url_for('main_urls.main_page'))

    @staticmethod
    @printer_urls.route('/issuance_printers', methods=['GET', 'POST'])
    @login_required
    def issuance_printers():
        if request.method == "GET":
            printers = model_controller.filter_by_model(model_name="Printer",
                                                        mode="all",
                                                        efficiency=1)
            printers_data = []
            for printer in printers:
                all_history = model_controller.filter_by_model(model_name='AllHistory',
                                                               mode='all',
                                                               printer_id=printer.id)
                last_history = all_history[-1]
                printers_data.append([printer, last_history])

            buildings = model_controller.get_all_entries(model_name="Buildings")
            divisions = model_controller.get_all_entries(model_name="Division")
            return render_template('Printer_urls/IssuancePrinters.html',
                                   printers_data=printers_data,
                                   buildings=buildings,
                                   divisions=divisions,
                                   StatusSettings=StatusSettings)

        if request.method == "POST":
            printer_num = request.form.getlist('num_inventory')
            id_form = request.form['id_form']
            user = current_user.username

            if len(printer_num) == 0:
                flash('Не выбрана ни одна модель')
                return redirect(url_for('printer_urls.issuance_printers'))

            if id_form == "1":
                location = request.form[f'location'].strip()
                learning_campus = request.form[f'learning_campus'].strip()
                cabinet = request.form[f'cabinet'].strip()

                action_history = StatusSettings.Cartridge.in_division
                type_history = StatusSettings.Types.cartridge

                for number in printer_num:
                    printer = model_controller.filter_by_model(model_name="Printer",
                                                               mode="first",
                                                               num_inventory=number)
                    model_controller.update(model_entry=printer,
                                            location_now=location,
                                            learning_campus_now=learning_campus,
                                            cabinet_now=cabinet)
                    name_history = number

                    request_redirect = save_in_history(action=action_history,
                                                       type=type_history,
                                                       name=name_history,
                                                       date=datetime.now(),
                                                       user=user,
                                                       printer_id=printer.id,
                                                       status=action_history,
                                                       location=printer.location_now,
                                                       learning_campus=printer.learning_campus_now,
                                                       cabinet=printer.cabinet_now)
                    if request_redirect is not None:
                        return request_redirect

                return try_to_commit(redirect_to='printer_urls.issuance_printers')

            if id_form == "2":
                action_history = StatusSettings.Cartridge.in_division
                type_history = StatusSettings.Types.cartridge

                for number in printer_num:
                    location = request.form[f'location{number}'].strip()
                    learning_campus = request.form[f'learning_campus{number}'].strip()
                    cabinet = request.form[f'cabinet{number}'].strip()
                    printer = model_controller.filter_by_model(model_name="Printer",
                                                               mode="first",
                                                               num_inventory=number)

                    model_controller.update(model_entry=printer,
                                            location_now=location,
                                            learning_campus_now=learning_campus,
                                            cabinet_now=cabinet)

                    name_history = number

                    request_redirect = save_in_history(action=action_history,
                                                       type=type_history,
                                                       name=name_history,
                                                       date=datetime.now(),
                                                       user=user,
                                                       printer_id=printer.id,
                                                       status=action_history,
                                                       location=printer.location_now,
                                                       learning_campus=printer.learning_campus_now,
                                                       cabinet=printer.cabinet_now)
                    if request_redirect is not None:
                        return request_redirect

                return try_to_commit(redirect_to='printer_urls.issuance_printers')

            flash(f'Не верная идентификация формы!')
            return redirect(url_for('main_urls.main_page'))

        flash(f'Не определён метод запроса!')
        return redirect(url_for('main_urls.main_page'))
