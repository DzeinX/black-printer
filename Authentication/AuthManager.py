from abc import ABCMeta, abstractmethod
from flask_login import LoginManager
from Settings.Singleton import MetaSingleton
from flask_ldap3_login import LDAP3LoginManager


class AuthInterface:
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_manager(self): pass


class AuthManager(AuthInterface, metaclass=MetaSingleton):
    def __init__(self):
        self.manager = LoginManager()

    def get_manager(self):
        return self.manager


class LDAPManagerAUP(AuthInterface, metaclass=MetaSingleton):
    def __init__(self):
        self.manager = LDAP3LoginManager()

    def get_manager(self):
        return self.manager


class LDAPManagerEDU(AuthInterface, metaclass=MetaSingleton):
    def __init__(self):
        self.manager = LDAP3LoginManager()

    def get_manager(self):
        return self.manager
