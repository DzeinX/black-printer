from models import Cartridges
from models import Printer


def IsWorkDone() -> bool:
    cartridges = Cartridges.query.all()
    printers = Printer.query.all()
    is_work_done = True
    for cartridge in cartridges:
        if not cartridge.work_done:
            is_work_done = False
            break
    for printer in printers:
        if not printer.work_done:
            is_work_done = False
            break
    return is_work_done
