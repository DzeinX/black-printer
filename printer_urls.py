from flask import render_template
from flask import redirect
from flask import request
from flask import Blueprint
from flask import flash
from models import *
from tabs_that_appear import *
from ScanFunctions import TypeVar


printer_urls = Blueprint('printer_urls', __name__)


@printer_urls.route('/add_works_printers', methods=['GET', 'POST'])
def add_works_printers():
    all_works_printers = AllWorksPrinters.query.all()
    counter_works = len(all_works_printers)

    if request.method == "POST":
        all_works_printers = request.form.getlist('works')

        var_check = TypeVar(all_works_printers, var_type='str')
        if var_check[1]:
            all_works_printers = var_check[0][0]
        else:
            if isinstance(var_check[0], str):
                flash(var_check[0])
                return redirect(request.referrer)
            else:
                flash('Incorrect value')
                return redirect(request.referrer)

        if len(all_works_printers) == 0:
            flash('Нельзя удалить все модели')
            return redirect(request.referrer)

        AllWorksPrinters.query.delete()
        try:
            for work in all_works_printers:

                if work != '' and not work.isspace():
                    model = AllWorksPrinters(work=work)
                    db.session.add(model)
        except:
            return f"Не удалось сохранить изменения"

        try:
            db.session.commit()
            return redirect("/add_works_printers")
        except:
            flash('Не удалось добавить тип работ')
            return render_template("main.html")
    else:
        return render_template("AddWorksPrinters.html",
                               all_works_printers=all_works_printers,
                               counter_works=counter_works)


@printer_urls.route('/printer/<int:id>/update', methods=['GET', 'POST'])
def update_printer(id):
    printer = Printer.query.get(id)

    if request.method == "POST":
        name = request.form['name']
        num_inventory = request.form['num_inventory']
        location = request.form['location']
        learning_campus = request.form['learning_campus']
        cabinet = request.form['cabinet']

        var_check = TypeVar(name, num_inventory, location, learning_campus, cabinet, var_type='str')
        if var_check[1]:
            printer.name = var_check[0][0]
            printer.num_inventory = var_check[0][1]
            printer.location_now = var_check[0][2]
            printer.learning_campus_now = var_check[0][3]
            printer.cabinet_now = var_check[0][4]
        else:
            if isinstance(var_check[0], str):
                flash(var_check[0])
                return redirect(request.referrer)
            else:
                flash('Incorrect value')
                return redirect(request.referrer)

        try:
            db.session.commit()
            return redirect('/printers')
        except:
            flash('При обновлении принтера произошла ошибка')
            return render_template("main.html")
    else:
        return render_template("printer_update.html",
                               printer=printer)


@printer_urls.route('/printers', methods=['GET', 'POST'])
def printers():
    printers = Printer.query.order_by(Printer.date_added.desc()).all()

    if request.method == 'POST':
        name = request.form['name']
        num_inventory = request.form['num_inventory']
        location = request.form['location']
        learning_campus = request.form['learning_campus']
        cabinet = request.form['cabinet']

        var_check = TypeVar(name, num_inventory, location, learning_campus, cabinet, var_type='str')
        if var_check[1]:
            name = var_check[0][0]
            num_inventory = var_check[0][1]
            location_now = var_check[0][2]
            learning_campus_now = var_check[0][3]
            cabinet_now = var_check[0][4]
        else:
            if isinstance(var_check[0], str):
                flash(var_check[0])
                return redirect(request.referrer)
            else:
                flash('Incorrect value')
                return redirect(request.referrer)

        status = "Добавлен"
        user = request.form['user']
        date_of_status = DateStatusPrinter(status=status,
                                           user=user)

        printer = Printer(name=name,
                          num_inventory=num_inventory,
                          location_now=location_now,
                          learning_campus_now=learning_campus_now,
                          cabinet_now=cabinet_now,
                          status=status)

        printer.date_of_status.append(date_of_status)

        try:
            db.session.add(printer)
            db.session.commit()
            return redirect('/printers')
        except:
            flash('При добавлении принтера произошла ошибка')
            return render_template("main.html")

    return render_template("Printers.html",
                           printers=printers)


@printer_urls.route('/printer/<int:id>/statuses')
def printers_status(id):
    statuses = DateStatusPrinter.query.order_by(DateStatusPrinter.date.desc()).all()
    printer = Printer.query.get(id)
    return render_template("PrinterStatuses.html",
                           statuses=statuses,
                           id=id,
                           printer=printer)


