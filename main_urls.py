from datetime import datetime

from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import flash
from models import *
from tabs_that_appear import *
from ScanFunctions import TypeVar

main_urls = Blueprint('main_urls', __name__)


def AllChecksIsActive(contract) -> bool:
    for check in contract.check_lists_id:
        if check.active:
            return True
    return False


def CheckPrice(check) -> float:
    check_price = 0
    for wl in check.work_lists_id:
        for wl_c in wl.work_list_cartridges_id:
            for wp_c in wl_c.works_prices_cartridges_id:
                check_price += wp_c.price
        for wl_p in wl.work_list_printers_id:
            for wp_p in wl_p.works_prices_printers_id:
                check_price += wp_p.price
    return check_price


def WorkDonePrice(work_list) -> float:
    check_price = 0
    for wl_c in work_list.work_list_cartridges_id:
        for wp_c in wl_c.works_prices_cartridges_id:
            check_price += wp_c.price
    for wl_p in work_list.work_list_printers_id:
        for wp_p in wl_p.works_prices_printers_id:
            check_price += wp_p.price
    return check_price


def ContractPrice(contract) -> float:
    check_price = 0
    for check in contract.check_lists_id:
        for wl in check.work_lists_id:
            for wl_c in wl.work_list_cartridges_id:
                for wp_c in wl_c.works_prices_cartridges_id:
                    check_price += wp_c.price
            for wl_p in wl.work_list_printers_id:
                for wp_p in wl_p.works_prices_printers_id:
                    check_price += wp_p.price
    return check_price


@main_urls.route('/')
def main_page():
    return render_template("main.html")


@main_urls.route('/all_history')
def all_history():
    history_cartridges = HistoryCartridge.query.all()
    history_printers = HistoryPrinter.query.all()
    history_works = HistoryWorks.query.all()
    history_checks = HistoryChecks.query.all()
    history_contracts = HistoryContracts.query.all()
    all_history = history_printers + history_cartridges + history_works + history_checks + history_contracts
    return render_template("AllHistory.html",
                           all_history=all_history,
                           Cartridges=Cartridges,
                           Printer=Printer,
                           WorkList=WorkList,
                           CheckLists=CheckLists,
                           ListsOfContracts=ListsOfContracts)


@main_urls.route('/active_contract', methods=['GET', 'POST'])
def active_contract():
    if len(ListsOfContracts.query.all()) > 0:
        last_contract = ListsOfContracts.query.filter(ListsOfContracts.active == 1).first()
    else:
        last_contract = None

    force_close = False
    cartridges = Cartridges.query.all()
    printers = Printer.query.all()

    no_one_is_active = False
    if last_contract is not None:
        check_list = CheckLists.query.filter(CheckLists.list_of_contracts_id == last_contract.id).all()
        for check in check_list:
            if check.active:
                no_one_is_active = False
                break
            else:
                no_one_is_active = True

    count_wd = len(
        Cartridges.query.filter(Cartridges.work_done == 0).all() + Printer.query.filter(Printer.work_done == 0).all())

    all_checks_active = False
    contract_price = 0
    for contract in ListsOfContracts.query.all():
        if contract.active:
            all_checks_active = AllChecksIsActive(last_contract)
            contract_price = ContractPrice(last_contract)
            break

    if request.method == "POST":
        name = request.form['name']
        sum_contract = request.form['sum_contract']
        date_contract = request.form['date_contract']
        date_contract = datetime.fromisoformat(f'{date_contract}')

        contract = ListsOfContracts(name=name,
                                    sum=sum_contract,
                                    date_contract=date_contract,
                                    active=True)

        db.session.add(contract)

        try:
            action = f"Создан новый договор"
            user = "Добрынин И.А."
            ah = HistoryContracts(action=action,
                                  user=user)
            contract.history_contracts_id.append(ah)
            db.session.add(ah)
        except:
            flash('При создании статуса произошла ошибка')
            return render_template("main.html")

        try:
            db.session.commit()
            return redirect(request.referrer)
        except:
            flash('При создании договора произошла ошибка')
            return render_template("main.html")

    else:
        return render_template('WorkDone.html',
                               cartridges=cartridges,
                               printers=printers,
                               count_wd=count_wd,
                               last_contract=last_contract,
                               CheckLists=CheckLists,
                               force_close=force_close,
                               no_one_is_active=no_one_is_active,
                               all_checks_active=all_checks_active,
                               contract_price=contract_price)


