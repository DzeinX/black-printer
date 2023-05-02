from flask import render_template
from flask import redirect
from flask import request
from flask import flash
from flask import Blueprint
from flask_login import current_user, login_required
from datetime import datetime
from models import *
from tabs_that_appear import *
from ScanFunctions import TypeVar
from StatusSettings import StatusSettings
from sqlalchemy import func

cartridge_urls = Blueprint('cartridge_urls', __name__)


@cartridge_urls.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        return redirect('/login')
    else:
        return response


@cartridge_urls.route('/add_works_cartridges', methods=['GET', 'POST'])
@login_required
def add_works_cartridges():
    if current_user.is_boss:
        all_works_cartridges = AllWorksCartridges.query.all()
        counter_works = len(all_works_cartridges)

        if request.method == "POST":
            all_works_cartridges = request.form.getlist('works')

            var_check = TypeVar(all_works_cartridges, var_type='str')
            if var_check[1]:
                all_works_cartridges = var_check[0][0]
            else:
                if isinstance(var_check[0], str):
                    flash(var_check[0])
                    return redirect(request.referrer)
                else:
                    flash('Incorrect value')
                    return redirect(request.referrer)

            if len(all_works_cartridges) == 0:
                flash('Нельзя удалить все модели')
                return redirect(request.referrer)

            AllWorksCartridges.query.delete()
            try:
                for work in all_works_cartridges:

                    if work != '' and not work.isspace():
                        model = AllWorksCartridges(work=work)
                        db.session.add(model)
            except:
                return f"Не удалось сохранить изменения"

            try:
                db.session.commit()
                return redirect("/add_works_cartridges")
            except:
                flash('Не удалось добавить тип работ')
                return render_template("main.html")
        else:
            return render_template("AddWorksCartridges.html",
                                   all_works_cartridges=all_works_cartridges,
                                   counter_works=counter_works)
    else:
        return redirect('/')


@cartridge_urls.route('/add_models', methods=['GET', 'POST'])
@login_required
def add_models():
    list_models = ListModels.query.all()
    counter_models = len(list_models)

    if request.method == "POST":
        list_models = request.form.getlist('model')

        var_check = TypeVar(list_models, var_type='str')
        if var_check[1]:
            list_models = var_check[0][0]
        else:
            if isinstance(var_check[0], str):
                flash(var_check[0])
                return redirect(request.referrer)
            else:
                flash('Incorrect value')
                return redirect(request.referrer)

        if len(list_models) == 0:
            flash('Нельзя удалить все модели')
            return redirect(request.referrer)

        ListModels.query.delete()
        try:
            for model in list_models:
                is_not_available = ListModels.query.filter(ListModels.model == model).first() is None
                if model != '' and not model.isspace() and is_not_available:
                    model = ListModels(model=model)
                    db.session.add(model)
        except:
            return f"Не удалось сохранить изменения"

        try:
            db.session.commit()
            return redirect("/add_models")
        except:
            flash('Не удалось добавить модель')
            return render_template("main.html")
    else:
        return render_template("AddModels.html",
                               list_models=list_models,
                               counter_models=counter_models)


