from flask import render_template
from flask import url_for
from flask import redirect
from flask import request
from flask import flash
from flask_login import current_user
from flask_login import login_required
from datetime import datetime

from Controller.SupportFunctions import prevent_valid, try_to_commit, save_in_history
from Settings.StatusSettings import StatusSettings
from Model.ModelController import get_current_model_controller

from Settings.Blueprint import CartridgeBlueprint

blueprint = CartridgeBlueprint()
cartridge_urls = blueprint.get_url()

# Управление базой данных
model_controller = get_current_model_controller()


class CartridgeURLs:
    @staticmethod
    @cartridge_urls.route('/add_works_cartridges', methods=['GET', 'POST'])
    @login_required
    def add_works_cartridges():
        if not current_user.is_boss and not current_user.is_admin:
            return redirect(url_for('main_urls.main_page'))

        if request.method == "GET":
            all_works_cartridges = model_controller.get_all_entries(model_name='AllWorksCartridges')
            counter_works = len(all_works_cartridges)
            return render_template("Cartridge_urls/AddWorksCartridges.html",
                                   all_works_cartridges=all_works_cartridges,
                                   counter_works=counter_works)

        if request.method == "POST":
            all_works_cartridges = request.form.getlist('works')

            if len(all_works_cartridges) == 0:
                flash('Нельзя удалить все модели', 'warning')
                return redirect(url_for('cartridge_urls.add_works_cartridges'))

            model_controller.delete_all_entries_in_model(model_name="AllWorksCartridges")

            try:
                for work in all_works_cartridges:
                    work = work.strip()
                    is_not_available = model_controller.filter_by_model(model_name="AllWorksCartridges",
                                                                        mode="first",
                                                                        work=work) is None
                    if work != '' and is_not_available:
                        model = model_controller.create(model_name="AllWorksCartridges",
                                                        work=work)
                        model_controller.add_in_session(model)
            except Exception as e:
                flash(f'Не удалось сохранить изменения. Ошибка: {e}', 'error')
                return redirect(url_for('main_urls.main_page'))

            return try_to_commit(redirect_to='cartridge_urls.add_works_cartridges')

        flash(f'Не определён метод запроса!', 'error')
        return redirect(url_for('main_urls.main_page'))

    @staticmethod
    @cartridge_urls.route('/add_models_cartridge', methods=['GET', 'POST'])
    @login_required
    def add_models_cartridge():
        if request.method == "GET":
            list_models = model_controller.get_all_entries(model_name='ListModels')
            counter_models = len(list_models)
            return render_template("Cartridge_urls/AddModels.html",
                                   list_models=list_models,
                                   counter_models=counter_models)

        if request.method == "POST":
            list_models = request.form.getlist('model')

            if len(list_models) == 0:
                flash('Нельзя удалить все модели', 'warning')
                return redirect(url_for('cartridge_urls.add_models_cartridge'))

            model_controller.delete_all_entries_in_model(model_name="ListModels")
            try:
                for model in list_models:
                    model = model.strip()
                    is_not_available = model_controller.filter_by_model(model_name='ListModels',
                                                                        mode='first',
                                                                        model=model) is None
                    if model != '' and not model.isspace() and is_not_available:
                        model = model_controller.create(model_name='ListModels',
                                                        model=model)
                        model_controller.add_in_session(model_entry=model)
            except Exception as e:
                flash(f'Не удалось сохранить изменения. Ошибка: {e}', 'error')
                return redirect(url_for('main_urls.main_page'))

            return try_to_commit(redirect_to='cartridge_urls.add_models_cartridge')

        flash(f'Не определён метод запроса!', 'error')
        return redirect(url_for('main_urls.main_page'))

    @staticmethod
    @cartridge_urls.route('/cartridge/<int:pk>/update', methods=['GET', 'POST'])
    @login_required
    def update_cartridge(pk):
        if request.method == "GET":
            cartridge = model_controller.get_model_by_id(model_name='Cartridges',
                                                         pk=pk)
            list_models = model_controller.get_all_entries(model_name='ListModels')
            counter_models = len(cartridge.cartridge_models)

            return render_template("Cartridge_urls/cartridge_update.html",
                                   cartridge=cartridge,
                                   list_models=list_models,
                                   counter_models=counter_models)

        if request.method == "POST":
            cartridge = model_controller.get_model_by_id(model_name='Cartridges',
                                                         pk=pk)
            cartridge_models = request.form.getlist('model')
            number = request.form['number'].strip()

            number = prevent_valid(var_type='int',
                                   variables=number)
            if type(number) is not int:
                return number

            if number != cartridge.number:
                is_numer_exist = model_controller.filter_by_model(model_name="Cartridges",
                                                                  mode="first",
                                                                  number=number) is not None
                if is_numer_exist:
                    flash('Такой номер уже есть', 'warning')
                    return redirect(url_for('cartridge_urls.update_cartridge', pk=cartridge.id))
                else:
                    model_controller.update(model_entry=cartridge,
                                            number=number)

            cartridge_models_list = []
            for model in cartridge_models:
                model = model.strip()
                if model != "":
                    model = model_controller.filter_by_model(model_name='ListModels',
                                                             mode='first',
                                                             model=model)
                    cartridge_models_list.append(model)
            model_controller.update(model_entry=cartridge,
                                    cartridge_models=cartridge_models_list)

            action_history = StatusSettings.Cartridge.updated
            type_history = StatusSettings.Types.cartridge
            name_history = cartridge.number
            user = current_user.username
            all_history = model_controller.filter_by_model(model_name='AllHistory',
                                                           mode='all',
                                                           cartridge_id=cartridge.id)
            all_history.sort(key=lambda ah: ah.date,
                             reverse=True)
            last_all_history = all_history[-1]
            for entry in all_history:
                if entry.status is not None:
                    last_all_history = entry
                    break
            request_redirect = save_in_history(action=action_history,
                                               type=type_history,
                                               name=name_history,
                                               date=datetime.now(),
                                               user=user,
                                               cartridge_id=cartridge.id,
                                               status=last_all_history.status,
                                               location=last_all_history.location,
                                               learning_campus=last_all_history.learning_campus,
                                               cabinet=last_all_history.cabinet)
            if request_redirect is not None:
                return request_redirect

            return try_to_commit(redirect_to='cartridge_urls.cartridges')

        flash(f'Не определён метод запроса!', 'error')
        return redirect(url_for('main_urls.main_page'))

    @staticmethod
    @cartridge_urls.route('/cartridge/<int:pk>/statuses')
    @login_required
    def cartridge_status(pk):
        if request.method == "GET":
            statuses = model_controller.filter_by_model(model_name='AllHistory',
                                                        mode='all',
                                                        cartridge_id=pk)
            statuses.sort(key=lambda all_history: all_history.date,
                          reverse=True)
            cartridge = model_controller.get_model_by_id(model_name='Cartridges',
                                                         pk=pk)
            users = model_controller.get_all_entries(model_name="User")
            return render_template("Cartridge_urls/CartridgeStatuses.html",
                                   statuses=statuses,
                                   cartridge=cartridge,
                                   StatusSettings=StatusSettings,
                                   users=users)

        flash(f'Не определён метод запроса!', 'error')
        return redirect(url_for('main_urls.main_page'))

    @staticmethod
    @cartridge_urls.route('/cartridges/', methods=['GET', 'POST'], defaults={'is_show_own': 1})
    @cartridge_urls.route('/cartridges/show=<int:is_show_own>', methods=['GET', 'POST'])
    @login_required
    def cartridges(is_show_own=1):
        if request.method == 'GET':
            list_models = model_controller.get_all_entries(model_name='ListModels')
            cartridges = model_controller.get_all_entries(model_name='Cartridges')

            # Выборка нужных статусов через метод __dict__
            all_statuses = dict(StatusSettings.Cartridge.__dict__)
            del all_statuses['__module__']
            del all_statuses['__dict__']
            del all_statuses['__weakref__']
            del all_statuses['__doc__']
            del all_statuses['restored']
            del all_statuses['deleted']
            del all_statuses['updated']
            del all_statuses['in_division']
            del all_statuses['in_refueling']

            is_not_find = False
            if len(cartridges) == 0:
                new_cartridge_number = 1
                cartridges_info = None
            else:
                cartridges.sort(key=lambda c: c.date_added,
                                reverse=True)

                buildings = current_user.buildings_id
                current_buildings = []
                for building in buildings:
                    current_buildings.append(building.building)

                cartridges_info = []
                if is_show_own and current_buildings:
                    amount_finding = 0
                    for cartridge in cartridges:
                        all_history = model_controller.filter_by_model(model_name='AllHistory',
                                                                       mode='all',
                                                                       cartridge_id=cartridge.id)
                        all_history.sort(key=lambda ah: ah.date,
                                         reverse=True)
                        learning_campus = None
                        for history in all_history:
                            if history.learning_campus is not None:
                                learning_campus = history.learning_campus
                                break

                        if learning_campus is None:
                            continue

                        if learning_campus in current_buildings:
                            amount_finding += 1
                            # status
                            status = all_history[0].status

                            # location
                            location = model_controller.filter_by_model(model_name='AllHistory',
                                                                        mode='all',
                                                                        cartridge_id=cartridge.id)

                            location = location[0] if len(location) == 1 else location[-1]

                            # printer
                            printer = model_controller.filter_by_model(model_name='Printer',
                                                                       mode='first',
                                                                       id=location.printer_id)
                            # add all vars
                            cartridges_info.append([cartridge, location, status, printer])

                    if amount_finding == 0:
                        is_not_find = True
                else:
                    for cartridge in cartridges:
                        # location
                        location = model_controller.filter_by_model(model_name='AllHistory',
                                                                    mode='all',
                                                                    cartridge_id=cartridge.id)

                        location = location[0] if len(location) == 1 else location[-1]
                        # status
                        all_history = model_controller.filter_by_model(model_name='AllHistory',
                                                                       mode='all',
                                                                       cartridge_id=cartridge.id)
                        all_history.sort(key=lambda ah: ah.date)
                        status = all_history[-1].status
                        # printer
                        printer = model_controller.filter_by_model(model_name='Printer',
                                                                   mode='first',
                                                                   id=location.printer_id)
                        # add all vars
                        cartridges_info.append([cartridge, location, status, printer])

                cartridges_info.sort(key=lambda c: c[0].number,
                                     reverse=True)
                new_cartridge_number = max([cartridge.number for cartridge in cartridges]) + 1

            return render_template("Cartridge_urls/Cartridges.html",
                                   cartridges_info=cartridges_info,
                                   list_models=list_models,
                                   StatusSettings=StatusSettings,
                                   new_cartridge_number=new_cartridge_number,
                                   all_statuses=all_statuses,
                                   is_show_own=is_show_own,
                                   is_not_find=is_not_find)

        if request.method == 'POST':
            status = request.form['status'].strip()
            number = request.form['number'].strip()
            cartridge_models = request.form.getlist('model')

            number = prevent_valid(var_type='int',
                                   variables=number)
            if type(number) is not int:
                return number

            if len(cartridge_models) == 0:
                flash('Не выбрана ни одна модель', 'warning')
                return redirect(url_for('cartridge_urls.cartridges'))

            is_number_exist = model_controller.filter_by_model(model_name='Cartridges',
                                                               mode='first',
                                                               number=number)
            if is_number_exist:
                flash('Такой номер уже есть', 'warning')
                return redirect(url_for('cartridge_urls.cartridges'))

            cartridge = model_controller.create(model_name='cartridges',
                                                number=number,
                                                date_added=datetime.now())

            models = []
            for model in cartridge_models:
                model = model.strip()
                model = model_controller.filter_by_model(model_name='ListModels',
                                                         mode='first',
                                                         model=model)
                models.append(model)
            model_controller.update(model_entry=cartridge,
                                    cartridge_models=models)

            action_history = StatusSettings.Cartridge.created
            type_history = StatusSettings.Types.cartridge
            name_history = number
            user = current_user.username
            if status == StatusSettings.Cartridge.created:
                status = StatusSettings.Cartridge.in_reserve
            request_redirect = save_in_history(action=action_history,
                                               type=type_history,
                                               name=name_history,
                                               date=datetime.now(),
                                               user=user,
                                               cartridge_id=cartridge.id,
                                               status=status)
            if request_redirect is not None:
                return request_redirect

            return try_to_commit(redirect_to='cartridge_urls.cartridges')

        flash(f'Не определён метод запроса!', 'error')
        return redirect(url_for('main_urls.main_page'))

    @staticmethod
    @cartridge_urls.route('/cartridge/<int:pk>/delete')
    @login_required
    def delete_cartridge(pk):
        if request.method == "GET":
            cartridge = model_controller.get_model_by_id(model_name='Cartridges',
                                                         pk=pk)
            if not cartridge.efficiency:
                flash("Картридж и так находится в утиле", "error")
                return redirect(url_for('main_urls.main_page'))
            try:
                action_history = StatusSettings.Cartridge.deleted
                type_history = StatusSettings.Types.cartridge
                name_history = cartridge.number
                user = current_user.username
                last_all_history = model_controller.filter_by_model(model_name='AllHistory',
                                                                    mode='all',
                                                                    cartridge_id=cartridge.id)[-1]
                request_redirect = save_in_history(action=action_history,
                                                   type=type_history,
                                                   name=name_history,
                                                   date=datetime.now(),
                                                   user=user,
                                                   cartridge_id=cartridge.id,
                                                   status=last_all_history.status,
                                                   location=last_all_history.location,
                                                   learning_campus=last_all_history.learning_campus,
                                                   cabinet=last_all_history.cabinet)
                if request_redirect is not None:
                    return request_redirect

                model_controller.update(model_entry=cartridge,
                                        efficiency=0)
                return try_to_commit(redirect_to='cartridge_urls.cartridges')
            except Exception as e:
                flash(f'Ошибка удаления картриджа. Ошибка: {e}', 'error')
                return redirect(url_for('main_urls.main_page'))

        flash(f'Не определён метод запроса!', 'error')
        return redirect(url_for('main_urls.main_page'))

    @staticmethod
    @cartridge_urls.route('/cartridge/<int:pk>/resume')
    @login_required
    def resume_cartridge(pk):
        if request.method == "GET":
            cartridge = model_controller.get_model_by_id(model_name='Cartridges',
                                                         pk=pk)
            if cartridge.efficiency:
                flash("Картридж не был утилизирован", "error")
                return redirect(url_for('main_urls.main_page'))
            try:
                action_history = StatusSettings.Cartridge.restored
                type_history = StatusSettings.Types.cartridge
                name_history = cartridge.number
                user = current_user.username
                last_all_history = model_controller.filter_by_model(model_name='AllHistory',
                                                                    mode='all',
                                                                    cartridge_id=cartridge.id)[-2]

                request_redirect = save_in_history(action=action_history,
                                                   type=type_history,
                                                   name=name_history,
                                                   date=datetime.now(),
                                                   user=user,
                                                   cartridge_id=cartridge.id,
                                                   status=last_all_history.status,
                                                   location=last_all_history.location,
                                                   learning_campus=last_all_history.learning_campus,
                                                   cabinet=last_all_history.cabinet)
                if request_redirect is not None:
                    return request_redirect

                model_controller.update(model_entry=cartridge,
                                        efficiency=1)

                return try_to_commit(redirect_to='cartridge_urls.deleted_cartridges')
            except Exception as e:
                flash(f'Ошибка восстановления картриджа. Ошибка: {e}', 'error')
                return redirect(url_for('main_urls.main_page'))

        flash(f'Не определён метод запроса!', 'error')
        return redirect(url_for('main_urls.main_page'))

    @staticmethod
    @cartridge_urls.route('/deleted_cartridges')
    @login_required
    def deleted_cartridges():
        if request.method == "GET":
            cartridges = model_controller.get_all_entries(model_name='Cartridges')
            return render_template('Cartridge_urls/DeletedCartridges.html',
                                   cartridges=cartridges)

        flash(f'Не определён метод запроса!', 'error')
        return redirect(url_for('main_urls.main_page'))

    @staticmethod
    @cartridge_urls.route('/brought_a_cartridge', methods=['GET', 'POST'])
    @login_required
    def brought_a_cartridge():
        if request.method == "GET":
            cartridges = model_controller.filter_by_model(model_name='Cartridges',
                                                          mode="all",
                                                          efficiency=1)
            printers = model_controller.get_all_entries(model_name='Printer')
            buildings = model_controller.get_all_entries(model_name='Buildings')
            divisions = model_controller.get_all_entries(model_name='Division')

            cartridges_info = []
            for cartridge in cartridges:
                # all history
                all_history = model_controller.filter_by_model(model_name='AllHistory',
                                                               mode='all',
                                                               cartridge_id=cartridge.id)
                # status
                status = all_history[-1].status

                # printer
                printer = model_controller.filter_by_model(model_name='Printer',
                                                           mode='first',
                                                           id=all_history[-1].printer_id)

                # add info
                cartridges_info.append([cartridge, status, printer, all_history])

            printers_info = []
            for printer in printers:
                printers_info.append({
                    "id": str(printer.id),
                    "location_now": printer.location_now,
                    "learning_campus_now": printer.learning_campus_now,
                    "cabinet_now": printer.cabinet_now,
                    "name": printer.name,
                    "num_inventory": printer.num_inventory
                })

            return render_template('Cartridge_urls/BroughtACartridge.html',
                                   cartridges_info=cartridges_info,
                                   printers=printers,
                                   buildings=buildings,
                                   divisions=divisions,
                                   StatusSettings=StatusSettings,
                                   printers_info=printers_info)

        if request.method == "POST":
            cartridge_number = request.form.getlist('cartridge_number')
            id_form = request.form['id_form'].strip()
            user = current_user.username

            if len(cartridge_number) == 0:
                flash('Не выбрана ни одна модель', 'warning')
                return redirect(url_for('cartridge_urls.brought_a_cartridge'))

            if id_form == "1":
                location = request.form['location'].strip()
                learning_campus = request.form['learning_campus'].strip()
                cabinet = request.form['cabinet'].strip()
                printer_id = request.form['printer_id'].strip()
                printer = model_controller.filter_by_model(model_name='Printer',
                                                           mode='first',
                                                           id=printer_id)

                site = [location, learning_campus, cabinet]
                site = prevent_valid(var_type='str',
                                     variables=site)
                if type(site) is not list:
                    return site
                location, learning_campus, cabinet = site

                action_status_history = StatusSettings.Cartridge.accepted_for_refuel
                type_history = StatusSettings.Types.cartridge
                for number in cartridge_number:
                    number = number.strip()
                    cartridge = model_controller.filter_by_model(model_name='Cartridges',
                                                                 mode='first',
                                                                 number=number)
                    name_history = number
                    request_redirect = save_in_history(action=action_status_history,
                                                       type=type_history,
                                                       name=name_history,
                                                       date=datetime.now(),
                                                       user=user,
                                                       cartridge_id=cartridge.id,
                                                       printer_id=printer.id,
                                                       status=action_status_history,
                                                       location=location,
                                                       learning_campus=learning_campus,
                                                       cabinet=cabinet)
                    if request_redirect is not None:
                        return request_redirect

                return try_to_commit(redirect_to='cartridge_urls.cartridges')

            if id_form == "2":
                print(cartridge_number)
                for number in cartridge_number:
                    number = number.strip()
                    print(number)
                    location = request.form[f'location{number}'].strip()
                    learning_campus = request.form[f'learning_campus{number}'].strip()
                    cabinet = request.form[f'cabinet{number}'].strip()
                    printer_id = request.form[f'printer_id{number}'].strip()
                    printer = model_controller.filter_by_model(model_name='Printer',
                                                               mode='first',
                                                               id=printer_id)
                    cartridge = model_controller.filter_by_model(model_name='Cartridges',
                                                                 mode='first',
                                                                 number=number)

                    action_status_history = StatusSettings.Cartridge.accepted_for_refuel
                    type_history = StatusSettings.Types.cartridge
                    name_history = number
                    request_redirect = save_in_history(action=action_status_history,
                                                       type=type_history,
                                                       name=name_history,
                                                       date=datetime.now(),
                                                       user=user,
                                                       cartridge_id=cartridge.id,
                                                       printer_id=printer.id,
                                                       status=action_status_history,
                                                       location=location,
                                                       learning_campus=learning_campus,
                                                       cabinet=cabinet)
                    if request_redirect is not None:
                        return request_redirect

                return try_to_commit(redirect_to='cartridge_urls.cartridges')

            flash(f'Не верная идентификация формы!', 'error')
            return redirect(url_for('main_urls.main_page'))

        flash(f'Не определён метод запроса!', 'error')
        return redirect(url_for('main_urls.main_page'))

    @staticmethod
    @cartridge_urls.route('/refueling', methods=['GET', 'POST'])
    @login_required
    def refueling():
        if request.method == "GET":
            cartridges = model_controller.filter_by_model(model_name='Cartridges',
                                                          mode="all",
                                                          efficiency=1)

            cartridges_info = []
            for cartridge in cartridges:
                # status
                all_history = model_controller.filter_by_model(model_name='AllHistory',
                                                               mode='all',
                                                               cartridge_id=cartridge.id)
                status = all_history[-1].status

                # TODO: Динамическое изменение limit_refills_not_including, в зависимости от среднего показателя
                #  количества заправок картриджа по производителю
                limit_refills_not_including = 3

                is_refills_left = True if cartridge.refills > limit_refills_not_including else False
                cartridges_info.append([cartridge, status, is_refills_left, limit_refills_not_including])
            return render_template('Cartridge_urls/Refueling.html',
                                   cartridges_info=cartridges_info,
                                   StatusSettings=StatusSettings)

        if request.method == "POST":
            cartridge_number = request.form.getlist('cartridge_number')
            user = current_user.username

            if len(cartridge_number) == 0:
                flash('Не выбрана ни одна модель', 'warning')
                return redirect(url_for('cartridge_urls.refueling'))

            for number in cartridge_number:
                number = number.strip()
                cartridge = model_controller.filter_by_model(model_name='Cartridges',
                                                             mode='first',
                                                             number=number)

                # TODO: Добавить возможность заправить картридж даже если он уже был заправлен более 4 раз,
                #  но с предупреждением
                if cartridge.refills > 3:
                    flash(f"Картридж №{cartridge.number} был заправлен более 4 раз. Его следует утилизировать.",
                          'warning')
                    return redirect(url_for('cartridge_urls.refueling'))

            for number in cartridge_number:
                number = number.strip()
                cartridge = model_controller.filter_by_model(model_name='Cartridges',
                                                             mode='first',
                                                             number=number)

                # TODO: избавиться от таблицы 'Refueling' и перенести все данные в таблицу 'AllHistory'
                refueling = model_controller.create(model_name='Refueling',
                                                    user=user,
                                                    date=datetime.now(),
                                                    cartridge_number_id=cartridge.id)
                model_controller.add_in_session(model_entry=refueling)

                action_status_history = StatusSettings.Cartridge.in_refueling
                type_history = StatusSettings.Types.cartridge
                name_history = cartridge.number
                last_all_history = model_controller.filter_by_model(model_name='AllHistory',
                                                                    mode='all',
                                                                    cartridge_id=cartridge.id)[-1]
                request_redirect = save_in_history(action=action_status_history,
                                                   type=type_history,
                                                   name=name_history,
                                                   date=datetime.now(),
                                                   user=user,
                                                   cartridge_id=cartridge.id,
                                                   status=action_status_history,
                                                   location=last_all_history.location,
                                                   learning_campus=last_all_history.learning_campus,
                                                   cabinet=last_all_history.cabinet)
                if request_redirect is not None:
                    return request_redirect

            return try_to_commit(redirect_to='cartridge_urls.cartridges')

        flash(f'Не определён метод запроса!', 'error')
        return redirect(url_for('main_urls.main_page'))

    @staticmethod
    @cartridge_urls.route('/reception_from_a_refuelling', methods=['GET', 'POST'])
    @login_required
    def reception_from_a_refuelling():
        if request.method == "GET":
            cartridges = model_controller.filter_by_model(model_name='Cartridges',
                                                          mode="all",
                                                          efficiency=1)

            cartridges_info = []
            for cartridge in cartridges:
                # status
                all_history = model_controller.filter_by_model(model_name='AllHistory',
                                                               mode='all',
                                                               cartridge_id=cartridge.id)
                status = all_history[-1].status
                cartridges_info.append([cartridge, status])
            return render_template('Cartridge_urls/ReceptionFromARefuelling.html',
                                   cartridges_info=cartridges_info,
                                   StatusSettings=StatusSettings)

        if request.method == "POST":
            cartridge_number = request.form.getlist('cartridge_number')
            user = current_user.username

            if len(cartridge_number) == 0:
                flash('Не выбрана ни одна модель', 'warning')
                return redirect(url_for('cartridge_urls.reception_from_a_refuelling'))

            for number in cartridge_number:
                number = number.strip()
                cartridge = model_controller.filter_by_model(model_name='Cartridges',
                                                             mode='first',
                                                             number=number)

                # TODO: избавиться от таблицы 'ReceptionFromARefueling' и перенести все данные в таблицу 'AllHistory'
                reception_from_a_refueling = model_controller.create(model_name='ReceptionFromARefueling',
                                                                     user=user,
                                                                     date=datetime.now(),
                                                                     cartridge_number_id=cartridge.id)
                model_controller.add_in_session(model_entry=reception_from_a_refueling)

                action_status_history = StatusSettings.Cartridge.in_reserve
                type_history = StatusSettings.Types.cartridge
                name_history = cartridge.number
                last_all_history = model_controller.filter_by_model(model_name='AllHistory',
                                                                    mode='all',
                                                                    cartridge_id=cartridge.id)[-1]
                request_redirect = save_in_history(action=action_status_history,
                                                   type=type_history,
                                                   name=name_history,
                                                   date=datetime.now(),
                                                   user=user,
                                                   cartridge_id=cartridge.id,
                                                   status=action_status_history,
                                                   location=last_all_history.location,
                                                   learning_campus=last_all_history.learning_campus,
                                                   cabinet=last_all_history.cabinet)
                if request_redirect is not None:
                    return request_redirect

                new_refills = cartridge.refills + 1
                new_work_done = cartridge.work_done + 1
                model_controller.update(model_entry=cartridge,
                                        refills=new_refills,
                                        work_done=new_work_done)

            return try_to_commit(redirect_to='cartridge_urls.cartridges')

        flash(f'Не определён метод запроса!', 'error')
        return redirect(url_for('main_urls.main_page'))

    @staticmethod
    @cartridge_urls.route('/issuance_cartridges', methods=['GET', 'POST'])
    @login_required
    def issuance_cartridges():
        if request.method == "GET":
            cartridges = model_controller.filter_by_model(model_name='Cartridges',
                                                          mode="all",
                                                          efficiency=1)
            printers = model_controller.get_all_entries(model_name='Printer')
            buildings = model_controller.get_all_entries(model_name='Buildings')
            divisions = model_controller.get_all_entries(model_name='Division')

            cartridges_info = []
            for cartridge in cartridges:
                # all history
                all_history = model_controller.filter_by_model(model_name='AllHistory',
                                                               mode='all',
                                                               cartridge_id=cartridge.id)
                sorted_all_history = []
                for history in all_history:
                    if history.printer_id is not None:
                        sorted_all_history.append(history)

                if not sorted_all_history:
                    # status
                    status = all_history[-1].status

                    # printer
                    printer = model_controller.filter_by_model(model_name='Printer',
                                                               mode='first',
                                                               id=all_history[-1].printer_id)

                    sorted_all_history = all_history
                else:
                    # status
                    status = all_history[-1].status

                    # printer
                    printer = model_controller.filter_by_model(model_name='Printer',
                                                               mode='first',
                                                               id=sorted_all_history[-1].printer_id)

                # add info
                cartridges_info.append([cartridge, status, printer, sorted_all_history])

            printers_info = []
            for printer in printers:
                printers_info.append({
                    "id": str(printer.id),
                    "location_now": printer.location_now,
                    "learning_campus_now": printer.learning_campus_now,
                    "cabinet_now": printer.cabinet_now,
                    "name": printer.name,
                    "num_inventory": printer.num_inventory
                })

            return render_template('Cartridge_urls/IssuanceCartridges.html',
                                   cartridges_info=cartridges_info,
                                   printers=printers,
                                   buildings=buildings,
                                   divisions=divisions,
                                   StatusSettings=StatusSettings,
                                   printers_info=printers_info)

        if request.method == "POST":
            cartridge_number = request.form.getlist('cartridge_number')
            id_form = request.form['id_form'].strip()
            user = current_user.username

            if len(cartridge_number) == 0:
                flash('Не выбрана ни одна модель', 'warning')
                return redirect(request.referrer)

            if id_form == "1":
                location = request.form['location'].strip()
                learning_campus = request.form['learning_campus'].strip()
                cabinet = request.form['cabinet'].strip()
                printer_id = request.form['printer_id'].strip()
                printer = model_controller.filter_by_model(model_name='Printer',
                                                           mode='first',
                                                           id=printer_id)

                site = [location, learning_campus, cabinet]
                site = prevent_valid(var_type='str',
                                     variables=site)
                if type(site) is not list:
                    return site
                location, learning_campus, cabinet = site

                action_status_history = StatusSettings.Cartridge.in_division
                type_history = StatusSettings.Types.cartridge
                for number in cartridge_number:
                    number = number.strip()
                    cartridge = model_controller.filter_by_model(model_name='Cartridges',
                                                                 mode='first',
                                                                 number=number)
                    name_history = number
                    request_redirect = save_in_history(action=action_status_history,
                                                       type=type_history,
                                                       name=name_history,
                                                       date=datetime.now(),
                                                       user=user,
                                                       cartridge_id=cartridge.id,
                                                       printer_id=printer.id,
                                                       status=action_status_history,
                                                       location=location,
                                                       learning_campus=learning_campus,
                                                       cabinet=cabinet)
                    if request_redirect is not None:
                        return request_redirect

                return try_to_commit(redirect_to='cartridge_urls.cartridges')

            if id_form == "2":
                for number in cartridge_number:
                    number = number.strip()
                    location = request.form[f'location{number}'].strip()
                    learning_campus = request.form[f'learning_campus{number}'].strip()
                    cabinet = request.form[f'cabinet{number}'].strip()
                    printer_id = request.form[f'printer{number}'].strip()
                    printer = model_controller.filter_by_model(model_name='Printer',
                                                               mode='first',
                                                               id=printer_id)
                    cartridge = model_controller.filter_by_model(model_name='Cartridges',
                                                                 mode='first',
                                                                 number=number)

                    action_status_history = StatusSettings.Cartridge.in_division
                    type_history = StatusSettings.Types.cartridge
                    name_history = number
                    request_redirect = save_in_history(action=action_status_history,
                                                       type=type_history,
                                                       name=name_history,
                                                       date=datetime.now(),
                                                       user=user,
                                                       cartridge_id=cartridge.id,
                                                       printer_id=printer.id,
                                                       status=action_status_history,
                                                       location=location,
                                                       learning_campus=learning_campus,
                                                       cabinet=cabinet)
                    if request_redirect is not None:
                        return request_redirect

                return try_to_commit(redirect_to='cartridge_urls.cartridges')

            flash(f'Не верная идентификация формы!', 'error')
            return redirect(url_for('main_urls.main_page'))

        flash(f'Не определён метод запроса!', 'error')
        return redirect(url_for('main_urls.main_page'))
