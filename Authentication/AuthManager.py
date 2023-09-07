from abc import ABCMeta, abstractmethod
from flask_login import LoginManager
from Settings.Singleton import MetaSingleton
from flask_ldap3_login import LDAP3LoginManager


class AuthInterface:
    __metaclass__ = ABCMeta
    domain = None

    @abstractmethod
    def get_manager(self): pass


class AuthManager(AuthInterface, metaclass=MetaSingleton):
    def __init__(self):
        self.manager = LoginManager()
        self.domain = ""

    def get_manager(self):
        return self.manager


class LDAPManager:
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_manager(self): pass


class LDAPManagerAUP(AuthInterface, LDAPManager, metaclass=MetaSingleton):
    def __init__(self):
        self.manager = LDAP3LoginManager()
        self.domain = "AUP"

    def get_manager(self):
        return self.manager


class LDAPManagerEDU(AuthInterface, LDAPManager, metaclass=MetaSingleton):
    def __init__(self):
        self.manager = LDAP3LoginManager()
        self.domain = "EDU"

    def get_manager(self):
        return self.manager
