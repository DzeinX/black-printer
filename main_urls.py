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


@main_urls.route('/')
def main_page():
    return render_template("main.html",
                           is_work_done=IsWorkDone())


@main_urls.route('/all_history')
def all_history():
    statuses_in_cartridges = DateStatusCartridge.query.all()
    statuses_in_printers = DateStatusPrinter.query.all()
    cartridges = Cartridges.query.all()

    return render_template("AllHistory.html",
                           statuses_in_cartridges=statuses_in_cartridges,
                           statuses_in_printers=statuses_in_printers,
                           cartridges=cartridges,
                           Cartridges=Cartridges,
                           Printer=Printer,
                           is_work_done=IsWorkDone())


@main_urls.route('/work_done', methods=['GET', 'POST'])
def work_done():
    cartridges = Cartridges.query.all()
    printers = Printer.query.all()
    count_wd = len(
        Cartridges.query.filter(Cartridges.work_done == 0).all() + Printer.query.filter(Printer.work_done == 0).all())

    if request.method == "POST":
        count_add_c = 0
        count_add_p = 0

        num_arg = request.form['num_arg']
        date_arg = request.form['date_arg']
        cartridge_num = request.form.getlist('cartridge_num')
        num_inventory = request.form.getlist('num_inventory')

        date_arg = datetime.fromisoformat(f'{date_arg}')

        for num in cartridge_num:
            type_works_c = request.form.getlist(f'type_work{num}')
            prices_c = request.form.getlist(f'price{num}')
            user_c = request.form['user']

            var_check = TypeVar(prices_c, var_type='int')
            if var_check[1]:
                prices_c = var_check[0][0]
            else:
                if isinstance(var_check[0], str):
                    flash(var_check[0])
                    return redirect(request.referrer)
                else:
                    flash('Incorrect value')
                    return redirect(request.referrer)

            for wrk in type_works_c:
                if wrk == 'NAN':
                    prices_c.pop(type_works_c.index('NAN'))
                    type_works_c.remove('NAN')

            if not len(type_works_c) == 0 or not len(prices_c) == 0:
                if 'refuelling' in type_works_c:
                    refuelling = prices_c[type_works_c.index('refuelling')]
                else:
                    refuelling = 0

                if 'magnet_roller_rep' in type_works_c:
                    magnet_roller_rep = prices_c[type_works_c.index('magnet_roller_rep')]
                else:
                    magnet_roller_rep = 0

                if 'charge_shaft_rep' in type_works_c:
                    charge_shaft_rep = prices_c[type_works_c.index('charge_shaft_rep')]
                else:
                    charge_shaft_rep = 0

                if 'drum_rep' in type_works_c:
                    drum_rep = prices_c[type_works_c.index('drum_rep')]
                else:
                    drum_rep = 0

                if 'chip_rep' in type_works_c:
                    chip_rep = prices_c[type_works_c.index('chip_rep')]
                else:
                    chip_rep = 0

                if 'doctor_blade_rep' in type_works_c:
                    doctor_blade_rep = prices_c[type_works_c.index('doctor_blade_rep')]
                else:
                    doctor_blade_rep = 0

                sum_price = 0
                for price in prices_c:
                    sum_price += int(price)

                if not sum_price == 0:
                    cartridge = Cartridges.query.filter(Cartridges.number == num).first()

                    wdc = WorkDoneCartridges(refuelling=refuelling,
                                             magnet_roller_rep=magnet_roller_rep,
                                             charge_shaft_rep=charge_shaft_rep,
                                             drum_rep=drum_rep,
                                             chip_rep=chip_rep,
                                             doctor_blade_rep=doctor_blade_rep,
                                             sum_price=sum_price,
                                             user=user_c,
                                             num_arg=num_arg,
                                             date_arg=date_arg)

                    cartridge.work_done_cartridges_id.append(wdc)
                    cartridge.work_done = True

                    db.session.add(wdc)
                    count_add_c += 1
                else:
                    flash('Цена за услугу равна нулю')
                    return redirect(request.referrer)

        for num in num_inventory:
            type_works_p = request.form.getlist(f'type_work{num}')
            prices_p = request.form.getlist(f'price{num}')
            user_p = request.form['user']

            for wrk in type_works_p:
                if wrk == 'NAN':
                    prices_p.pop(type_works_p.index('NAN'))
                    type_works_p.remove('NAN')

            if not len(type_works_p) == 0 or not len(prices_p) == 0:
                if 'squeegee_rep' in type_works_p:
                    squeegee_rep = prices_p[type_works_p.index('squeegee_rep')]
                else:
                    squeegee_rep = 0

                if 'thermal_film_rep' in type_works_p:
                    thermal_film_rep = prices_p[type_works_p.index('thermal_film_rep')]
                else:
                    thermal_film_rep = 0

                if 'paper_feed_roller_rep' in type_works_p:
                    paper_feed_roller_rep = prices_p[type_works_p.index('paper_feed_roller_rep')]
                else:
                    paper_feed_roller_rep = 0

                sum_price = 0
                for price in prices_p:
                    sum_price += int(price)

                if not sum_price == 0:
                    printer = Printer.query.filter(Printer.num_inventory == num).first()

                    wdp = WorkDonePrinters(squeegee_rep=squeegee_rep,
                                           thermal_film_rep=thermal_film_rep,
                                           paper_feed_roller_rep=paper_feed_roller_rep,
                                           sum_price=sum_price,
                                           user=user_p,
                                           num_arg=num_arg,
                                           date_arg=date_arg)

                    printer.work_done_printers_id.append(wdp)
                    printer.work_done = True

                    db.session.add(wdp)
                    count_add_p += 1
                else:
                    flash('Цена за услугу равна нулю')
                    return redirect(request.referrer)

        try:
            if not count_add_c == 0 or not count_add_p == 0:
                db.session.commit()
                return redirect('/')
            else:
                flash('Ничего не выбрано')
                return redirect(request.referrer)
        except:
            flash('Не удалось отправить форму')
            return render_template('main.html')

    else:
        return render_template('WorkDone.html',
                               cartridges=cartridges,
                               printers=printers,
                               is_work_done=IsWorkDone(),
                               count_wd=count_wd)
