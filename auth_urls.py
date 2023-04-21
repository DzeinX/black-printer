from flask import render_template
from flask import redirect
from flask import request
from flask import flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from flask_ldap3_login import AuthenticationResponseStatus
from flask import Blueprint
from models import *
from app import ldap_manager

auth_urls = Blueprint('auth_urls', __name__)


@auth_urls.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == "POST":
        username = request.form.get('login')
        password = request.form.get('password')

        new_user = ldap_manager.authenticate(username=username, password=password)

        if new_user.status != AuthenticationResponseStatus.fail:
            user = User.query.filter(User.username == username).first()
            if user is None:
                user = save_user(new_user.user_dn, username, False)
            login_user(user)
            return redirect('/')
        flash("Не верный логин или пароль")
        return redirect('/login')

    else:
        return render_template("login.html")


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
