from flask import Flask
from models import db
from models import manager
from cartridge_urls import cartridge_urls
from printer_urls import printer_urls
from main_urls import main_urls
from auth_urls import auth_urls
from flask_migrate import Migrate


reset_key_db = False  # Ключ на случай перезагрузки базы данных (полное удаление всей базы и создание её заново)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'jkmhclahu282dh2ouho79g287gy'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///printersDB.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
manager.init_app(app)
migration = Migrate(app, db)

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