@main_urls.route('/active_contract/<int:contract_id>/close_contract', methods=['GET', 'POST'])
def close_contract(contract_id):
    contract = ListsOfContracts.query.get(contract_id)
    contract.active = False

    try:
        action = f"Закрытие договора"
        user = "Добрынин И.А."
        ah = HistoryContracts(action=action,
                              user=user)
        contract.history_contracts_id.append(ah)
        db.session.add(ah)
    except:
        flash('При создании статуса произошла ошибка')
        return render_template("main.html")

    contract_price = ContractPrice(contract)
    if contract_price == contract.sum:
        try:
            db.session.commit()
            return redirect('/active_contract')
        except:
            flash('При закрытии контракта произошла ошибка')
            return render_template("main.html")
    else:
        flash(f'Указанная сумма контракта не совпадает с действительной на {contract.sum - contract_price} рублей')
        return redirect('/active_contract')


@main_urls.route('/active_contract/<int:contract_id>/new_check', methods=['GET', 'POST'])
def new_check(contract_id):
    contract = ListsOfContracts.query.get(contract_id)

    if request.method == 'POST':
        sum_check = request.form['sum']
        date_check = request.form['date_check']
        date_check = datetime.fromisoformat(f'{date_check}')

        check = CheckLists(date_check=date_check,
                           sum=sum_check,
                           active=1)

        contract.check_lists_id.append(check)
        db.session.add(check)

        try:
            action = f"Создание счёта для договора"
            user = "Добрынин И.А."
            ah = HistoryContracts(action=action,
                                  user=user)
            contract.history_contracts_id.append(ah)
            db.session.add(ah)
        except:
            flash('При создании статуса произошла ошибка')
            return render_template("main.html")

        try:
            db.session.commit()
            return redirect(f'/active_contract/{check.id}/more')
        except:
            flash('При создании счёта произошла ошибка')
            return render_template("main.html")

    return render_template('NewCheck.html',
                           contract=contract)


@main_urls.route('/active_contract/<int:check_id>/close_check')
def close_check(check_id):
    check = CheckLists.query.get(check_id)

    check_price = CheckPrice(check)

    if check.sum == check_price:
        check.active = False
        contract = ListsOfContracts.query.get(check.list_of_contracts_id)

        try:
            action = f"Закрытие счёта у договора"
            user = "Добрынин И.А."
            ah = HistoryContracts(action=action,
                                  user=user)
            contract.history_contracts_id.append(ah)
            db.session.add(ah)
        except:
            flash('При создании статуса произошла ошибка')
            return render_template("main.html")

        try:
            db.session.commit()
            return redirect('/active_contract')
        except:
            flash('При закрытии счёта произошла ошибка')
            return render_template("main.html")

    else:
        flash(f'Указанная сумма счёта не совпадает с действительной на {check.sum - check_price} рублей')
        return redirect('/active_contract')


@main_urls.route('/active_contract/<int:check_id>/reopen_check')
def reopen_check(check_id):
    check = CheckLists.query.get(check_id)
    check.active = True
    contract = ListsOfContracts.query.get(check.list_of_contracts_id)

    try:
        action = f"Переоткрытие счёта у договора"
        user = "Добрынин И.А."
        ah = HistoryContracts(action=action,
                              user=user)
        contract.history_contracts_id.append(ah)
        db.session.add(ah)
    except:
        flash('При создании статуса произошла ошибка')
        return render_template("main.html")

    try:
        db.session.commit()
        return redirect('/active_contract')
    except:
        flash('При переоткрытии счёта произошла ошибка')
        return render_template("main.html")


