# coding:utf8
"""
@author: xsren 
@contact: bestrenxs@gmail.com
@site: xsren.me

@version: 1.0
@file: __init__.py.py
@time: 25/12/2017 4:30 PM

"""

from importlib import import_module

from . import default_settings


class BaseSettings(object):
    """
    """

    def __init__(self, module=None, attributes=None):
        """
        """
        self.attributes = {}
        if module:
            self.add_module(module)
        if attributes:
            self.set_from_dict(attributes)

    def __getattr__(self, name):
        val = self.get(name)
        if val is not None:
            return val
        else:
            return self.__dict__[name]

    def __setattr__(self, name, value):
        if name.isupper():
            self.attributes[name] = value
        else:
            self.__dict__[name] = value

    def add_module(self, module):
        if isinstance(module, str):
            module = import_module(module)
        for key in dir(module):
            if key.isupper():
                self.set(key, getattr(module, key))

    def get(self, key, default_value=None):
        if not key.isupper():
            return None
        return self.attributes.get(key, default_value)

    def set(self, key, value):
        if key.isupper():
            self.attributes[key] = value

    def set_from_dict(self, attributes):
        for name, value in attributes.items():
            self.set(name, value)


class Settings(BaseSettings):
    def __init__(self, module=None, attributes=None):
        super(Settings, self).__init__(default_settings, attributes)

        if module:
            self.add_module(module)
