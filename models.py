from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

association_table_1 = db.Table('association', db.Model.metadata,
                               db.Column('cartridges_id', db.Integer, db.ForeignKey('cartridges.id')),
                               db.Column('ListModels_id', db.Integer, db.ForeignKey('ListModels.id')))


class AllHistory(db.Model):
    __tablename__ = "AllHistory"
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(30), nullable=False)
    type = db.Column(db.String(30), nullable=False)
    name = db.Column(db.String(30), nullable=False)
    date = db.Column(db.DateTime, default=datetime.now())
    user = db.Column(db.String(20), nullable=False)

    cartridge_id = db.Column(db.Integer, db.ForeignKey("cartridges.id"))
    printer_id = db.Column(db.Integer, db.ForeignKey("printer.id"))

    def __repr__(self):
        return '<AllHistory %r>' % self.id


class Printer(db.Model):
    __tablename__ = "printer"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    num_inventory = db.Column(db.String(50), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.now())
    status = db.Column(db.String(15), nullable=False)
    location_now = db.Column(db.String(50), nullable=False)
    learning_campus_now = db.Column(db.String(25), nullable=False)
    cabinet_now = db.Column(db.String(10), nullable=False)
    efficiency = db.Column(db.Boolean, nullable=False, default=True)
    work_done = db.Column(db.Boolean, nullable=False, default=True)

    all_history_id = db.relationship("AllHistory")
    brought_a_printer_id = db.relationship("BroughtAPrinter")
    repair_id = db.relationship("Repair")
    reception_from_a_repair_id = db.relationship("ReceptionFromARepairing")
    issuance_id = db.relationship("PrinterIssuance")
    work_done_printers_id = db.relationship("WorkListsPrinters")

    def __repr__(self):
        return '<Printer %r>' % self.id


class Cartridges(db.Model):
    __tablename__ = "cartridges"
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, unique=True)
    status = db.Column(db.String(15), nullable=False)
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.now())
    efficiency = db.Column(db.Boolean, nullable=False, default=True)
    work_done = db.Column(db.Boolean, nullable=False, default=True)

    all_history_id = db.relationship("AllHistory")
    cartridge_models = db.relationship("ListModels", secondary=association_table_1)
    brought_a_cartridge_id = db.relationship("BroughtACartridge")
    refueling_id = db.relationship("Refueling")
    reception_from_a_refueling_id = db.relationship("ReceptionFromARefueling")
    issuance_id = db.relationship("CartridgeIssuance")
    work_done_cartridges_id = db.relationship("WorkListsCartridges")

    def __repr__(self):
        return '<Cartridges %r>' % self.id


class ListModels(db.Model):
    __tablename__ = "ListModels"
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(15))

    def __repr__(self):
        return '<ListModels %r>' % self.id


class BroughtACartridge(db.Model):
    __tablename__ = "BroughtACartridge"
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(15), nullable=False)
    learning_campus = db.Column(db.String(35), nullable=False)
    cabinet = db.Column(db.String(15), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now())
    user = db.Column(db.String(40), nullable=False)

    cartridge_number_id = db.Column(db.Integer, db.ForeignKey("cartridges.id"))

    def __repr__(self):
        return '<BroughtACartridge %r>' % self.id


class BroughtAPrinter(db.Model):
    __tablename__ = "BroughtAPrinter"
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(15), nullable=False)
    learning_campus = db.Column(db.String(35), nullable=False)
    cabinet = db.Column(db.String(15), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now())
    user = db.Column(db.String(40), nullable=False)

    printer_id = db.Column(db.Integer, db.ForeignKey("printer.id"))

    def __repr__(self):
        return '<BroughtAPrinter %r>' % self.id


class Refueling(db.Model):
    __tablename__ = "Refueling"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now())
    user = db.Column(db.String(40), nullable=False)

    cartridge_number_id = db.Column(db.Integer, db.ForeignKey("cartridges.id"))

    def __repr__(self):
        return '<Refueling %r>' % self.id


class Repair(db.Model):
    __tablename__ = "Repair"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now())
    user = db.Column(db.String(40), nullable=False)

    printer_id = db.Column(db.Integer, db.ForeignKey("printer.id"))

    def __repr__(self):
        return '<Repair %r>' % self.id


class ReceptionFromARefueling(db.Model):
    __tablename__ = "ReceptionFromARefueling"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now())
    user = db.Column(db.String(40), nullable=False)

    cartridge_number_id = db.Column(db.Integer, db.ForeignKey("cartridges.id"))

    def __repr__(self):
        return '<ReceptionFromARefuelling %r>' % self.id


class ReceptionFromARepairing(db.Model):
    __tablename__ = "ReceptionFromARepairing"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now())
    user = db.Column(db.String(40), nullable=False)

    printer_id = db.Column(db.Integer, db.ForeignKey("printer.id"))

    def __repr__(self):
        return '<ReceptionFromARepairing %r>' % self.id


