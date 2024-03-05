from flask import render_template, url_for
from flask import redirect
from flask import request
from flask import flash
from flask_login import login_required, logout_user, current_user
from flask_ldap3_login import AuthenticationResponseStatus
from threading import Thread

from Controller.SupportFunctions import try_to_commit

from Model.ModelController import get_current_model_controller
from Config import IsBoss
from Settings.Blueprint import AuthBlueprint
from flask_login import login_user
from Authentication.AuthManager import AuthManager, LDAPManagerAUP, LDAPManager, LDAPManagerEDU

login_manager = AuthManager().get_manager()
ldap_manager_aup = LDAPManagerAUP().get_manager()
ldap_manager_edu = LDAPManagerEDU().get_manager()

blueprint = AuthBlueprint()
auth_urls = blueprint.get_url()

# Управление базой данных
model_controller = get_current_model_controller()


@login_manager.user_loader
def load_user(pk):
    """
    Загрузка пользователя из локальной базы данных (поиск по идентификатору).
    :param pk: Идентификатор пользователя.
    :return: Объект модели пользователя.
    """
    return model_controller.filter_by_model(model_name='User',
                                            mode='first',
                                            id=pk)


@ldap_manager_aup.save_user
@ldap_manager_edu.save_user
def save_user(username, is_boss):
    """
    Сохраняет пользователя в локальной базе данных (без пароля, только логин и привилегии).
    :param username: Имя пользователя из домена.
    :param is_boss: Привилегии.
    :return: Объект модели пользователя.
    """
    user = model_controller.create(model_name='User',
                                   username=username,
                                   is_boss=is_boss)
    model_controller.add_in_session(user)
    model_controller.commit_session()
    return user


def search_in_ldap(ldap_manager, username: str, password: str, pull_result: list) -> None:
    response_status = ldap_manager.authenticate(username=username, password=password).status
    pull_result.append(False if response_status == AuthenticationResponseStatus.fail else True)


class AuthURLs:
    @staticmethod
    @auth_urls.route('/login', methods=['GET', 'POST'])
    def login_page():
        """
        Проводит аутентификацию и авторизацию пользователя.
        :return: В случае успеха переадресовывает на главную станицу,
                 иначе переадресовывает на страницу аутентификации.
        """
        if request.method == "GET":
            return render_template("Auth_urls/login.html")

        if request.method == "POST":
            username = request.form.get('login')
            password = request.form.get('password')

            results = []
            threads = []
            ldap_managers = LDAPManager.__subclasses__()
            for ldap_manager in ldap_managers:
                manager = ldap_manager().get_manager()
                thread = Thread(target=search_in_ldap, args=(manager, username, password, results))
                threads.append(thread)

            for thread in threads:
                thread.start()

            for thread in threads:
                thread.join()

            if True in results:
                user = model_controller.filter_by_model(model_name='User',
                                                        mode='first',
                                                        username=username)

                # Пользователь входит первый раз
                if user is None:
                    if username in IsBoss.BOSS_LOGIN:
                        user = save_user(username, True)
                    else:
                        user = save_user(username, False)
                    login_user(user)
                    flash("Добро пожаловать", 'success')
                    return redirect(url_for('main_urls.main_page'))

                # Пользователь уже входил, проверка на доступность привилегий (если он Босс)
                if user.username in IsBoss.BOSS_LOGIN:
                    user = model_controller.update(model_entry=user,
                                                   is_boss=True)
                    login_user(user)
                    flash("Добро пожаловать", 'success')
                    return redirect(url_for('main_urls.main_page'))

                # Пользователь уже входил, проверка на доступность привилегий (если он не Босс)
                if user.username not in IsBoss.BOSS_LOGIN:
                    user = model_controller.update(model_entry=user,
                                                   is_boss=False)
                    login_user(user)
                    flash("Добро пожаловать", 'success')
                    return redirect(url_for('main_urls.main_page'))

            flash("Не верный логин или пароль", 'warning')
            return redirect(url_for('auth_urls.login_page'))

        flash(f'Не определён метод запроса!', 'error')
        return redirect(url_for('main_urls.main_page'))

    @staticmethod
    @auth_urls.route('/logout', methods=['GET', 'POST'])
    @login_required
    def logout():
        """
        Производит выход из учётной записи пользователя.
        :return: В случае успеха переадресовывает на страницу аутентификации,
                 иначе переадресовывает на главную страницу с ошибкой.
        """
        try:
            logout_user()
        except Exception as e:
            flash(f'Не удалось выйти из учётной записи. Ошибка: {e}', 'error')
            return redirect(url_for('main_urls.main_page'))
        return redirect(url_for('auth_urls.login_page'))

    @staticmethod
    @auth_urls.route('/profile', methods=['GET', 'POST'])
    @login_required
    def profile():
        if request.method == "GET":
            current_buildings = current_user.buildings_id
            counter_buildings = len(current_buildings)
            buildings = model_controller.get_all_entries(model_name="Buildings")
            return render_template("Auth_urls/profile.html",
                                   current_buildings=current_buildings,
                                   counter_buildings=counter_buildings,
                                   buildings=buildings)

        if request.method == "POST":
            buildings_id = request.form.getlist("building")
            is_responsible_for_buildings = request.form.getlist('is_responsible_for_buildings')

            if is_responsible_for_buildings:
                model_controller.update(model_entry=current_user,
                                        is_responsible_for_buildings=False)
            else:
                model_controller.update(model_entry=current_user,
                                        is_responsible_for_buildings=True)

            new_buildings = []
            # Чтобы избежать дубликатов в БД обернул в set()
            for building_id in set(buildings_id):
                building = model_controller.get_model_by_id(model_name="Buildings",
                                                            pk=int(building_id))

                new_buildings.append(building)

            model_controller.update(model_entry=current_user,
                                    buildings_id=new_buildings)

            return try_to_commit(redirect_to='auth_urls.profile')

        flash(f'Не определён метод запроса!', 'error')
        return redirect(url_for('main_urls.main_page'))

    @staticmethod
    @auth_urls.after_request
    def redirect_to_signin(response):
        """
        Проверка на неавторизованного пользователя. Если пользователь не авторизован,
        то переадресовывает его на страницу аутентификации.
        :param response: Ответ сервера.
        :return: Переадресация на страницу аутентификации в случае неавторизованного пользователя,
                 иначе пропускает дальше (возвращает ответ сервера неизменным)
        """
        if response.status_code == 401:
            return redirect(url_for('auth_urls.login_page'))
        else:
            return response