@printer_urls.route('/printer/<int:id>/delete')
def delete_printer(id):
    printer = Printer.query.get_or_404(id)
    try:
        user = "Добрынин И.А."
        status = DateStatusPrinter(status="Удалён",
                                   printer_id=id,
                                   user=user)
        printer.efficiency = 0
        printer.status = "Удалён"
        db.session.add(status)
        db.session.add(printer)
        db.session.commit()
        return redirect('/printers')
    except:
        flash('Ошибка удаления принтера')
        return render_template('main.html')


@printer_urls.route('/printer/<int:id>/resume')
def resume_printer(id):
    printer = Printer.query.get_or_404(id)
    try:
        user = "Добрынин И.А."
        status = DateStatusPrinter(status="Восстановлен",
                                   printer_id=id,
                                   user=user)
        printer.efficiency = 1
        printer.status = "Восстановлен"
        db.session.add(status)
        db.session.add(printer)
        db.session.commit()
        return redirect(request.referrer)
    except:
        flash('Ошибка восстановления принтера')
        return render_template('main.html')


@printer_urls.route('/deleted_printers')
def deleted_printers():
    printers = Printer.query.all()

    return render_template('DeletedPrinters.html',
                           printers=printers)


@printer_urls.route('/brought_a_printer', methods=['GET', 'POST'])
def brought_a_printer():
    printers = Printer.query.all()

    if request.method == "POST":
        printer_num = request.form.getlist('num_inventory')
        id_form = request.form['id_form']

        if len(printer_num) == 0:
            flash('Не выбрана ни одна модель')
            return redirect(request.referrer)

        if id_form == "2":
            for number in printer_num:
                location = request.form[f'location{number}']
                learning_campus = request.form[f'learning_campus{number}']
                cabinet = request.form[f'cabinet{number}']
                user = request.form[f'user{number}']
                printer = Printer.query.filter(Printer.num_inventory == number).first()

                brought_a_printer = BroughtAPrinter(location=location,
                                                    learning_campus=learning_campus,
                                                    cabinet=cabinet,
                                                    user=user)

                printer.status = "Принят в ремонт"
                date_of_status = DateStatusPrinter(status="Принят в ремонт",
                                                   user=user)
                printer.date_of_status.append(date_of_status)
                printer.brought_a_printer_id.append(brought_a_printer)

                db.session.add(brought_a_printer)
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

            for number in printer_num:

                printer = Printer.query.filter(Printer.num_inventory == number).first()

                brought_a_printer = BroughtAPrinter(location=location,
                                                    learning_campus=learning_campus,
                                                    cabinet=cabinet,
                                                    user=user)

                printer.status = "Принят в ремонт"
                date_of_status = DateStatusPrinter(status="Принят в ремонт",
                                                   user=user)
                printer.date_of_status.append(date_of_status)
                printer.brought_a_printer_id.append(brought_a_printer)

                db.session.add(brought_a_printer)

        try:
            db.session.commit()
            return redirect('/printers')
        except:
            flash('Не удалось отправить форму')
            return render_template("main.html")

    else:
        return render_template('BroughtAPrinter.html',
                               printers=printers,
                               PrinterIssuance=PrinterIssuance)


@printer_urls.route('/repairing', methods=['GET', 'POST'])
def repairing():
    printers = Printer.query.all()

    if request.method == "POST":
        id_form = request.form['id_form']
        printer_num = request.form.getlist('num_inventory')

        if len(printer_num) == 0:
            flash('Не выбрана ни одна модель')
            return redirect(request.referrer)

        if id_form == '2':
            for number in printer_num:
                user = request.form[f'user{number}']
                printer = Printer.query.filter(Printer.num_inventory == number).first()
                repair = Repair(user=user)

                printer.status = "В ремонте"
                date_of_status = DateStatusPrinter(status="В ремонте",
                                                   user=user)
                printer.date_of_status.append(date_of_status)
                printer.repair_id.append(repair)

                db.session.add(repair)
        else:
            for number in printer_num:
                user = request.form['user']
                printer = Printer.query.filter(Printer.num_inventory == number).first()
                repair = Repair(user=user)

                printer.status = "В ремонте"
                date_of_status = DateStatusPrinter(status="В ремонте",
                                                   user=user)
                printer.date_of_status.append(date_of_status)
                printer.repair_id.append(repair)

                db.session.add(repair)

        try:
            db.session.commit()
            return redirect('/printers')
        except:
            flash('Не удалось отправить форму')
            return render_template("main.html")
    else:
        return render_template('Repairing.html',
                               printers=printers)


