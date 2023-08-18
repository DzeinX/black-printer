from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from abc import ABCMeta


db = SQLAlchemy()

association_table_1 = db.Table('association', db.Model.metadata,
                               db.Column('cartridges_id', db.Integer, db.ForeignKey('cartridges.id')),
                               db.Column('ListModels_id', db.Integer, db.ForeignKey('ListModels.id')))

association_table_2 = db.Table('association2', db.Model.metadata,
                               db.Column('user_id', db.Integer, db.ForeignKey('User.id')),
                               db.Column('building_id', db.Integer, db.ForeignKey('Buildings.id')))


class ModelInterface:
    __metaclass__ = ABCMeta
    __sql_query_amount_rows__ = ...


class AllHistory(db.Model, ModelInterface):
    __tablename__ = "AllHistory"
    __sql_query_amount_rows__ = 9
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(30), nullable=False)
    type = db.Column(db.String(30), nullable=False)
    name = db.Column(db.String(30), nullable=False)
    date = db.Column(db.DateTime)
    user = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20))
    location = db.Column(db.String(30))
    learning_campus = db.Column(db.String(30))
    cabinet = db.Column(db.String(20))

    cartridge_id = db.Column(db.Integer, db.ForeignKey("cartridges.id"))
    printer_id = db.Column(db.Integer, db.ForeignKey("printer.id"))

    def __repr__(self):
        return '<AllHistory %r>' % self.id


class Buildings(db.Model, ModelInterface):
    __tablename__ = "Buildings"
    __sql_query_amount_rows__ = 1
    id = db.Column(db.Integer, primary_key=True)
    building = db.Column(db.String(50), nullable=False, unique=True)

    def __repr__(self):
        return '<Buildings %r>' % self.id


class Division(db.Model, ModelInterface):
    __tablename__ = "Division"
    __sql_query_amount_rows__ = 1
    id = db.Column(db.Integer, primary_key=True)
    division = db.Column(db.String(50), nullable=False, unique=True)

    def __repr__(self):
        return '<Division %r>' % self.id


class Printer(db.Model, ModelInterface):
    __tablename__ = "printer"
    __sql_query_amount_rows__ = 8
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    num_inventory = db.Column(db.String(50), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, nullable=False)
    location_now = db.Column(db.String(50), nullable=False)
    learning_campus_now = db.Column(db.String(25), nullable=False)
    cabinet_now = db.Column(db.String(10), nullable=False)
    efficiency = db.Column(db.Boolean, nullable=False, default=True)
    work_done = db.Column(db.Integer, nullable=False, default=True)

    all_history_id = db.relationship("AllHistory")
    repair_id = db.relationship("Repair")
    reception_from_a_repair_id = db.relationship("ReceptionFromARepairing")
    work_done_printers_id = db.relationship("WorkListsPrinters")

    def __repr__(self):
        return '<Printer %r>' % self.id


class Cartridges(db.Model, ModelInterface):
    __tablename__ = "cartridges"
    __sql_query_amount_rows__ = 5
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, unique=True)
    date_added = db.Column(db.DateTime, nullable=False)
    efficiency = db.Column(db.Boolean, nullable=False, default=True)
    work_done = db.Column(db.Integer, nullable=False, default=0)
    refills = db.Column(db.Integer, default=0)

    all_history_id = db.relationship("AllHistory")
    cartridge_models = db.relationship("ListModels", secondary=association_table_1)
    refueling_id = db.relationship("Refueling")
    reception_from_a_refueling_id = db.relationship("ReceptionFromARefueling")
    work_done_cartridges_id = db.relationship("WorkListsCartridges")

    def __repr__(self):
        return '<cartridges %r>' % self.id


class ListModels(db.Model, ModelInterface):
    __tablename__ = "ListModels"
    __sql_query_amount_rows__ = 1
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(15), unique=True)

    def __repr__(self):
        return '<ListModels %r>' % self.id


class Refueling(db.Model, ModelInterface):
    __tablename__ = "Refueling"
    __sql_query_amount_rows__ = 2
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    user = db.Column(db.String(40), nullable=False)

    cartridge_number_id = db.Column(db.Integer, db.ForeignKey("cartridges.id"))

    def __repr__(self):
        return '<Refueling %r>' % self.id


class Repair(db.Model, ModelInterface):
    __tablename__ = "Repair"
    __sql_query_amount_rows__ = 2
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    user = db.Column(db.String(40), nullable=False)

    printer_id = db.Column(db.Integer, db.ForeignKey("printer.id"))

    def __repr__(self):
        return '<Repair %r>' % self.id


class ReceptionFromARefueling(db.Model, ModelInterface):
    __tablename__ = "ReceptionFromARefueling"
    __sql_query_amount_rows__ = 2
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    user = db.Column(db.String(40), nullable=False)

    cartridge_number_id = db.Column(db.Integer, db.ForeignKey("cartridges.id"))

    def __repr__(self):
        return '<ReceptionFromARefuelling %r>' % self.id


class ReceptionFromARepairing(db.Model, ModelInterface):
    __tablename__ = "ReceptionFromARepairing"
    __sql_query_amount_rows__ = 2
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    user = db.Column(db.String(40), nullable=False)

    printer_id = db.Column(db.Integer, db.ForeignKey("printer.id"))

    def __repr__(self):
        return '<ReceptionFromARepairing %r>' % self.id


