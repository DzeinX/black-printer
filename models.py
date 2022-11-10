from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

association_table = db.Table('association', db.Model.metadata,
                             db.Column('cartridges_id', db.Integer, db.ForeignKey('cartridges.id')),
                             db.Column('ListModels_id', db.Integer, db.ForeignKey('ListModels.id'))
                             )


class Printer(db.Model):
    __tablename__ = "printer"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Integer, nullable=False)
    num_inventory = db.Column(db.Integer, nullable=False, unique=True)
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(15), nullable=False)
    location_now = db.Column(db.String(50), nullable=False)
    learning_campus_now = db.Column(db.String(25), nullable=False)
    cabinet_now = db.Column(db.String(10), nullable=False)
    efficiency = db.Column(db.Boolean, nullable=False, default=True)
    work_done = db.Column(db.Boolean, nullable=False, default=True)

    date_of_status = db.relationship("DateStatusPrinter")
    brought_a_printer_id = db.relationship("BroughtAPrinter")
    repair_id = db.relationship("Repair")
    reception_from_a_repair_id = db.relationship("ReceptionFromARepairing")
    issuance_id = db.relationship("PrinterIssuance")
    work_done_printers_id = db.relationship("WorkDonePrinters")

    def __repr__(self):
        return '<Printer %r>' % self.id


class Cartridges(db.Model):
    __tablename__ = "cartridges"
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, unique=True)
    status = db.Column(db.String(15), nullable=False)
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    efficiency = db.Column(db.Boolean, nullable=False, default=True)
    work_done = db.Column(db.Boolean, nullable=False, default=True)

    date_of_status = db.relationship("DateStatusCartridge")
    cartridge_models = db.relationship("ListModels", secondary=association_table)
    brought_a_cartridge_id = db.relationship("BroughtACartridge")
    refueling_id = db.relationship("Refueling")
    reception_from_a_refueling_id = db.relationship("ReceptionFromARefueling")
    issuance_id = db.relationship("CartridgeIssuance")
    work_done_cartridges_id = db.relationship("WorkDoneCartridges")

    def __repr__(self):
        return '<Cartridges %r>' % self.id


class DateStatusPrinter(db.Model):
    __tablename__ = "DateStatusPrinter"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(15), nullable=False)
    user = db.Column(db.String(25))

    printer_id = db.Column(db.Integer, db.ForeignKey("printer.id"))

    def __repr__(self):
        return '<DateStatusPrinter %r>' % self.id


class DateStatusCartridge(db.Model):
    __tablename__ = "DateStatusCartridge"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(15), nullable=False)
    user = db.Column(db.String(25))  # Пользователь, который обновил статус

    cartridge_id = db.Column(db.Integer, db.ForeignKey("cartridges.id"))

    def __repr__(self):
        return '<DateStatusCartridge %r>' % self.id


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
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
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
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user = db.Column(db.String(40), nullable=False)

    printer_id = db.Column(db.Integer, db.ForeignKey("printer.id"))

    def __repr__(self):
        return '<BroughtAPrinter %r>' % self.id


class Refueling(db.Model):
    __tablename__ = "Refueling"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user = db.Column(db.String(40), nullable=False)

    cartridge_number_id = db.Column(db.Integer, db.ForeignKey("cartridges.id"))

    def __repr__(self):
        return '<Refueling %r>' % self.id


class Repair(db.Model):
    __tablename__ = "Repair"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user = db.Column(db.String(40), nullable=False)

    printer_id = db.Column(db.Integer, db.ForeignKey("printer.id"))

    def __repr__(self):
        return '<Repair %r>' % self.id


class ReceptionFromARefueling(db.Model):
    __tablename__ = "ReceptionFromARefueling"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user = db.Column(db.String(40), nullable=False)

    cartridge_number_id = db.Column(db.Integer, db.ForeignKey("cartridges.id"))

    def __repr__(self):
        return '<ReceptionFromARefuelling %r>' % self.id


class ReceptionFromARepairing(db.Model):
    __tablename__ = "ReceptionFromARepairing"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
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
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
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
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user = db.Column(db.String(40), nullable=True)

    printer_id = db.Column(db.Integer, db.ForeignKey("printer.id"))

    def __repr__(self):
        return '<PrinterIssuance %r>' % self.id


class WorkDoneCartridges(db.Model):
    __tablename__ = "WorkDoneCartridges"
    id = db.Column(db.Integer, primary_key=True)
    refuelling = db.Column(db.Float, nullable=False, default=0)
    magnet_roller_rep = db.Column(db.Float, nullable=False, default=0)
    charge_shaft_rep = db.Column(db.Float, nullable=False, default=0)
    drum_rep = db.Column(db.Float, nullable=False, default=0)
    chip_rep = db.Column(db.Float, nullable=False, default=0)
    doctor_blade_rep = db.Column(db.Float, nullable=False, default=0)
    sum_price = db.Column(db.Float, nullable=False, default=0)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user = db.Column(db.String(40), nullable=True)

    cartridge_id = db.Column(db.Integer, db.ForeignKey("cartridges.id"))

    def __repr__(self):
        return '<WorkDoneCartridges %r>' % self.id


class WorkDonePrinters(db.Model):
    __tablename__ = "WorkDonePrinters"
    id = db.Column(db.Integer, primary_key=True)
    squeegee_rep = db.Column(db.Float, nullable=False, default=0)
    thermal_film_rep = db.Column(db.Float, nullable=False, default=0)
    paper_feed_roller_rep = db.Column(db.Float, nullable=False, default=0)
    sum_price = db.Column(db.Float, nullable=False, default=0)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user = db.Column(db.String(40), nullable=True)

    cartridge_id = db.Column(db.Integer, db.ForeignKey("printer.id"))

    def __repr__(self):
        return '<WorkDonePrinters %r>' % self.id
