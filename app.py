from flask import Flask

from Authentication.AuthManager import AuthInterface

# Не удалять, нужно для корректного запуска
from Controller.printer_urls import *
from Controller.cartridge_urls import *
from Controller.auth_urls import *
from Controller.main_urls import *
from Controller.api_urls import *

from Settings.Blueprint import BlueprintInterface

from flask_migrate import Migrate
from Config import *
from Model.models import db


class APP:
    def __init__(self, data_base):
        self.db = data_base

        # Ключ на случай перезагрузки базы данных (полное удаление всей базы и создание её заново)
        self.__reset_key_db = False

        self.app = Flask(import_name=__name__,
                         template_folder='templates')

        self.app.config['SECRET_KEY'] = AppSettings.SECRET_KEY
        self.app.config['SQLALCHEMY_DATABASE_URI'] = AppSettings.SQLALCHEMY_DATABASE_URI
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = AppSettings.SQLALCHEMY_TRACK_MODIFICATIONS

        self.db.init_app(self.app)
        self.migration = Migrate(self.app, self.db, render_as_batch=True)

        # self.get_config()
        self.register_blueprints()
        self.init_auth()
        self.check_rest_key_db()

    def get_config_aup(self):
        self.app.config['LDAP_HOST'] = LDAPSettings.AUP_LDAP_HOST
        self.app.config['LDAP_BASE_DN'] = LDAPSettings.AUP_LDAP_BASE_DN
        self.app.config['LDAP_ALWAYS_SEARCH_BIND'] = LDAPSettings.AUP_LDAP_ALWAYS_SEARCH_BIND
        self.app.config['LDAP_USER_SEARCH_SCOPE'] = LDAPSettings.AUP_LDAP_USER_SEARCH_SCOPE
        self.app.config['LDAP_USER_RDN_ATTR'] = LDAPSettings.AUP_LDAP_USER_RDN_ATTR
        self.app.config['LDAP_USER_LOGIN_ATTR'] = LDAPSettings.AUP_LDAP_USER_LOGIN_ATTR
        self.app.config['LDAP_BIND_USER_DN'] = LDAPSettings.AUP_LDAP_BIND_USER_DN
        self.app.config['LDAP_BIND_USER_PASSWORD'] = LDAPSettings.AUP_LDAP_BIND_USER_PASSWORD

    def get_config_edu(self):
        self.app.config['LDAP_HOST'] = LDAPSettings.EDU_LDAP_HOST
        self.app.config['LDAP_BASE_DN'] = LDAPSettings.EDU_LDAP_BASE_DN
        self.app.config['LDAP_ALWAYS_SEARCH_BIND'] = LDAPSettings.EDU_LDAP_ALWAYS_SEARCH_BIND
        self.app.config['LDAP_USER_SEARCH_SCOPE'] = LDAPSettings.EDU_LDAP_USER_SEARCH_SCOPE
        self.app.config['LDAP_USER_RDN_ATTR'] = LDAPSettings.EDU_LDAP_USER_RDN_ATTR
        self.app.config['LDAP_USER_LOGIN_ATTR'] = LDAPSettings.EDU_LDAP_USER_LOGIN_ATTR
        self.app.config['LDAP_BIND_USER_DN'] = LDAPSettings.EDU_LDAP_BIND_USER_DN
        self.app.config['LDAP_BIND_USER_PASSWORD'] = LDAPSettings.EDU_LDAP_BIND_USER_PASSWORD

    # НОВЫЕ КОНФИГИ ПИСАТЬ ТУТ

    def init_auth(self):
        subclasses = AuthInterface.__subclasses__()
        methods = list(dir(self))[30:]
        configs = []
        for method in methods:
            if "get_config" in method:
                configs.append(method)

        for index, subclass in enumerate(subclasses):
            manager = subclass()
            for config in configs:
                if manager.domain.upper() in config.upper():
                    getattr(self, config)()
                    manager.get_manager().init_app(self.app)
                if manager.domain == "":
                    manager.get_manager().init_app(self.app)

    def check_rest_key_db(self):
        with self.app.app_context():
            if self.__reset_key_db:
                self.db.drop_all()
                self.db.create_all()

    def register_blueprints(self):
        subclasses = BlueprintInterface.__subclasses__()
        for subclass in subclasses:
            blueprint = subclass()
            self.app.register_blueprint(blueprint.get_url())


application = APP(data_base=db)
app = application.app

if __name__ == '__main__':
    app.run(debug=True)
