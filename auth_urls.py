from flask import render_template, url_for
from flask import redirect
from flask import request
from flask import flash
from flask_login import login_user, login_required, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from flask import Blueprint
from models import *

auth_urls = Blueprint('auth_urls', __name__)


@auth_urls.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == "POST":
        login = request.form.get('login')
        password = request.form.get('password')

        user = User.query.filter_by(login=login).first()

        if not user:
            flash("Неверный логин или пароль")
            return redirect('/login')

        if check_password_hash(user.password, password):
            login_user(user)
            return redirect('/')
        else:
            flash("Неверный логин или пароль")
            return redirect('/login')
    else:
        return render_template("login.html")


@auth_urls.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        login = request.form.get('login')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        check_login = User.query.filter_by(login=login).first()

        if not check_login:
            if password1 == password2:
                password = password1

                if not(login or password):
                    flash('Заполните поля')
                    redirect("/register")
                else:
                    hash_pwd = generate_password_hash(password)

                    new_user = User(login=login, password=hash_pwd)
                    db.session.add(new_user)
                    db.session.commit()

                    flash("Пользователь зарегистрирован успешно")
                    return redirect('/login')
            else:
                flash("Пароли не совпадают")
                return redirect("/register")
        else:
            flash("Такой пользователь уже существует")
            return redirect("/register")
    else:
        return render_template('Register.html')


@auth_urls.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect('/login')


@auth_urls.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        return redirect('/login')
    else:
        return response