class WorksPricesCartridges(db.Model, ModelInterface):
    __tablename__ = "WorksPricesCartridges"
    __sql_query_amount_rows__ = 1
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False)

    all_works_cartridges_id = db.Column(db.Integer, db.ForeignKey("AllWorksCartridges.id"))
    work_lists_cartridges_id = db.Column(db.Integer, db.ForeignKey("WorkListsCartridges.id"))

    def __repr__(self):
        return '<WorksPricesCartridges %r>' % self.id


class WorksPricesPrinters(db.Model, ModelInterface):
    __tablename__ = "WorksPricesPrinters"
    __sql_query_amount_rows__ = 1
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False)

    all_works_printers_id = db.Column(db.Integer, db.ForeignKey("AllWorksPrinters.id"))
    work_lists_printers_id = db.Column(db.Integer, db.ForeignKey("WorkListsPrinters.id"))

    def __repr__(self):
        return '<WorksPricesPrinters %r>' % self.id


class AllWorksPrinters(db.Model, ModelInterface):
    __tablename__ = "AllWorksPrinters"
    __sql_query_amount_rows__ = 1
    id = db.Column(db.Integer, primary_key=True)
    work = db.Column(db.String(40))

    works_prices_printers_id = db.relationship("WorksPricesPrinters")

    def __repr__(self):
        return '<AllWorksPrinters %r>' % self.id


class AllWorksCartridges(db.Model, ModelInterface):
    __tablename__ = "AllWorksCartridges"
    __sql_query_amount_rows__ = 1
    id = db.Column(db.Integer, primary_key=True)
    work = db.Column(db.String(40))

    works_prices_cartridges_id = db.relationship("WorksPricesCartridges")

    def __repr__(self):
        return '<AllWorksCartridges %r>' % self.id


class WorkListsCartridges(db.Model, ModelInterface):
    __tablename__ = "WorkListsCartridges"
    __sql_query_amount_rows__ = 2
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    user = db.Column(db.String(40), nullable=True)

    works_prices_cartridges_id = db.relationship("WorksPricesCartridges")

    cartridge_id = db.Column(db.Integer, db.ForeignKey("cartridges.id"))
    work_list = db.Column(db.Integer, db.ForeignKey('WorkList.id'))

    def __repr__(self):
        return '<WorkDoneCartridges %r>' % self.id


class WorkListsPrinters(db.Model, ModelInterface):
    __tablename__ = "WorkListsPrinters"
    __sql_query_amount_rows__ = 2
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    user = db.Column(db.String(40), nullable=True)

    works_prices_printers_id = db.relationship("WorksPricesPrinters")

    printer_id = db.Column(db.Integer, db.ForeignKey("printer.id"))
    work_list = db.Column(db.Integer, db.ForeignKey('WorkList.id'))

    def __repr__(self):
        return '<WorkDonePrinters %r>' % self.id


class WorkList(db.Model, ModelInterface):
    __tablename__ = "WorkList"
    __sql_query_amount_rows__ = 2
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date_create = db.Column(db.DateTime, nullable=False)
    date_work = db.Column(db.DateTime, nullable=False)

    check_lists_id = db.Column(db.Integer, db.ForeignKey("CheckLists.id"))

    work_list_cartridges_id = db.relationship('WorkListsCartridges')
    work_list_printers_id = db.relationship('WorkListsPrinters')

    def __repr__(self):
        return '<WorkList %r>' % self.id


class CheckLists(db.Model, ModelInterface):
    __tablename__ = "CheckLists"
    __sql_query_amount_rows__ = 4
    id = db.Column(db.Integer, primary_key=True)
    date_create = db.Column(db.DateTime, nullable=False)
    date_check = db.Column(db.DateTime, nullable=False)
    sum = db.Column(db.Integer, nullable=False)
    active = db.Column(db.Boolean, nullable=False)

    list_of_contracts_id = db.Column(db.Integer, db.ForeignKey("ListsOfContracts.id"))

    work_lists_id = db.relationship("WorkList")

    def __repr__(self):
        return '<CheckLists %r>' % self.id


class ListsOfContracts(db.Model, ModelInterface):
    __tablename__ = "ListsOfContracts"
    __sql_query_amount_rows__ = 5
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), nullable=False)
    sum = db.Column(db.Integer, nullable=False)
    date_create = db.Column(db.DateTime, nullable=False)
    date_contract = db.Column(db.DateTime, nullable=False)
    active = db.Column(db.Boolean, nullable=False)

    check_lists_id = db.relationship("CheckLists")

    def __repr__(self):
        return '<ListOfContracts %r>' % self.id


class User(UserMixin, db.Model, ModelInterface):
    __tablename__ = "User"
    __sql_query_amount_rows__ = 2
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(35), nullable=False)
    is_boss = db.Column(db.Boolean, nullable=False, default=0)
    is_admin = db.Column(db.Boolean, nullable=True, default=0)

    buildings_id = db.relationship("Buildings", secondary=association_table_2)

    def __init__(self, username, is_boss):
        self.username = username
        self.is_boss = is_boss

    def __repr__(self):
        return f'{self.id}'

    def get_id(self):
        return self.id
