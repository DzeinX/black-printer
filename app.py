import os

from flask import Flask
from models import db
from models import ldap_manager
from models import login_manager
from cartridge_urls import cartridge_urls
from printer_urls import printer_urls
from main_urls import main_urls
from auth_urls import auth_urls
from flask_migrate import Migrate

reset_key_db = False  # Ключ на случай перезагрузки базы данных (полное удаление всей базы и создание её заново)

app = Flask(__name__)
db.init_app(app)
migration = Migrate(app, db)

BASE_DIR = __file__[:-6]
is_config = os.path.exists(str(BASE_DIR) + "Config.py")

if is_config:
    from Config import *
    app.config['SECRET_KEY'] = AppSettings.SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = AppSettings.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = AppSettings.SQLALCHEMY_TRACK_MODIFICATIONS

    app.config['LDAP_HOST'] = LDAPSettings.LDAP_HOST
    app.config['LDAP_BASE_DN'] = LDAPSettings.LDAP_BASE_DN
    app.config['LDAP_ALWAYS_SEARCH_BIND'] = True
    app.config['LDAP_USER_SEARCH_SCOPE'] = 'SUBTREE'
    app.config['LDAP_USER_RDN_ATTR'] = LDAPSettings.LDAP_USER_RDN_ATTR
    app.config['LDAP_USER_LOGIN_ATTR'] = LDAPSettings.LDAP_USER_LOGIN_ATTR
    app.config['LDAP_BIND_USER_DN'] = LDAPSettings.LDAP_BIND_USER_DN
    app.config['LDAP_BIND_USER_PASSWORD'] = LDAPSettings.LDAP_BIND_USER_PASSWORD
else:
    raise "Конфигурация не заданна... Положите файл Config.py в корень проекта (рядом с файлом app.py)."

ldap_manager.init_app(app)
login_manager.init_app(app)

with app.app_context():
    if reset_key_db:
        db.drop_all()
        db.create_all()

app.register_blueprint(cartridge_urls)
app.register_blueprint(printer_urls)
app.register_blueprint(main_urls)
app.register_blueprint(auth_urls)

if __name__ == '__main__':
    app.run(debug=True)
