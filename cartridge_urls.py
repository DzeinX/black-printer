from flask import render_template
from flask import redirect
from flask import request
from flask import flash
from flask import Blueprint
from models import *
from tabs_that_appear import *
from ScanFunctions import TypeVar

cartridge_urls = Blueprint('cartridge_urls', __name__)


@cartridge_urls.route('/add_works_cartridges', methods=['GET', 'POST'])
def add_works_cartridges():
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


@cartridge_urls.route('/add_models', methods=['GET', 'POST'])
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

                if model != '' and not model.isspace():
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

        user = "Добрынин И.А."
        date_of_status = HistoryCartridge(action="изменён",
                                          user=user)
        cartridge.date_of_status.append(date_of_status)
        db.session.add(date_of_status)

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
def cartridge_status(id):
    statuses = HistoryCartridge.query.order_by(HistoryCartridge.date.desc()).all()
    cartridge = Cartridges.query.get(id)
    return render_template("CartridgeStatuses.html",
                           statuses=statuses,
                           id=id,
                           cartridge=cartridge)


@cartridge_urls.route('/cartridges', methods=['GET', 'POST'])
def cartridges():
    list_models = ListModels.query.all()
    cartridges = Cartridges.query.order_by(Cartridges.date_added.desc()).all()

    if request.method == 'POST':
        action = "В резерве"
        number = request.form['number']
        user = request.form['user']
        date_of_status = HistoryCartridge(action=action,
                                          user=user)
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
        cartridge.date_of_status.append(date_of_status)

        for model in cartridge_models:
            model = ListModels.query.filter(ListModels.model == model).first()
            cartridge.cartridge_models.append(model)

        try:
            db.session.add(cartridge)
            db.session.commit()
            return redirect('/cartridges')
        except:
            flash('При создании картриджа произошла ошибка')
            return render_template("main.html")
    else:
        return render_template("Cartridges.html",
                               cartridges=cartridges,
                               list_models=list_models)


@cartridge_urls.route('/cartridge/<int:id>/delete')
def delete_cartridge(id):
    cartridge = Cartridges.query.get_or_404(id)
    try:
        user = "Добрынин И.А."
        action = HistoryCartridge(action="Удалён",
                                  cartridge_id=id,
                                  user=user)
        cartridge.efficiency = 0
        cartridge.status = "Удалён"
        db.session.add(action)
        db.session.add(cartridge)
        db.session.commit()
        return redirect('/cartridges')
    except:
        flash('Ошибка удаления картриджа')
        return render_template('main.html')


@cartridge_urls.route('/cartridge/<int:id>/resume')
def resume_cartridge(id):
    cartridge = Cartridges.query.get_or_404(id)
    try:
        user = "Добрынин И.А."
        action = HistoryCartridge(action="Восстановлен",
                                  cartridge_id=id,
                                  user=user)
        cartridge.efficiency = 1
        cartridge.status = "Восстановлен"
        db.session.add(action)
        db.session.add(cartridge)
        db.session.commit()
        return redirect(request.referrer)
    except:
        flash('Ошибка восстановления картриджа')
        return render_template('main.html')


@cartridge_urls.route('/deleted_cartridges')
def deleted_cartridges():
    cartridges = Cartridges.query.all()
    return render_template('DeletedCartridges.html',
                           cartridges=cartridges)


@cartridge_urls.route('/brought_a_cartridge', methods=['GET', 'POST'])
def brought_a_cartridge():
    cartridges = Cartridges.query.all()

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
                user = request.form[f'user{number}']
                cartridge = Cartridges.query.filter(Cartridges.number == number).first()

                brought_a_cartridge = BroughtACartridge(location=location,
                                                        learning_campus=learning_campus,
                                                        cabinet=cabinet,
                                                        user=user)

                cartridge.status = "Принят в заправку"
                date_of_status = HistoryCartridge(action="Принят в заправку",
                                                  user=user)
                cartridge.date_of_status.append(date_of_status)
                cartridge.brought_a_cartridge_id.append(brought_a_cartridge)

                db.session.add(brought_a_cartridge)
        else:
            location = request.form['location']
            learning_campus = request.form['learning_campus']
            cabinet = request.form['cabinet']
            user = request.form['user']

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
                date_of_status = HistoryCartridge(action="Принят в заправку",
                                                  user=user)
                cartridge.date_of_status.append(date_of_status)
                cartridge.brought_a_cartridge_id.append(brought_a_cartridge)

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
                               CartridgeIssuance=CartridgeIssuance)


@cartridge_urls.route('/refueling', methods=['GET', 'POST'])
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
                user = request.form[f'user{number}']
                cartridge = Cartridges.query.filter(Cartridges.number == number).first()
                refueling = Refueling(user=user)

                cartridge.status = "В заправке"
                date_of_status = HistoryCartridge(action="В заправке",
                                                  user=user)
                cartridge.date_of_status.append(date_of_status)
                cartridge.refueling_id.append(refueling)

                db.session.add(refueling)
        else:
            for number in cartridge_number:
                user = request.form['user']
                cartridge = Cartridges.query.filter(Cartridges.number == number).first()
                refueling = Refueling(user=user)

                cartridge.status = "В заправке"
                date_of_status = HistoryCartridge(action="В заправке",
                                                  user=user)
                cartridge.date_of_status.append(date_of_status)
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
                user = request.form[f'user{number}']
                cartridge = Cartridges.query.filter(Cartridges.number == number).first()
                reception_from_a_refueling = ReceptionFromARefueling(user=user)

                cartridge.status = "В резерве"
                date_of_status = HistoryCartridge(action="В резерве",
                                                  user=user)
                cartridge.date_of_status.append(date_of_status)
                cartridge.reception_from_a_refueling_id.append(reception_from_a_refueling)

                cartridge.work_done = False

                db.session.add(reception_from_a_refueling)
        else:
            for number in cartridge_number:
                user = request.form['user']
                cartridge = Cartridges.query.filter(Cartridges.number == number).first()
                reception_from_a_refueling = ReceptionFromARefueling(user=user)

                cartridge.status = "В резерве"
                date_of_status = HistoryCartridge(action="В резерве",
                                                  user=user)
                cartridge.date_of_status.append(date_of_status)
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
def issuance_cartridges():
    cartridges = Cartridges.query.all()

    if request.method == "POST":
        cartridge_number = request.form.getlist('cartridge_number')
        id_form = request.form['id_form']

        if len(cartridge_number) == 0:
            flash('Не выбрана ни одна модель')
            return redirect(request.referrer)

        if id_form == "2":
            for number in cartridge_number:
                user = request.form[f'user{number}']
                location = request.form[f'location{number}']
                learning_campus = request.form[f'learning_campus{number}']
                cabinet = request.form[f'cabinet{number}']
                cartridge = Cartridges.query.filter(Cartridges.number == number).first()
                issuance = CartridgeIssuance(user=user,
                                             location=location,
                                             learning_campus=learning_campus,
                                             cabinet=cabinet)

                cartridge.status = "Выдан"
                date_of_status = HistoryCartridge(action="Выдан",
                                                  user=user)
                cartridge.date_of_status.append(date_of_status)
                cartridge.issuance_id.append(issuance)

                db.session.add(issuance)
        else:
            user = request.form['user']
            location = request.form['location']
            learning_campus = request.form['learning_campus']
            cabinet = request.form['cabinet']

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

                cartridge.status = "Выдан"
                date_of_status = HistoryCartridge(action="Выдан",
                                                  user=user)
                cartridge.date_of_status.append(date_of_status)
                cartridge.issuance_id.append(issuance)

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
                               BroughtACartridge=BroughtACartridge)
