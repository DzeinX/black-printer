from flask import Blueprint
from Settings.Singleton import MetaSingleton
from abc import ABCMeta, abstractmethod


class BlueprintInterface:
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_url(self): pass


class AuthBlueprint(BlueprintInterface, metaclass=MetaSingleton):
    def __init__(self):
        self.auth_urls = Blueprint('auth_urls', "auth_urls")

    def get_url(self):
        return self.auth_urls


class MainBlueprint(BlueprintInterface, metaclass=MetaSingleton):
    def __init__(self):
        self.main_urls = Blueprint('main_urls', "main_urls")

    def get_url(self):
        return self.main_urls


class CartridgeBlueprint(BlueprintInterface, metaclass=MetaSingleton):
    def __init__(self):
        self.cartridge_urls = Blueprint('cartridge_urls', "cartridge_urls")

    def get_url(self):
        return self.cartridge_urls


class PrinterBlueprint(BlueprintInterface, metaclass=MetaSingleton):
    def __init__(self):
        self.printer_urls = Blueprint('printer_urls', "printer_urls")

    def get_url(self):
        return self.printer_urls


class ApiBlueprint(BlueprintInterface, metaclass=MetaSingleton):
    def __init__(self):
        self.api_urls = Blueprint('api_urls', "api_urls")

    def get_url(self):
        return self.api_urls
