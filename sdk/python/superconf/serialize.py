# coding=utf-8
# author=veficos


try:
    import simplejson as json
except ImportError:
    import json

from collections import OrderedDict

from .jsonformatter import JsonFormatter


class Serialize(dict):
    def __init__(self, *args, **kwargs):
        super(Serialize, self).__init__(*args, **kwargs)

    def __getitem__(self, key):
        try:
            return super(Serialize, self).__getitem__(key)
        except KeyError:
            value = self[key] = Serialize()
            return value

    def __setitem__(self, key, value):
        super(Serialize, self).__setitem__(key, value)

    def loads(self, s):
        """
        Loading metadata by string

        :param s: type(string): json string
        :return:
        """
        self.update(json.loads(s))

    def dumps(self):
        """
        dump to metadata

        :return: type(string): json string
        """
        return JsonFormatter().dump(OrderedDict(self))

    def guarantee(self):
        """
        Make sure the configuration file exists

        :return: None
        """
        pass

    def load(self):
        """
        import the configuration file

        :return: None
        """
        pass

    def dump(self):
        """
        Dump to configuration file

        :return: None
        """
        pass