@cartridge_urls.route('/cartridge/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update_cartridge(id):
    cartridge = Cartridges.query.get(id)
    list_models = ListModels.query.all()

    counter_models = len(cartridge.cartridge_models)

    if request.method == "POST":
        cartridge_models = request.form.getlist('model')
        number = request.form['number']

        var_check = TypeVar(cartridge_models, var_type='str')
        if var_check[1]:
            cartridge_models = var_check[0][0]
        else:
            if isinstance(var_check[0], str):
                flash(var_check[0])
                return redirect(request.referrer)
            else:
                flash('Incorrect value')
                return redirect(request.referrer)

        var_check = TypeVar(number, var_type='int')
        if var_check[1]:
            number = var_check[0][0]
        else:
            if isinstance(var_check[0], str):
                flash(var_check[0])
                return redirect(request.referrer)
            else:
                flash('Incorrect value')
                return redirect(request.referrer)

        if len(Cartridges.query.filter(Cartridges.number == number).all()) > 1:
            flash('Такой номер уже есть')
            return redirect(request.referrer)
        else:
            cartridge.number = number

        cartridge.cartridge_models = []
        for model in cartridge_models:
            if model != "":
                model = ListModels.query.filter(ListModels.model == model).first()
                cartridge.cartridge_models.append(model)

        try:
            action_h = StatusSettings.CARTRIDGE["Изменён"]
            type_h = StatusSettings.TYPE['CARTRIDGE']
            name_h = f"{cartridge.number}"
            user = request.form['user']
            ah = AllHistory(action=action_h,
                            type=type_h,
                            name=name_h,
                            user=user,
                            date=datetime.now())
            cartridge.all_history_id.append(ah)
            db.session.add(ah)
        except:
            flash('При создании статуса произошла ошибка')
            return render_template("main.html")

        try:
            db.session.commit()
            return redirect('/cartridges')
        except:
            flash('При обновлении картриджа произошла ошибка')
            return render_template("main.html")
    else:
        return render_template("cartridge_update.html",
                               cartridge=cartridge,
                               list_models=list_models,
                               counter_models=counter_models)


@cartridge_urls.route('/cartridge/<int:id>/statuses')
@login_required
def cartridge_status(id):
    statuses = AllHistory.query.filter(AllHistory.cartridge_id == id).order_by(AllHistory.date.desc()).all()
    cartridge = Cartridges.query.get(id)
    return render_template("CartridgeStatuses.html",
                           statuses=statuses,
                           id=id,
                           cartridge=cartridge,
                           StatusSettings=StatusSettings)


@cartridge_urls.route('/cartridges', methods=['GET', 'POST'])
@login_required
def cartridges():
    list_models = ListModels.query.all()
    cartridges = Cartridges.query.order_by(Cartridges.date_added.desc()).all()

    cartridges_and_location = []
    for cartridge in cartridges:
        cartridges_and_location.append(
            [cartridge, CartridgeIssuance.query.filter(CartridgeIssuance.cartridge_number_id == cartridge.id).all()])

    if request.method == 'POST':
        action = "Создан"
        number = request.form['number']
        cartridge_models = request.form.getlist('model')

        var_check = TypeVar(number, var_type='int')
        if var_check[1]:
            number = var_check[0][0]
        else:
            if isinstance(var_check[0], str):
                flash(var_check[0])
                return redirect(request.referrer)
            else:
                flash('Incorrect value')
                return redirect(request.referrer)

        if len(cartridge_models) == 0:
            flash('Не выбрана ни одна модель')
            return redirect(request.referrer)

        if Cartridges.query.filter(Cartridges.number == number).first():
            flash('Такой номер уже есть')
            return redirect(request.referrer)

        cartridge = Cartridges(status=action,
                               number=number)

        for model in cartridge_models:
            model = ListModels.query.filter(ListModels.model == model).first()
            cartridge.cartridge_models.append(model)

        try:
            action_h = StatusSettings.CARTRIDGE["Создан"]
            type_h = StatusSettings.TYPE['CARTRIDGE']
            name_h = f"{number}"
            user = request.form['user']
            ah = AllHistory(action=action_h,
                            type=type_h,
                            name=name_h,
                            user=user,
                            date=datetime.now())
            cartridge.all_history_id.append(ah)
            db.session.add(ah)
        except:
            flash('При создании статуса произошла ошибка')
            return render_template("main.html")

        try:
            db.session.add(cartridge)
            db.session.commit()
            return redirect('/cartridges')
        except:
            flash('При создании картриджа произошла ошибка')
            return render_template("main.html")
    else:
        number_cartridge = int(db.session.query(func.max(Cartridges.number)).first()[0] + 1)
        return render_template("Cartridges.html",
                               cartridges_and_location=cartridges_and_location,
                               list_models=list_models,
                               CartridgeIssuance=CartridgeIssuance,
                               Printer=Printer,
                               StatusSettings=StatusSettings,
                               number_cartridge=number_cartridge)


@cartridge_urls.route('/cartridge/<int:id>/delete')
@login_required
def delete_cartridge(id):
    cartridge = Cartridges.query.get_or_404(id)
    try:
        try:
            action_h = StatusSettings.CARTRIDGE["Удалён"]
            type_h = StatusSettings.TYPE['CARTRIDGE']
            name_h = f"{cartridge.number}"
            user = current_user.username
            ah = AllHistory(action=action_h,
                            type=type_h,
                            name=name_h,
                            user=user,
                            date=datetime.now())
            cartridge.all_history_id.append(ah)
            db.session.add(ah)
        except:
            flash('При создании статуса произошла ошибка')
            return render_template("main.html")

        cartridge.efficiency = 0
        cartridge.status = "Удалён"
        db.session.add(cartridge)
        db.session.commit()
        return redirect('/cartridges')
    except:
        flash('Ошибка удаления картриджа')
        return render_template('main.html')


@cartridge_urls.route('/cartridge/<int:id>/resume')
@login_required
def resume_cartridge(id):
    cartridge = Cartridges.query.get_or_404(id)
    try:
        try:
            action_h = StatusSettings.CARTRIDGE["Восстановлен"]
            type_h = StatusSettings.TYPE['CARTRIDGE']
            name_h = f"{cartridge.number}"
            user = current_user.username
            ah = AllHistory(action=action_h,
                            type=type_h,
                            name=name_h,
                            user=user,
                            date=datetime.now())
            cartridge.all_history_id.append(ah)
            db.session.add(ah)
        except:
            flash('При создании статуса произошла ошибка')
            return render_template("main.html")

        cartridge.efficiency = 1
        cartridge.status = "Восстановлен"
        db.session.add(cartridge)
        db.session.commit()
        return redirect(request.referrer)
    except:
        flash('Ошибка восстановления картриджа')
        return render_template('main.html')


@cartridge_urls.route('/deleted_cartridges')
@login_required
def deleted_cartridges():
    cartridges = Cartridges.query.all()
    return render_template('DeletedCartridges.html',
                           cartridges=cartridges)


@cartridge_urls.route('/brought_a_cartridge', methods=['GET', 'POST'])
@login_required
def brought_a_cartridge():
    cartridges = Cartridges.query.all()
    printers = Printer.query.all()
    buildings = Buildings.query.all()
    divisions = Division.query.all()

    if request.method == "POST":
        cartridge_number = request.form.getlist('cartridge_number')
        id_form = request.form['id_form']

        if len(cartridge_number) == 0:
            flash('Не выбрана ни одна модель')
            return redirect(request.referrer)

        if id_form == "2":
            for number in cartridge_number:
                location = request.form[f'location{number}']
                learning_campus = request.form[f'learning_campus{number}']
                cabinet = request.form[f'cabinet{number}']
                user = request.form['user']
                cartridge = Cartridges.query.filter(Cartridges.number == number).first()

                brought_a_cartridge = BroughtACartridge(location=location,
                                                        learning_campus=learning_campus,
                                                        cabinet=cabinet,
                                                        user=user)

                cartridge.status = "Принят в заправку"

                try:
                    action_h = StatusSettings.CARTRIDGE["Принят в заправку"]
                    type_h = StatusSettings.TYPE['CARTRIDGE']
                    name_h = f"{cartridge.number}"
                    ah = AllHistory(action=action_h,
                                    type=type_h,
                                    name=name_h,
                                    user=user)
                    cartridge.all_history_id.append(ah)
                    db.session.add(ah)
                except:
                    flash('При создании статуса произошла ошибка')
                    return render_template("main.html")

                cartridge.brought_a_cartridge_id.append(brought_a_cartridge)

                db.session.add(brought_a_cartridge)
        else:
            location = request.form['location']
            learning_campus = request.form['learning_campus']
            cabinet = request.form['cabinet']
            user = request.form['user']
            printer = request.form['printer_id']
            printer = Printer.query.get(int(printer))

            var_check = TypeVar(location, learning_campus, cabinet, var_type='str')
            if var_check[1]:
                location = var_check[0][0]
                learning_campus = var_check[0][1]
                cabinet = var_check[0][2]
            else:
                if isinstance(var_check[0], str):
                    flash(var_check[0])
                    return redirect(request.referrer)
                else:
                    flash('Incorrect value')
                    return redirect(request.referrer)

            for number in cartridge_number:
                cartridge = Cartridges.query.filter(Cartridges.number == number).first()

                brought_a_cartridge = BroughtACartridge(location=location,
                                                        learning_campus=learning_campus,
                                                        cabinet=cabinet,
                                                        user=user)

                cartridge.status = "Принят в заправку"

                try:
                    action_h = StatusSettings.CARTRIDGE["Принят в заправку"]
                    type_h = StatusSettings.TYPE['CARTRIDGE']
                    name_h = f"{cartridge.number}"
                    ah = AllHistory(action=action_h,
                                    type=type_h,
                                    name=name_h,
                                    user=user,
                                    date=datetime.now())
                    cartridge.all_history_id.append(ah)
                    db.session.add(ah)
                except:
                    flash('При создании статуса произошла ошибка')
                    return render_template("main.html")

                cartridge.brought_a_cartridge_id.append(brought_a_cartridge)
                printer.cartridge_brought_id.append(brought_a_cartridge)

                db.session.add(brought_a_cartridge)

        try:
            db.session.commit()
            return redirect('/cartridges')
        except:
            flash('Не удалось отправить форму')
            return render_template("main.html")
    else:
        return render_template('BroughtACartridge.html',
                               cartridges=cartridges,
                               printers=printers,
                               CartridgeIssuance=CartridgeIssuance,
                               buildings=buildings,
                               divisions=divisions)


@cartridge_urls.route('/refueling', methods=['GET', 'POST'])
@login_required
def refueling():
    cartridges = Cartridges.query.all()

    if request.method == "POST":
        id_form = request.form['id_form']
        cartridge_number = request.form.getlist('cartridge_number')

        if len(cartridge_number) == 0:
            flash('Не выбрана ни одна модель')
            return redirect(request.referrer)

        if id_form == '2':
            for number in cartridge_number:
                user = request.form[f'user']
                cartridge = Cartridges.query.filter(Cartridges.number == number).first()
                refueling = Refueling(user=user)

                cartridge.status = "В заправке"

                try:
                    action_h = StatusSettings.CARTRIDGE["В заправке"]
                    type_h = StatusSettings.TYPE['CARTRIDGE']
                    name_h = f"{cartridge.number}"
                    ah = AllHistory(action=action_h,
                                    type=type_h,
                                    name=name_h,
                                    user=user,
                                    date=datetime.now())
                    cartridge.all_history_id.append(ah)
                    db.session.add(ah)
                except:
                    flash('При создании статуса произошла ошибка')
                    return render_template("main.html")

                cartridge.refueling_id.append(refueling)

                db.session.add(refueling)
        else:
            for number in cartridge_number:
                user = request.form['user']
                cartridge = Cartridges.query.filter(Cartridges.number == number).first()
                refueling = Refueling(user=user)

                cartridge.status = "В заправке"

                try:
                    action_h = StatusSettings.CARTRIDGE["В заправке"]
                    type_h = StatusSettings.TYPE['CARTRIDGE']
                    name_h = f"{cartridge.number}"
                    ah = AllHistory(action=action_h,
                                    type=type_h,
                                    name=name_h,
                                    user=user,
                                    date=datetime.now())
                    cartridge.all_history_id.append(ah)
                    db.session.add(ah)
                except:
                    flash('При создании статуса произошла ошибка')
                    return render_template("main.html")

                cartridge.refueling_id.append(refueling)

                db.session.add(refueling)

        try:
            db.session.commit()
            return redirect('/cartridges')
        except:
            flash('Не удалось отправить форму')
            return render_template("main.html")
    else:
        return render_template('Refueling.html',
                               cartridges=cartridges)


@cartridge_urls.route('/reception_from_a_refuelling', methods=['GET', 'POST'])
@login_required
def receptionFromARefuelling():
    cartridges = Cartridges.query.all()

    if request.method == "POST":
        id_form = request.form['id_form']
        cartridge_number = request.form.getlist('cartridge_number')

        if len(cartridge_number) == 0:
            flash('Не выбрана ни одна модель')
            return redirect(request.referrer)

        if id_form == '2':
            for number in cartridge_number:
                user = request.form['user']
                cartridge = Cartridges.query.filter(Cartridges.number == number).first()
                reception_from_a_refueling = ReceptionFromARefueling(user=user)

                cartridge.status = "В резерве"

                try:
                    action_h = StatusSettings.CARTRIDGE["В резерве"]
                    type_h = StatusSettings.TYPE['CARTRIDGE']
                    name_h = f"{cartridge.number}"
                    ah = AllHistory(action=action_h,
                                    type=type_h,
                                    name=name_h,
                                    user=user,
                                    date=datetime.now())
                    cartridge.all_history_id.append(ah)
                    db.session.add(ah)
                except:
                    flash('При создании статуса произошла ошибка')
                    return render_template("main.html")

                cartridge.reception_from_a_refueling_id.append(reception_from_a_refueling)

                cartridge.work_done = False

                db.session.add(reception_from_a_refueling)
        else:
            for number in cartridge_number:
                user = request.form['user']
                cartridge = Cartridges.query.filter(Cartridges.number == number).first()
                reception_from_a_refueling = ReceptionFromARefueling(user=user)

                cartridge.status = "В резерве"

                try:
                    action_h = StatusSettings.CARTRIDGE["В резерве"]
                    type_h = StatusSettings.TYPE['CARTRIDGE']
                    name_h = f"{cartridge.number}"
                    ah = AllHistory(action=action_h,
                                    type=type_h,
                                    name=name_h,
                                    user=user,
                                    date=datetime.now())
                    cartridge.all_history_id.append(ah)
                    db.session.add(ah)
                except:
                    flash('При создании статуса произошла ошибка')
                    return render_template("main.html")

                cartridge.reception_from_a_refueling_id.append(reception_from_a_refueling)

                cartridge.work_done = False

                db.session.add(reception_from_a_refueling)

        try:
            db.session.commit()
            return redirect('/cartridges')
        except:
            flash('Не удалось отправить форму')
            return render_template("main.html")
    else:
        return render_template('ReceptionFromARefuelling.html',
                               cartridges=cartridges)


@cartridge_urls.route('/issuance_cartridges', methods=['GET', 'POST'])
@login_required
def issuance_cartridges():
    cartridges = Cartridges.query.all()
    printers = Printer.query.all()
    buildings = Buildings.query.all()
    divisions = Division.query.all()

    if request.method == "POST":
        cartridge_number = request.form.getlist('cartridge_number')
        id_form = request.form['id_form']

        if len(cartridge_number) == 0:
            flash('Не выбрана ни одна модель')
            return redirect(request.referrer)

        if id_form == "2":
            for number in cartridge_number:
                user = request.form[f'user']
                location = request.form[f'location{number}']
                learning_campus = request.form[f'learning_campus{number}']
                cabinet = request.form[f'cabinet{number}']
                printer = request.form[f'printer{number}']
                cartridge = Cartridges.query.filter(Cartridges.number == number).first()
                issuance = CartridgeIssuance(user=user,
                                             location=location,
                                             learning_campus=learning_campus,
                                             cabinet=cabinet)

                cartridge.status = "В подразделении"

                try:
                    action_h = StatusSettings.CARTRIDGE["В подразделении"]
                    type_h = StatusSettings.TYPE['CARTRIDGE']
                    name_h = f"{cartridge.number}"
                    ah = AllHistory(action=action_h,
                                    type=type_h,
                                    name=name_h,
                                    user=user,
                                    date=datetime.now())
                    cartridge.all_history_id.append(ah)
                    db.session.add(ah)
                except:
                    flash('При создании статуса произошла ошибка')
                    return render_template("main.html")

                cartridge.issuance_id.append(issuance)

                db.session.add(issuance)
        else:
            user = request.form['user']
            location = request.form['location']
            learning_campus = request.form['learning_campus']
            cabinet = request.form['cabinet']
            printer = request.form['printer_id']
            printer = Printer.query.filter(Printer.id == int(printer)).first()

            var_check = TypeVar(location, learning_campus, cabinet, var_type='str')
            if var_check[1]:
                location = var_check[0][0]
                learning_campus = var_check[0][1]
                cabinet = var_check[0][2]
            else:
                if isinstance(var_check[0], str):
                    flash(var_check[0])
                    return redirect(request.referrer)
                else:
                    flash('Incorrect value')
                    return redirect(request.referrer)

            for number in cartridge_number:
                cartridge = Cartridges.query.filter(Cartridges.number == number).first()

                issuance = CartridgeIssuance(user=user,
                                             location=location,
                                             learning_campus=learning_campus,
                                             cabinet=cabinet)

                cartridge.status = "В подразделении"

                try:
                    action_h = StatusSettings.CARTRIDGE["В подразделении"]
                    type_h = StatusSettings.TYPE['CARTRIDGE']
                    name_h = f"{cartridge.number}"
                    ah = AllHistory(action=action_h,
                                    type=type_h,
                                    name=name_h,
                                    user=user,
                                    date=datetime.now())
                    cartridge.all_history_id.append(ah)
                    db.session.add(ah)
                except:
                    flash('При создании статуса произошла ошибка')
                    return render_template("main.html")

                cartridge.issuance_id.append(issuance)
                printer.cartridge_issuance_id.append(issuance)

                db.session.add(issuance)

        try:
            db.session.commit()
            return redirect('/cartridges')
        except:
            flash('Не удалось отправить форму')
            return render_template("main.html")
    else:
        return render_template('IssuanceCartridges.html',
                               cartridges=cartridges,
                               BroughtACartridge=BroughtACartridge,
                               Printer=Printer,
                               printers=printers,
                               buildings=buildings,
                               divisions=divisions)