@printer_urls.route('/reception_from_a_repairing', methods=['GET', 'POST'])
def receptionFromARepairing():
    printers = Printer.query.all()

    if request.method == "POST":
        id_form = request.form['id_form']
        printer_num = request.form.getlist('num_inventory')

        if len(printer_num) == 0:
            flash('Не выбрана ни одна модель')
            return redirect(request.referrer)

        if id_form == '2':
            for number in printer_num:
                user = request.form[f'user{number}']
                printer = Printer.query.filter(Printer.num_inventory == number).first()
                reception_from_a_repairing = ReceptionFromARepairing(user=user)

                printer.status = "Получен из ремонта"
                date_of_status = DateStatusPrinter(status="Получен из ремонта",
                                                   user=user)
                printer.date_of_status.append(date_of_status)
                printer.reception_from_a_repair_id.append(reception_from_a_repairing)

                printer.work_done = False

                db.session.add(reception_from_a_repairing)
        else:
            for number in printer_num:
                user = request.form[f'user']
                printer = Printer.query.filter(Printer.num_inventory == number).first()
                reception_from_a_repairing = ReceptionFromARepairing(user=user)

                printer.status = "Получен из ремонта"
                date_of_status = DateStatusPrinter(status="Получен из ремонта",
                                                   user=user)
                printer.date_of_status.append(date_of_status)
                printer.reception_from_a_repair_id.append(reception_from_a_repairing)

                printer.work_done = False

                db.session.add(reception_from_a_repairing)

        try:
            db.session.commit()
            return redirect('/printers')
        except:
            flash('Не удалось отправить форму')
            return render_template("main.html")
    else:
        return render_template('ReceptionFromARepair.html',
                               printers=printers)


@printer_urls.route('/issuance_printers', methods=['GET', 'POST'])
def issuance_printers():
    printers = Printer.query.all()

    if request.method == "POST":
        printer_num = request.form.getlist('num_inventory')
        id_form = request.form['id_form']

        if len(printer_num) == 0:
            flash('Не выбрана ни одна модель')
            return redirect(request.referrer)

        if id_form == "2":
            for number in printer_num:
                user = request.form[f'user{number}']
                location = request.form[f'location{number}']
                learning_campus = request.form[f'learning_campus{number}']
                cabinet = request.form[f'cabinet{number}']
                printer = Printer.query.filter(Printer.num_inventory == number).first()

                printer.location_now = location
                printer.learning_campus_now = learning_campus
                printer.cabinet_now = cabinet

                issuance = PrinterIssuance(user=user,
                                           location=location,
                                           learning_campus=learning_campus,
                                           cabinet=cabinet)

                printer.status = "В подразделении"
                date_of_status = DateStatusPrinter(status="В подразделении",
                                                   user=user)
                printer.date_of_status.append(date_of_status)
                printer.issuance_id.append(issuance)

                db.session.add(issuance)
        else:
            user = request.form[f'user']
            location = request.form[f'location']
            learning_campus = request.form[f'learning_campus']
            cabinet = request.form[f'cabinet']

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

            for number in printer_num:

                printer = Printer.query.filter(Printer.num_inventory == number).first()

                printer.location_now = location
                printer.learning_campus_now = learning_campus
                printer.cabinet_now = cabinet

                issuance = PrinterIssuance(user=user,
                                           location=location,
                                           learning_campus=learning_campus,
                                           cabinet=cabinet)

                printer.status = "В подразделении"
                date_of_status = DateStatusPrinter(status="В подразделении",
                                                   user=user)
                printer.date_of_status.append(date_of_status)
                printer.issuance_id.append(issuance)

                db.session.add(issuance)

        try:
            db.session.commit()
            return redirect('/printers')
        except:
            flash('Не удалось отправить форму')
            return render_template("main.html")
    else:
        return render_template('IssuancePrinters.html',
                               printers=printers,
                               BroughtAPrinter=BroughtAPrinter)