@main_urls.route('/active_contract/<int:check_id>/more', methods=['GET', 'POST'])
def check_more(check_id):
    if len(ListsOfContracts.query.all()) > 0:
        last_contract = ListsOfContracts.query.filter(ListsOfContracts.active == 1).first()
    else:
        last_contract = None

    all_wp = AllWorksPrinters.query.all()
    all_wc = AllWorksCartridges.query.all()
    wl_add = WorkList.query.filter(WorkList.check_lists_id == None).all()
    wl = WorkList.query.filter(WorkList.check_lists_id == check_id).all()
    len_wl = len(wl_add)
    wlp = WorkListsPrinters.query.all()
    wlc = WorkListsCartridges.query.all()
    check = CheckLists.query.get(check_id)

    wd_prices = []
    for el in wl:
        wd_prices.append(WorkDonePrice(el))

    if request.method == "POST":
        works = request.form.getlist('works')

        for work in works:
            work = WorkList.query.filter(WorkList.id == work).first()
            check.work_lists_id.append(work)

        try:
            action = f"Добавление проделанных работ к счёту"
            user = "Добрынин И.А."
            ah = HistoryChecks(action=action,
                               user=user)
            check.history_check_list_id.append(ah)
            db.session.add(ah)
        except:
            flash('При создании статуса произошла ошибка')
            return render_template("main.html")

        try:
            db.session.commit()
            return redirect(request.referrer)
        except:
            flash('При обновлении счёта произошла ошибка')
            return render_template("main.html")
    else:
        return render_template('CheckMore.html',
                               check=check,
                               last_contract=last_contract,
                               wlc=wlc,
                               wlp=wlp,
                               wl=wl,
                               wl_add=wl_add,
                               Printer=Printer,
                               Cartridges=Cartridges,
                               AllWorksPrinters=AllWorksPrinters,
                               AllWorksCartridges=AllWorksCartridges,
                               all_wc=all_wc,
                               all_wp=all_wp,
                               len_wl=len_wl,
                               wd_prices=wd_prices)