class CartridgeIssuance(db.Model):
    __tablename__ = "CartridgeIssuance"
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(15), nullable=True)
    learning_campus = db.Column(db.String(35), nullable=True)
    cabinet = db.Column(db.String(15), nullable=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now())
    user = db.Column(db.String(40), nullable=True)

    cartridge_number_id = db.Column(db.Integer, db.ForeignKey("cartridges.id"))

    def __repr__(self):
        return '<CartridgeIssuance %r>' % self.id


class PrinterIssuance(db.Model):
    __tablename__ = "PrinterIssuance"
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(15), nullable=True)
    learning_campus = db.Column(db.String(35), nullable=True)
    cabinet = db.Column(db.String(15), nullable=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now())
    user = db.Column(db.String(40), nullable=True)

    printer_id = db.Column(db.Integer, db.ForeignKey("printer.id"))

    def __repr__(self):
        return '<PrinterIssuance %r>' % self.id


class WorksPricesCartridges(db.Model):
    __tablename__ = "WorksPricesCartridges"
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False)

    all_works_cartridges_id = db.Column(db.Integer, db.ForeignKey("AllWorksCartridges.id"))
    work_lists_cartridges_id = db.Column(db.Integer, db.ForeignKey("WorkListsCartridges.id"))

    def __repr__(self):
        return '<WorksPricesCartridges %r>' % self.id


class WorksPricesPrinters(db.Model):
    __tablename__ = "WorksPricesPrinters"
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False)

    all_works_printers_id = db.Column(db.Integer, db.ForeignKey("AllWorksPrinters.id"))
    work_lists_printers_id = db.Column(db.Integer, db.ForeignKey("WorkListsPrinters.id"))

    def __repr__(self):
        return '<WorksPricesPrinters %r>' % self.id


class AllWorksPrinters(db.Model):
    __tablename__ = "AllWorksPrinters"
    id = db.Column(db.Integer, primary_key=True)
    work = db.Column(db.String(40))

    works_prices_printers_id = db.relationship("WorksPricesPrinters")

    def __repr__(self):
        return '<AllWorksPrinters %r>' % self.id


class AllWorksCartridges(db.Model):
    __tablename__ = "AllWorksCartridges"
    id = db.Column(db.Integer, primary_key=True)
    work = db.Column(db.String(40))

    works_prices_cartridges_id = db.relationship("WorksPricesCartridges")

    def __repr__(self):
        return '<AllWorksCartridges %r>' % self.id


class WorkListsCartridges(db.Model):
    __tablename__ = "WorkListsCartridges"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now())
    user = db.Column(db.String(40), nullable=True)

    works_prices_cartridges_id = db.relationship("WorksPricesCartridges")

    cartridge_id = db.Column(db.Integer, db.ForeignKey("cartridges.id"))
    work_list = db.Column(db.Integer, db.ForeignKey('WorkList.id'))

    def __repr__(self):
        return '<WorkDoneCartridges %r>' % self.id


class WorkListsPrinters(db.Model):
    __tablename__ = "WorkListsPrinters"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now())
    user = db.Column(db.String(40), nullable=True)

    works_prices_printers_id = db.relationship("WorksPricesPrinters")

    printer_id = db.Column(db.Integer, db.ForeignKey("printer.id"))
    work_list = db.Column(db.Integer, db.ForeignKey('WorkList.id'))

    def __repr__(self):
        return '<WorkDonePrinters %r>' % self.id


class WorkList(db.Model):
    __tablename__ = "WorkList"
    id = db.Column(db.Integer, primary_key=True)
    date_create = db.Column(db.DateTime, nullable=False, default=datetime.now())
    date_work = db.Column(db.DateTime, nullable=False)

    check_lists_id = db.Column(db.Integer, db.ForeignKey("CheckLists.id"))

    work_list_cartridges_id = db.relationship('WorkListsCartridges')
    work_list_printers_id = db.relationship('WorkListsPrinters')

    def __repr__(self):
        return '<WorkList %r>' % self.id


class CheckLists(db.Model):
    __tablename__ = "CheckLists"
    id = db.Column(db.Integer, primary_key=True)
    date_create = db.Column(db.DateTime, nullable=False, default=datetime.now())
    date_check = db.Column(db.DateTime, nullable=False)
    sum = db.Column(db.Integer, nullable=False)
    active = db.Column(db.Boolean, nullable=False)

    list_of_contracts_id = db.Column(db.Integer, db.ForeignKey("ListsOfContracts.id"))

    work_lists_id = db.relationship("WorkList")

    def __repr__(self):
        return '<CheckLists %r>' % self.id


class ListsOfContracts(db.Model):
    __tablename__ = "ListsOfContracts"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), nullable=False)
    sum = db.Column(db.Integer, nullable=False)
    date_create = db.Column(db.DateTime, nullable=False, default=datetime.now())
    date_contract = db.Column(db.DateTime, nullable=False)
    active = db.Column(db.Boolean, nullable=False)

    check_lists_id = db.relationship("CheckLists")

    def __repr__(self):
        return '<ListOfContracts %r>' % self.id
