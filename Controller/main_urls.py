import json

from flask import render_template, url_for
from flask import request
from flask import redirect
from flask import flash
from flask_login import login_required, current_user
from datetime import datetime

from Controller.SupportFunctions import prevent_valid
from Controller.SupportFunctions import try_to_commit
from Controller.SupportFunctions import save_in_history
from Controller.SupportFunctions import all_checks_is_active
from Controller.SupportFunctions import get_contract_price
from Controller.SupportFunctions import get_check_price
from Controller.SupportFunctions import get_entries_for_work_list_cartridges
from Controller.SupportFunctions import get_entries_for_work_list_printers
from Controller.SupportFunctions import get_work_done_price

from Controller.CreateCharts import create_chart
from Controller.CreateCharts import created_deleted_chart
from Controller.CreateCharts import refill_cycle_chart

from Model.ModelController import ModelController
from Settings.StatusSettings import StatusSettings
from Settings.Blueprint import MainBlueprint

blueprint = MainBlueprint()
main_urls = blueprint.get_url()

# Управление базой данных
model_controller = ModelController()


class MainURLs:
    @staticmethod
    @main_urls.route('/get-charts-api/', defaults={'col_amount': 6})
    @main_urls.route('/get-charts-api/cols=<int:col_amount>')
    def get_charts_api(col_amount=6):
        # TODO: Создать API ключи. Отдельная таблица в БД с зашифрованными ключами.
        #  Генерирует только босс. Нужен для стороннего доступа к графикам
        pie_chart_data = create_chart()
        c_d_chat = created_deleted_chart(col_amount)
        r_c_chart = refill_cycle_chart(col_amount)
        charts = {
            "pie_chart_data": pie_chart_data,
            "created_deleted_chart": c_d_chat,
            "refill_cycle_chart": r_c_chart
        }
        json_charts = json.dumps(charts)
        return json.loads(json_charts)

    @staticmethod
    @main_urls.route('/', defaults={'is_show_charts': 0})
    @main_urls.route('/show=<int:is_show_charts>/cols=<int:col_amount>')
    def main_page(is_show_charts=0, col_amount=6):
        if request.method == "GET":
            if is_show_charts and current_user.is_authenticated:
                pie_chart_data = create_chart()
                c_d_chat = created_deleted_chart(col_amount)
                r_c_chart = refill_cycle_chart(col_amount)
            else:
                pie_chart_data = [0, 0, 0]
                c_d_chat = [0, 0, 0]
                r_c_chart = [0, 0]

            print(c_d_chat)

            return render_template("Main_urls/main.html",
                                   pie_chart_data=pie_chart_data,
                                   created_deleted_chart=c_d_chat,
                                   refill_cycle_chart=r_c_chart,
                                   is_show_charts=is_show_charts)

        flash(f'Не определён метод запроса!')
        return redirect(url_for('main_urls.main_page'))

    @staticmethod
    @main_urls.route('/divisions', methods=['GET', 'POST'])
    @login_required
    def add_divisions():
        if not current_user.is_boss:
            return redirect(url_for('main_urls.main_page'))

        if request.method == "GET":
            division_list = model_controller.get_all_entries(model_name="Division")
            counter_division = len(division_list)
            return render_template("Main_urls/Divisions.html",
                                   division_list=division_list,
                                   counter_division=counter_division)

        if request.method == "POST":
            list_division = request.form.getlist('division')

            list_division = prevent_valid(var_type='str',
                                          variables=list_division)
            if type(list_division) is not list:
                return list_division

            if len(list_division) == 0:
                flash('Нельзя удалить все подразделения')
                return redirect(url_for('main_urls.main_page'))

            model_controller.delete_all_entries_in_model(model_name="Division")
            try:
                for division in list_division:

                    is_not_available = model_controller.filter_by_model(model_name="Division",
                                                                        mode="first",
                                                                        division=division.strip()) is None
                    if division != '' and not division.isspace() and is_not_available:
                        division = model_controller.create(model_name="Division",
                                                           division=division)
                        model_controller.add_in_session(model_entry=division)
            except Exception as e:
                flash(f'Не удалось сохранить изменения. Ошибка: {e}')
                return redirect(url_for('main_urls.main_page'))

            return try_to_commit(redirect_to='main_urls.add_divisions')

        flash(f'Не определён метод запроса!')
        return redirect(url_for('main_urls.main_page'))

    @staticmethod
    @main_urls.route('/buildings', methods=['GET', 'POST'])
    @login_required
    def add_buildings():
        if not current_user.is_boss:
            return redirect(url_for('main_urls.main_page'))

        if request.method == "GET":
            building_list = model_controller.get_all_entries(model_name="Buildings")
            counter_building = len(building_list)
            return render_template("Main_urls/Buildings.html",
                                   building_list=building_list,
                                   counter_building=counter_building)

        if request.method == "POST":
            list_buildings = request.form.getlist('building')

            list_buildings = prevent_valid(var_type='str',
                                           variables=list_buildings)
            if type(list_buildings) is not list:
                return list_buildings

            if len(list_buildings) == 0:
                flash('Нельзя удалить все корпусы')
                return redirect(url_for('main_urls.main_page'))

            model_controller.delete_all_entries_in_model(model_name="Buildings")
            try:
                for building in list_buildings:
                    is_not_available = model_controller.filter_by_model(model_name="Buildings",
                                                                        mode='first',
                                                                        building=building.strip()) is None
                    if building != '' and not building.isspace() and is_not_available:
                        building = model_controller.create(model_name="Buildings",
                                                           building=building)
                        model_controller.add_in_session(building)
            except Exception as e:
                flash(f'Не удалось сохранить изменения. Ошибка: {e}')
                return redirect(url_for('main_urls.main_page'))

            return try_to_commit(redirect_to='main_urls.add_buildings')

        flash(f'Не определён метод запроса!')
        return redirect(url_for('main_urls.main_page'))

    @staticmethod
    @main_urls.route('/all_history', defaults={"page": 1, "is_show_paginate": 1}, methods=['GET', 'POST'])
    @main_urls.route('/all_history/page=<int:page>', defaults={"is_show_paginate": 1})
    @main_urls.route('/all_history/show=<int:is_show_paginate>', defaults={"page": 1})
    @login_required
    def all_history(page=1, is_show_paginate=1):
        if request.method == "GET":
            per_page = 75
            if current_user.is_boss:
                if is_show_paginate:
                    all_history = model_controller.get_all_entries_with_paginate(model_name="AllHistory",
                                                                                 page=page,
                                                                                 per_page=per_page)
                else:
                    all_history = model_controller.get_all_entries_with_order(model_name="AllHistory")
            else:
                if is_show_paginate:
                    all_history = model_controller.filter_two_or_with_paginate("AllHistory",
                                                                               page,
                                                                               per_page,
                                                                               "type",
                                                                               StatusSettings.Types.cartridge,
                                                                               StatusSettings.Types.printer)
                else:
                    all_history = model_controller.filter_two_or("AllHistory",
                                                                 "type",
                                                                 StatusSettings.Types.cartridge,
                                                                 StatusSettings.Types.printer)

            buildings = []
            locations = []
            actions = {}
            statuses = {}
            users = []
            entries_type = {}
            if current_user.is_boss or current_user.is_admin:
                buildings = model_controller.get_all_entries(model_name="Buildings")
                locations = model_controller.get_all_entries(model_name="Division")
                users = model_controller.get_all_entries(model_name="User")
                entries_type = dict(StatusSettings.Types.__dict__)
                del entries_type['__module__']
                del entries_type['__dict__']
                del entries_type['__weakref__']
                del entries_type['__doc__']

                statuses_list = [
                    dict(StatusSettings.Cartridge.__dict__),
                    dict(StatusSettings.Printer.__dict__),
                    dict(StatusSettings.Contract.__dict__),
                    dict(StatusSettings.Check.__dict__),
                    dict(StatusSettings.WorkList.__dict__),
                ]
                for status_list in statuses_list:
                    del status_list['__module__']
                    del status_list['__dict__']
                    del status_list['__weakref__']
                    del status_list['__doc__']

                    for name, value in status_list.items():
                        if name not in actions:
                            actions[name] = value

                for i in range(0, 2):
                    del statuses_list[i]['restored']
                    del statuses_list[i]['deleted']
                    del statuses_list[i]['updated']

                    for name, value in statuses_list[i].items():
                        if name not in statuses:
                            statuses[name] = value

            return render_template("Main_urls/AllHistory.html",
                                   all_history=all_history,
                                   StatusSettings=StatusSettings,
                                   is_show_paginate=is_show_paginate,
                                   buildings=buildings,
                                   locations=locations,
                                   statuses=statuses,
                                   actions=actions,
                                   users=users,
                                   entries_type=entries_type,
                                   page=page)

        if request.method == "POST":
            if current_user.is_boss or current_user.is_admin:
                action = request.form["action"].strip()
                entry_type = request.form["type"].strip()
                name = request.form["name"].strip()
                date = request.form["date"].strip()
                learning_campus = request.form["learning_campus"].strip()
                location = request.form["location"].strip()
                cabinet = request.form["cabinet"].strip()
                user = request.form["user"].strip()
                status = request.form["status"].strip()

                date = datetime.fromisoformat(f'{date}')

                all_history = model_controller.create(model_name="AllHistory",
                                                      action=action,
                                                      type=entry_type,
                                                      name=name,
                                                      date=date,
                                                      learning_campus=learning_campus,
                                                      location=location,
                                                      cabinet=cabinet,
                                                      user=user,
                                                      status=status)
                model_controller.add_in_session(all_history)
                return try_to_commit(redirect_to="main_urls.all_history")

            flash(f'У вас нет доступа к этому функционалу')
            return redirect(url_for('main_urls.main_page'))

        flash(f'Не определён метод запроса!')
        return redirect(url_for('main_urls.main_page'))

    @staticmethod
    @main_urls.route('/active_contract', methods=['GET', 'POST'])
    @login_required
    def active_contract():
        if not current_user.is_boss:
            return redirect(url_for('main_urls.main_page'))

        if request.method == "GET":
            list_of_contracts = model_controller.get_all_entries(model_name="ListsOfContracts")
            if len(list_of_contracts) > 0:
                last_contract = model_controller.filter_by_model(model_name="ListsOfContracts",
                                                                 mode="first",
                                                                 active=1)
            else:
                last_contract = None

            check_lists = model_controller.filter_by_model(model_name="CheckLists",
                                                           mode="all",
                                                           list_of_contracts_id=last_contract.id)

            all_checks_active = False
            contract_price = 0
            for contract in list_of_contracts:
                if contract.active:
                    all_checks_active = all_checks_is_active(last_contract)
                    contract_price = get_contract_price(last_contract)
                    break

            return render_template('Main_urls/WorkDone.html',
                                   last_contract=last_contract,
                                   check_lists=check_lists,
                                   all_checks_active=all_checks_active,
                                   contract_price=contract_price)

        if request.method == "POST":
            name = request.form['name']
            sum_contract = request.form['sum_contract']
            date_contract = request.form['date_contract']
            date_contract = datetime.fromisoformat(f'{date_contract}')

            contract = model_controller.create(model_name="ListsOfContracts",
                                               name=name,
                                               sum=sum_contract,
                                               date_contract=date_contract,
                                               active=True,
                                               date_create=datetime.now())

            model_controller.add_in_session(contract)

            action_history = StatusSettings.Contract.created
            type_history = StatusSettings.Types.contract
            user = current_user.username
            request_redirect = save_in_history(action=action_history,
                                               type=type_history,
                                               name=name,
                                               user=user,
                                               date=datetime.now())

            if request_redirect is not None:
                return request_redirect

            return try_to_commit(redirect_to='main_urls.active_contract')

        flash(f'Не определён метод запроса!')
        return redirect(url_for('main_urls.main_page'))

    @staticmethod
    @main_urls.route('/active_contract/<int:contract_id>/close_contract', methods=['GET', 'POST'])
    @login_required
    def close_contract(contract_id):
        if not current_user.is_boss:
            return redirect(url_for('main_urls.main_page'))

        if request.method == "GET":
            contract = model_controller.get_model_by_id(model_name="ListsOfContracts", pk=contract_id)
            model_controller.update(model_entry=contract,
                                    active=False)

            action_history = StatusSettings.Contract.close
            type_history = StatusSettings.Types.contract
            name_history = contract.name
            user = current_user.username
            request_redirect = save_in_history(action=action_history,
                                               type=type_history,
                                               name=name_history,
                                               user=user,
                                               date=datetime.now())

            if request_redirect is not None:
                return request_redirect

            contract_price = get_contract_price(contract)
            if contract_price == contract.sum:
                return try_to_commit(redirect_to='main_urls.active_contract')
            else:
                flash(f'Указанная сумма контракта не совпадает с действительной на \
                        {contract.sum - contract_price} \
                        рублей')
                return redirect(url_for('main_urls.active_contract'))

        flash(f'Не определён метод запроса!')
        return redirect(url_for('main_urls.main_page'))

    @staticmethod
    @main_urls.route('/active_contract/<int:contract_id>/new_check', methods=['GET', 'POST'])
    @login_required
    def new_check(contract_id):
        if not current_user.is_boss:
            return redirect(url_for('main_urls.main_page'))

        if request.method == "GET":
            contract = model_controller.get_model_by_id(model_name="ListsOfContracts",
                                                        pk=contract_id)
            return render_template('Main_urls/NewCheck.html',
                                   contract=contract)

        if request.method == 'POST':
            sum_check = request.form['sum']
            date_check = request.form['date_check']
            date_check = datetime.fromisoformat(f'{date_check}')

            check = model_controller.create(model_name="CheckLists",
                                            date_check=date_check,
                                            sum=sum_check,
                                            active=1,
                                            date_create=datetime.now(),
                                            list_of_contracts_id=contract_id)
            model_controller.add_in_session(check)

            action_history = StatusSettings.Check.created
            type_history = StatusSettings.Types.check
            name_history = f"{date_check.date().strftime('%d.%m.%Y')}"
            user = current_user.username
            request_redirect = save_in_history(action=action_history,
                                               type=type_history,
                                               name=name_history,
                                               user=user,
                                               date=datetime.now())

            if request_redirect is not None:
                return request_redirect

            return try_to_commit(redirect_to='main_urls.active_contract')

        flash(f'Не определён метод запроса!')
        return redirect(url_for('main_urls.main_page'))

    @staticmethod
    @main_urls.route('/active_contract/<int:check_id>/close_check')
    @login_required
    def close_check(check_id):
        if not current_user.is_boss:
            return redirect(url_for('main_urls.main_page'))

        if request.method == "GET":
            check = model_controller.get_model_by_id(model_name="CheckLists",
                                                     pk=check_id)
            check_price = get_check_price(check)
            if check.sum == check_price:
                model_controller.update(model_entry=check,
                                        active=False)

                action_history = StatusSettings.Check.close
                type_history = StatusSettings.Types.check
                name_history = f"{check.date_check.date().strftime('%d.%m.%Y')}"
                user = current_user.username
                request_redirect = save_in_history(action=action_history,
                                                   type=type_history,
                                                   name=name_history,
                                                   user=user,
                                                   date=datetime.now())
                if request_redirect is not None:
                    return request_redirect

                return try_to_commit(redirect_to='main_urls.active_contract')

            else:
                flash(f'Указанная сумма счёта не совпадает с действительной на {check.sum - check_price} рублей')
                return redirect(url_for('main_urls.active_contract'))

        flash(f'Не определён метод запроса!')
        return redirect(url_for('main_urls.main_page'))

    @staticmethod
    @main_urls.route('/active_contract/<int:check_id>/reopen_check')
    @login_required
    def reopen_check(check_id):
        if not current_user.is_boss:
            return redirect(url_for('main_urls.main_page'))

        if request.method == "GET":
            check = model_controller.get_model_by_id(model_name="CheckLists",
                                                     pk=check_id)
            check.active = True

            action_history = StatusSettings.Check.reopen
            type_history = StatusSettings.Types.check
            name_history = f"{check.date_check.date().strftime('%d.%m.%Y')}"
            user = current_user.username
            request_redirect = save_in_history(action=action_history,
                                               type=type_history,
                                               name=name_history,
                                               user=user,
                                               date=datetime.now())
            if request_redirect is not None:
                return request_redirect

            return try_to_commit(redirect_to='main_urls.active_contract')

        flash(f'Не определён метод запроса!')
        return redirect(url_for('main_urls.main_page'))

    @staticmethod
    @main_urls.route('/active_contract/<int:check_id>/more', methods=['GET', 'POST'])
    @login_required
    def check_more(check_id):
        if not current_user.is_boss:
            return redirect(url_for('main_urls.main_page'))

        if request.method == "GET":
            check = model_controller.get_model_by_id(model_name="CheckLists",
                                                     pk=check_id)

            list_of_contracts = model_controller.get_all_entries(model_name="ListsOfContracts")
            if len(list_of_contracts) > 0:
                last_contract = model_controller.filter_by_model(model_name="ListsOfContracts",
                                                                 mode="first",
                                                                 active=1)
            else:
                flash(f'Контрактов нет')
                return redirect(url_for('main_urls.main_page'))

            work_lists = model_controller.get_all_entries(model_name="WorkList")
            work_list_data = []
            for work in work_lists:
                if work.check_lists_id == check.id or work.check_lists_id is None:
                    work_list_cartridges = model_controller.filter_by_model(model_name="WorkListsCartridges",
                                                                            mode="all",
                                                                            work_list=work.id)
                    work_list_printers = model_controller.filter_by_model(model_name="WorkListsPrinters",
                                                                          mode="all",
                                                                          work_list=work.id)

                    wlc = get_entries_for_work_list_cartridges(work_list_cartridges=work_list_cartridges)
                    wlp = get_entries_for_work_list_printers(work_list_printers=work_list_printers)

                    is_belong = True if work.check_lists_id == check.id else False

                    work_list_data.append([is_belong, work, wlc, wlp, get_work_done_price(work)])

            return render_template('Main_urls/CheckMore.html',
                                   work_list_data=work_list_data,
                                   check=check,
                                   last_contract=last_contract)

        if request.method == "POST":
            works_id = request.form.getlist('works')
            check = model_controller.get_model_by_id(model_name="CheckLists",
                                                     pk=check_id)

            for work_id in works_id:
                work = model_controller.get_model_by_id(model_name="WorkList",
                                                        pk=int(work_id))
                model_controller.update(model_entry=work,
                                        check_lists_id=check.id)

            action_history = StatusSettings.Check.replenished
            type_history = StatusSettings.Types.check
            name_history = f"{check.date_check.date().strftime('%d.%m.%Y')}"
            user = current_user.username
            request_redirect = save_in_history(action=action_history,
                                               type=type_history,
                                               name=name_history,
                                               user=user,
                                               date=datetime.now())
            if request_redirect is not None:
                return request_redirect

            return try_to_commit(redirect_to='main_urls.active_contract')

        flash(f'Не определён метод запроса!')
        return redirect(url_for('main_urls.main_page'))

    @staticmethod
    @main_urls.route('/list_of_completed_works', methods=['GET', 'POST'])
    @login_required
    def list_of_completed_works():
        if not current_user.is_boss:
            return redirect(url_for('main_urls.main_page'))

        if request.method == "GET":
            work_lists = model_controller.get_all_entries(model_name="WorkList")
            work_list_data = []
            for work in work_lists:
                if work.check_lists_id is None:
                    work_list_cartridges = model_controller.filter_by_model(model_name="WorkListsCartridges",
                                                                            mode="all",
                                                                            work_list=work.id)
                    work_list_printers = model_controller.filter_by_model(model_name="WorkListsPrinters",
                                                                          mode="all",
                                                                          work_list=work.id)

                    wlc = get_entries_for_work_list_cartridges(work_list_cartridges=work_list_cartridges)
                    wlp = get_entries_for_work_list_printers(work_list_printers=work_list_printers)

                    work_list_data.append([work, wlc, wlp, get_work_done_price(work)])

            all_works_cartridges = model_controller.get_all_entries(model_name="AllWorksCartridges")
            all_works_printers = model_controller.get_all_entries(model_name="AllWorksPrinters")

            cartridges = model_controller.get_all_entries(model_name="Cartridges")
            printers = model_controller.get_all_entries(model_name="Printer")
            return render_template('Main_urls/ListOfCompletedWorks.html',
                                   work_list_data=work_list_data,
                                   cartridges=cartridges,
                                   printers=printers,
                                   all_works_printers=all_works_printers,
                                   all_works_cartridges=all_works_cartridges, )

        if request.method == "POST":
            date_work_list = request.form['date_work']
            name = request.form['name'].strip()
            date_work_list = datetime.fromisoformat(f'{date_work_list}')
            user = current_user.username

            work_list = model_controller.create(model_name="WorkList",
                                                date_work=date_work_list,
                                                name=name,
                                                date_create=datetime.now())

            cartridges = model_controller.get_all_entries(model_name="Cartridges")
            cartridges_0 = []
            for cartridge in cartridges:
                if cartridge.work_done > 0:
                    cartridges_0.append(cartridge)

            for ctg_0 in cartridges_0:
                prices = request.form.getlist(f'price{ctg_0.number}')
                works = request.form.getlist(f'work{ctg_0.number}')

                if not works[0] == 'NAN' and not prices[0] == "0":
                    for i in range(0, len(works)):
                        if not works[i] == 'NAN':
                            if not prices[i] == 0:
                                wl_c = model_controller.create(model_name="WorkListsCartridges",
                                                               user=user,
                                                               date=datetime.now(),
                                                               cartridge_id=ctg_0.id)
                                work_list.work_list_cartridges_id.append(wl_c)
                                work = model_controller.filter_by_model(model_name="AllWorksCartridges",
                                                                        mode="first",
                                                                        work=works[i])
                                wpc = model_controller.create(model_name="WorksPricesCartridges",
                                                              price=prices[i],
                                                              all_works_cartridges_id=work.id)
                                wl_c.works_prices_cartridges_id.append(wpc)
                                model_controller.add_in_session(wl_c)
                                model_controller.add_in_session(wpc)
                            else:
                                flash(f'Цена за {works[i]} у картриджа {ctg_0.number} не указана')
                                return redirect(request.referrer)
                        else:
                            flash(f'Тип работы у картриджа {ctg_0.number} не выбран')
                            return redirect(request.referrer)

                    new_work_done = ctg_0.work_done - 1
                    model_controller.update(model_entry=ctg_0,
                                            work_done=new_work_done)

            printers = model_controller.get_all_entries(model_name="Printer")
            printers_0 = []
            for printer in printers:
                if printer.work_done > 0:
                    printers_0.append(printer)

            for pr_0 in printers_0:
                prices = request.form.getlist(f'price{pr_0.num_inventory}')
                works = request.form.getlist(f'work{pr_0.num_inventory}')

                if not works[0] == 'NAN' and not prices[0] == "0":
                    for i in range(0, len(works)):
                        if not works[i] == 'NAN':
                            if not prices[i] == 0:
                                wl_p = model_controller.create(model_name="WorkListsPrinters",
                                                               user=user,
                                                               date=datetime.now(),
                                                               printer_id=pr_0.id,
                                                               work_list=work_list.id)
                                work_list.work_list_printers_id.append(wl_p)
                                work = model_controller.filter_by_model(model_name="AllWorksPrinters",
                                                                        mode="first",
                                                                        work=works[i])
                                wpp = model_controller.create(model_name="WorksPricesPrinters",
                                                              price=prices[i],
                                                              all_works_printers_id=work.id,
                                                              work_lists_printers_id=wl_p.id)
                                wl_p.works_prices_printers_id.append(wpp)
                                model_controller.add_in_session(wl_p)
                                model_controller.add_in_session(wpp)
                            else:
                                flash(f'Цена за {works[i]} у принтера {pr_0.name} не указана')
                                return redirect(request.referrer)
                        else:
                            flash(f'Тип работы у принтера {pr_0.name} не выбран')
                            return redirect(request.referrer)

                    new_work_done = pr_0.work_done - 1
                    model_controller.update(model_entry=pr_0,
                                            work_done=new_work_done)

            model_controller.add_in_session(work_list)

            action_history = StatusSettings.WorkList.created
            type_history = StatusSettings.Types.work_list
            name_history = work_list.name
            request_redirect = save_in_history(action=action_history,
                                               type=type_history,
                                               name=name_history,
                                               user=user,
                                               date=datetime.now())
            if request_redirect is not None:
                return request_redirect

            return try_to_commit(redirect_to='main_urls.list_of_completed_works')

        flash(f'Не определён метод запроса!')
        return redirect(url_for('main_urls.main_page'))

    @staticmethod
    @main_urls.route('/list_of_completed_works/<int:work_id>/update', methods=['GET', 'POST'])
    @login_required
    def update_work(work_id):
        if not current_user.is_boss:
            return redirect(url_for('main_urls.main_page'))

        if request.method == "GET":
            work = model_controller.get_model_by_id(model_name="WorkList",
                                                    pk=work_id)
            check = model_controller.get_model_by_id(model_name="CheckLists",
                                                     pk=work.check_lists_id)
            if check is None:
                flash(f'Список проделанных работ не принадлежит ни одному счёту')
                return redirect(url_for('main_urls.active_contract'))

            if not check.active:
                flash(f'Счёт закрыт')
                return redirect(url_for('main_urls.active_contract'))

            work_list_cartridges = model_controller.filter_by_model(model_name="WorkListsCartridges",
                                                                    mode="all",
                                                                    work_list=work.id)
            work_list_printers = model_controller.filter_by_model(model_name="WorkListsPrinters",
                                                                  mode="all",
                                                                  work_list=work.id)

            entries_cartridges_data = get_entries_for_work_list_cartridges(work_list_cartridges=work_list_cartridges)
            entries_printers_data = get_entries_for_work_list_printers(work_list_printers=work_list_printers)

            return render_template("Main_urls/UpdateWork.html",
                                   entries_cartridges_data=entries_cartridges_data,
                                   entries_printers_data=entries_printers_data,
                                   work=work)

        if request.method == "POST":
            work = model_controller.get_model_by_id(model_name="WorkList",
                                                    pk=work_id)
            prices_c = request.form.getlist('prices_c')
            prices_p = request.form.getlist('prices_p')
            works_c_id = request.form.getlist('works_c_id')
            works_p_id = request.form.getlist('works_p_id')

            for wlc in work.work_list_cartridges_id:
                for wpc in wlc.works_prices_cartridges_id:
                    for i in range(0, len(works_c_id)):
                        if int(works_c_id[i]) == wpc.id:
                            model_controller.update(model_entry=wpc,
                                                    price=prices_c[i])
                            break

            for wlp in work.work_list_printers_id:
                for wpp in wlp.works_prices_printers_id:
                    for i in range(0, len(works_p_id)):
                        if int(works_p_id[i]) == wpp.id:
                            model_controller.update(model_entry=wpp,
                                                    price=prices_p[i])
                            break

            action_history = StatusSettings.WorkList.updated
            type_history = StatusSettings.Types.work_list
            name_history = f"{work.date_work.date().strftime('%d.%m.%Y')}"
            user = current_user.username
            request_redirect = save_in_history(action=action_history,
                                               type=type_history,
                                               name=name_history,
                                               user=user,
                                               date=datetime.now())
            if request_redirect is not None:
                return request_redirect

            return try_to_commit(redirect_to='main_urls.active_contract')

        flash(f'Не определён метод запроса!')
        return redirect(url_for('main_urls.main_page'))

    @staticmethod
    @main_urls.route('/progress_report')
    @login_required
    def progress_report():
        if not current_user.is_boss:
            return redirect(url_for('main_urls.main_page'))

        if request.method == "GET":
            contract_data = []
            all_contracts = model_controller.filter_by_model(model_name="ListsOfContracts",
                                                             mode="all",
                                                             active=0)
            for contract in all_contracts:
                checks = model_controller.filter_by_model(model_name="CheckLists",
                                                          mode="all",
                                                          list_of_contracts_id=contract.id)
                contract_data.append([contract, checks])

            active_contract = model_controller.filter_by_model(model_name="ListsOfContracts",
                                                               mode="first",
                                                               active=1)
            if active_contract is not None:
                active_contract_checks = model_controller.filter_by_model(model_name="CheckLists",
                                                                          mode="all",
                                                                          list_of_contracts_id=active_contract.id)
            else:
                active_contract_checks = []

            return render_template('Main_urls/ProgressReport.html',
                                   active_contract=active_contract,
                                   active_contract_checks=active_contract_checks,
                                   contract_data=contract_data)

        flash(f'Не определён метод запроса!')
        return redirect(url_for('main_urls.main_page'))

    @staticmethod
    @main_urls.route('/progress_report/<int:check_id>/<int:contract_id>/more')
    @login_required
    def progress_report_more(check_id, contract_id):
        if not current_user.is_boss:
            return redirect(url_for('main_urls.main_page'))

        if request.method == "GET":
            check = model_controller.get_model_by_id(model_name="CheckLists",
                                                     pk=check_id)

            list_of_contracts = model_controller.get_all_entries(model_name="ListsOfContracts")
            if len(list_of_contracts) > 0:
                last_contract = model_controller.get_model_by_id(model_name="ListsOfContracts",
                                                                 pk=contract_id)
            else:
                flash(f'Контрактов нет')
                return redirect(url_for('main_urls.main_page'))

            work_lists = model_controller.get_all_entries(model_name="WorkList")
            work_list_data = []
            for work in work_lists:
                if work.check_lists_id == check.id or work.check_lists_id is None:
                    work_list_cartridges = model_controller.filter_by_model(model_name="WorkListsCartridges",
                                                                            mode="all",
                                                                            work_list=work.id)
                    work_list_printers = model_controller.filter_by_model(model_name="WorkListsPrinters",
                                                                          mode="all",
                                                                          work_list=work.id)

                    wlc = get_entries_for_work_list_cartridges(work_list_cartridges=work_list_cartridges)
                    wlp = get_entries_for_work_list_printers(work_list_printers=work_list_printers)

                    is_belong = True if work.check_lists_id == check.id else False

                    work_list_data.append([is_belong, work, wlc, wlp, get_work_done_price(work)])

            return render_template('Main_urls/CheckMore.html',
                                   work_list_data=work_list_data,
                                   check=check,
                                   last_contract=last_contract)

        flash(f'Не определён метод запроса!')
        return redirect(url_for('main_urls.main_page'))