@main_urls.route('/list_of_completed_works', methods=['GET', 'POST'])
def list_of_completed_works():
    wl = WorkList.query.filter(WorkList.check_lists_id == None).all()
    len_wl = len(wl)
    wlp = WorkListsPrinters.query.all()
    wlc = WorkListsCartridges.query.all()
    all_wc = AllWorksCartridges.query.all()
    all_wp = AllWorksPrinters.query.all()

    wd_prices = []
    for el in wl:
        wd_prices.append(WorkDonePrice(el))

    if request.method == "POST":
        date_work_list = request.form['date_work']
        date_work_list = datetime.fromisoformat(f'{date_work_list}')
        user = request.form.getlist('user')[0]

        work_list = WorkList(date_work=date_work_list)

        cartridges_0 = Cartridges.query.filter(Cartridges.work_done == 0).all()
        for ctg_0 in cartridges_0:
            prices = request.form.getlist(f'price{ctg_0.number}')
            works = request.form.getlist(f'work{ctg_0.number}')

            if not works[0] == 'NAN' and not prices[0] == "0":
                for i in range(0, len(works)):
                    if not works[i] == 'NAN':
                        if not prices[i] == 0:
                            wl_c = WorkListsCartridges(user=user)
                            work = AllWorksCartridges.query.filter(AllWorksCartridges.work == works[i]).first()
                            wpc = WorksPricesCartridges(price=prices[i])
                            work.works_prices_cartridges_id.append(wpc)
                            wl_c.works_prices_cartridges_id.append(wpc)
                            ctg_0.work_done_cartridges_id.append(wl_c)
                            work_list.work_list_cartridges_id.append(wl_c)
                            db.session.add(wl_c)
                            db.session.add(wpc)
                        else:
                            flash(f'Цена за {works[i]} у картриджа {ctg_0.number} не указана')
                            return redirect(request.referrer)
                    else:
                        flash(f'Тип работы у картриджа {ctg_0.number} не выбран')
                        return redirect(request.referrer)

                ctg_0.work_done = True

        printers_0 = Printer.query.filter(Printer.work_done == 0).all()
        for pr_0 in printers_0:
            prices = request.form.getlist(f'price{pr_0.num_inventory}')
            works = request.form.getlist(f'work{pr_0.num_inventory}')

            if not works[0] == 'NAN' and not prices[0] == "0":
                for i in range(0, len(works)):
                    if not works[i] == 'NAN':
                        if not prices[i] == 0:
                            wl_p = WorkListsPrinters(user=user)
                            work = AllWorksPrinters.query.filter(AllWorksPrinters.work == works[i]).first()
                            wpp = WorksPricesPrinters(price=prices[i])
                            work.works_prices_printers_id.append(wpp)
                            wl_p.works_prices_printers_id.append(wpp)
                            pr_0.work_done_printers_id.append(wl_p)
                            work_list.work_list_printers_id.append(wl_p)
                            db.session.add(wl_p)
                            db.session.add(wpp)
                        else:
                            flash(f'Цена за {works[i]} у принтера {pr_0.name} не указана')
                            return redirect(request.referrer)
                    else:
                        flash(f'Тип работы у принтера {pr_0.name} не выбран')
                        return redirect(request.referrer)

                pr_0.work_done = True

        try:
            action = f"Создание проделанных работ"
            user = "Добрынин И.А."
            ah = HistoryWorks(action=action,
                              user=user)
            work_list.history_work_id.append(ah)
            db.session.add(ah)
        except:
            flash('При создании статуса произошла ошибка')
            return render_template("main.html")

        try:
            db.session.add(work_list)
            db.session.commit()
            return redirect(request.referrer)
        except:
            return render_template("main.html")
    else:
        return render_template('ListOfCompletedWorks.html',
                               Cartridges=Cartridges,
                               Printer=Printer,
                               wl=wl,
                               wlc=wlc,
                               wlp=wlp,
                               AllWorksPrinters=AllWorksPrinters,
                               AllWorksCartridges=AllWorksCartridges,
                               len_wl=len_wl,
                               all_wc=all_wc,
                               all_wp=all_wp,
                               wd_prices=wd_prices)


@main_urls.route('/progress_report')
def progress_report():
    all_contracts = ListsOfContracts.query.filter(ListsOfContracts.active == 0).all()
    wdc = WorkListsCartridges.query.all()
    wdp = WorkListsPrinters.query.all()
    wd = wdc + wdp

    return render_template('ProgressReport.html',
                           work_done=wd,
                           Cartridges=Cartridges,
                           Printer=Printer,
                           CheckLists=CheckLists,
                           all_contracts=all_contracts)


@main_urls.route('/progress_report/<int:check_id><int:contract_id>/more')
def progress_report_more(check_id, contract_id):
    contract = ListsOfContracts.query.get(contract_id)
    check = CheckLists.query.get(check_id)

    wl = WorkList.query.filter(WorkList.check_lists_id == check_id).all()
    len_wl = len(wl)
    wlp = WorkListsPrinters.query.all()
    wlc = WorkListsCartridges.query.all()

    all_wp = AllWorksPrinters.query.all()
    all_wc = AllWorksCartridges.query.all()

    wd_prices = []
    for el in wl:
        wd_prices.append(WorkDonePrice(el))
    print(wl)

    return render_template('CheckMore.html',
                           check=check,
                           last_contract=contract,
                           wlc=wlc,
                           wlp=wlp,
                           wl=wl,
                           Printer=Printer,
                           Cartridges=Cartridges,
                           AllWorksPrinters=AllWorksPrinters,
                           AllWorksCartridges=AllWorksCartridges,
                           all_wc=all_wc,
                           all_wp=all_wp,
                           len_wl=len_wl,
                           wd_prices=wd_prices)
