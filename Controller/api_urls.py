import json

from Controller.CreateCharts import create_chart, created_deleted_chart, refill_cycle_chart
from Model.ModelController import get_current_model_controller
from Settings.Blueprint import ApiBlueprint

blueprint = ApiBlueprint()
api_urls = blueprint.get_url()

# Управление базой данных
model_controller = get_current_model_controller()


class ApiURLs:
    @staticmethod
    @api_urls.route('/get-charts-api/', defaults={'col_amount': 6})
    @api_urls.route('/get-charts-api/cols=<int:col_amount>')
    def get_charts_api(col_amount=6):
        # TODO: Создать API ключи. Отдельная таблица в БД с зашифрованными ключами.
        #  Генерирует только босс. Нужен для стороннего доступа к графикам
        pie_chart_data = create_chart()
        c_d_chat = created_deleted_chart(col_amount)
        r_c_chart = refill_cycle_chart(col_amount)
        charts = {
            "pie_chart_data": pie_chart_data,
            "created_deleted_chart": c_d_chat,
            "refill_cycle_chart": r_c_chart
        }
        json_charts = json.dumps(charts)
        return json.loads(json_charts)
