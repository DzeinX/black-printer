from sqlalchemy import desc

from Settings.Singleton import MetaSingleton
from Model.models import ModelInterface
from Model.models import db
from sqlalchemy.sql import text


class ModelController(metaclass=MetaSingleton):
    def __init__(self):
        self.models = dict()
        subclasses = ModelInterface.__subclasses__()
        for model in subclasses:
            self.models[self._get_model_name(model)] = model

    def create(self, model_name: str, **params) -> ModelInterface or None:
        name, model = self._get_model(model_name)
        if self._is_model_none(model):
            return None
        return model(**params)

    def update(self, model_entry: ModelInterface, **params) -> ModelInterface:
        for name, value in params.items():
            setattr(model_entry, name, value)
        self._commit(model_entry)
        return model_entry

    def get_model_by_id(self, model_name: str, pk: int) -> ModelInterface or None:
        _, model = self._get_model(model_name)
        if self._is_model_none(model):
            return None
        return model.query.get(pk)

    def filter_by_model(self, model_name: str, mode: str, **filters) -> ModelInterface or None:
        """
        :param model_name:
        :param mode: 'all' or 'first' required else return None
        :param filters:
        :return:
        """
        _, model = self._get_model(model_name)
        if self._is_model_none(model):
            return None
        filter_args = [text(f'{self._get_model_name(model)}.{row} == "{k}"') for row, k in filters.items()]
        if mode == "all":
            filter_entry = model.query.filter(*filter_args).all()
        elif mode == "first":
            filter_entry = model.query.filter(*filter_args).first()
        else:
            return None
        return filter_entry

    def filter_two_or(self, model_name: str, row: str, *filters) -> ModelInterface or None:
        """
        :param model_name:
        :param row:
        :param filters:
        :return:
        """
        if len(filters) == 2:
            _, model = self._get_model(model_name)
            if self._is_model_none(model):
                return None
            filter_args = text(f'({self._get_model_name(model)}.{row} == "{filters[0]}") | ({self._get_model_name(model)}.{row} == "{filters[1]}")')
            return model.query.filter(filter_args).order_by(desc(model.date))
        return None

    def filter_by_model_with_paginate(self, model_name: str, page: int, per_page: int, **filters) -> ModelInterface or None:
        """
        :param model_name:
        :param page:
        :param per_page:
        :param filters:
        :return:
        """
        _, model = self._get_model(model_name)
        if self._is_model_none(model):
            return None
        filter_args = [text(f'{self._get_model_name(model)}.{row} == "{k}"') for row, k in filters.items()]
        return model.query.filter(*filter_args).order_by(desc(model.date)).paginate(page, per_page, error_out=False)

    def filter_two_or_with_paginate(self, model_name: str, page: int, per_page: int, row: str, *filters) -> ModelInterface or None:
        """
        :param model_name:
        :param page:
        :param per_page:
        :param row:
        :param filters:
        :return:
        """
        if len(filters) == 2:
            _, model = self._get_model(model_name)
            if self._is_model_none(model):
                return None
            filter_args = text(f'({self._get_model_name(model)}.{row} == "{filters[0]}") | ({self._get_model_name(model)}.{row} == "{filters[1]}")')
            return model.query.filter(filter_args).order_by(desc(model.date)).paginate(page, per_page, error_out=False)
        return None

    def delete_all_entries_in_model(self, model_name: str):
        _, model = self._get_model(model_name)
        model.query.delete()

    @staticmethod
    def delete_entry(model_entry: ModelInterface):
        db.session.delete(model_entry)
        db.session.commit()

    def get_all_entries(self, model_name: str) -> list:
        _, model = self._get_model(model_name)
        return list(model.query.all())

    def get_all_entries_with_order(self, model_name: str) -> list:
        _, model = self._get_model(model_name)
        return model.query.order_by(desc(model.date))

    def get_all_entries_with_paginate(self, model_name: str, page: int, per_page: int) -> list:
        _, model = self._get_model(model_name)
        return model.query.order_by(desc(model.date)).paginate(page, per_page, error_out=False)

    def _get_model(self, model_name: str) -> (str, ModelInterface) or (None, None):
        model_name = model_name.lower()
        for key, model in self.models.items():
            if key.lower() == model_name:
                return key, model
        return None, None

    @staticmethod
    def add_in_session(model_entry: ModelInterface):
        db.session.add(model_entry)

    @staticmethod
    def commit_session():
        db.session.commit()

    @staticmethod
    def _get_model_name(model) -> str:
        return dict(model.__dict__)['__tablename__']

    @staticmethod
    def _commit(*models):
        for model in models:
            db.session.add(model)
        db.session.commit()

    @staticmethod
    def _is_model_none(model) -> bool:
        if model is None:
            return True
        return False
