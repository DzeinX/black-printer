from datetime import datetime

from dateutil.relativedelta import relativedelta
from Model.ModelController import ModelController
from Settings.StatusSettings import StatusSettings

model_controller = ModelController()


def create_chart() -> list:
    cartridges = model_controller.filter_by_model(model_name="Cartridges",
                                                  mode="all",
                                                  efficiency=1)
    chart_data = {
        "в резерве": 0,
        "в заправке": 0,
        "принят в заправку": 0,
        "в подразделении": 0,
        "другое": 0
    }
    if cartridges:
        for cartridge in cartridges:
            cartridge_actions = model_controller.filter_by_model(model_name="AllHistory",
                                                                 mode="all",
                                                                 cartridge_id=cartridge.id)
            cartridge_actions.sort(key=lambda c: c.date,
                                   reverse=True)
            if cartridge_actions[0].status is not None:
                last_action = cartridge_actions[0].status
                if last_action.lower() in chart_data:
                    chart_data[last_action.lower()] += 1
                else:
                    chart_data["другое"] += 1
    else:
        return [0, 0, 0, 0, 0]
    return list(chart_data.values())


def created_deleted_chart(amount_months=6) -> [int, int, int]:
    deleted_cartridges = model_controller.filter_by_model(model_name="AllHistory",
                                                          mode="all",
                                                          action="Удалён",
                                                          type="Картридж")
    created_cartridges = model_controller.filter_by_model(model_name="AllHistory",
                                                          mode="all",
                                                          action="Создан",
                                                          type="Картридж")
    data_per_month_created = {}
    data_per_month_deleted = {}
    if not deleted_cartridges and not created_cartridges:
        return [0, 0, 0]

    for i in range(amount_months - 1, -1, -1):
        date = datetime.now() - relativedelta(months=i)
        data_per_month_created[date.month] = 0
        data_per_month_deleted[date.month] = 0

    for entry in deleted_cartridges:
        month = entry.date.month
        if month in data_per_month_deleted:
            data_per_month_deleted[month] += 1

    for entry in created_cartridges:
        month = entry.date.month
        if month in data_per_month_created:
            data_per_month_created[month] += 1

    created_cartridges_data = list(data_per_month_created.values())
    deleted_cartridges_data = list(data_per_month_deleted.values())
    data_months = list(data_per_month_deleted.keys())
    return [data_months, created_cartridges_data, deleted_cartridges_data]


def refill_cycle_chart(amount_months=6) -> list:
    cartridges = model_controller.filter_by_model(model_name="Cartridges",
                                                  mode="all")
    if not cartridges:
        return [0, 0]

    permanent_actions = [
        StatusSettings.Cartridge.in_refueling,
        StatusSettings.Cartridge.in_reserve,
        StatusSettings.Cartridge.in_division,
        StatusSettings.Cartridge.accepted_for_refuel
    ]

    data_per_month = {}
    for i in range(amount_months - 1, -1, -1):
        date = datetime.now() - relativedelta(months=i)
        data_per_month[date.month] = 0

    for cartridge in cartridges:
        cartridge_actions = model_controller.filter_by_model(model_name="AllHistory",
                                                             mode="all",
                                                             cartridge_id=cartridge.id)
        statuses = [action.action for action in cartridge_actions if action.action in permanent_actions]
        dates = [action.date.month for action in cartridge_actions if action.action in permanent_actions]

        if set(permanent_actions).issubset(set(statuses)):
            while len(statuses) > 3:
                dates.pop(statuses.index(permanent_actions[0]))
                statuses.pop(statuses.index(permanent_actions[0]))

                in_reserve_date = dates.pop(statuses.index(permanent_actions[1]))
                statuses.pop(statuses.index(permanent_actions[1]))

                dates.pop(statuses.index(permanent_actions[2]))
                statuses.pop(statuses.index(permanent_actions[2]))

                dates.pop(statuses.index(permanent_actions[3]))
                statuses.pop(statuses.index(permanent_actions[3]))

                if in_reserve_date in data_per_month.keys():
                    data_per_month[in_reserve_date] += 1

    return [list(data_per_month.values()), list(data_per_month.keys())]
