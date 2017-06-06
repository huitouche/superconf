# coding=utf-8
# author=veficos

try:
    import simplejson as json
except ImportError:
    import json


class JsonFormatter(object):
    def __init__(self, intend=4):
        self.intend = intend
        self.stack = []

    @staticmethod
    def str(s):
        return '"' + s + '"'

    @staticmethod
    def unicode(s):
        return u'"' + s + u'"'

    @staticmethod
    def newline(intend, level):
        return '\n' + ' ' * intend * level

    def parse_dict(self, o=None, level=0):
        self.stack.append('{')
        level += 1
        for key, value in o.items():
            self.stack.append(''.join([
                self.newline(self.intend, level),
                self.str(str(key)) + ': '
            ]))
            self.parse(value, level)
            self.stack.append(',')

        len(o) and self.stack.pop()
        self.stack.append(''.join([
            self.newline(self.intend, level - 1), '}'
        ]))

    def parse_list(self, a=None, level=0):
        self.stack.append('[')
        level += 1
        for item in a:
            self.stack.append(self.newline(self.intend, level))
            self.parse(item, level)
            self.stack.append(',')

        len(a) and self.stack.pop()
        self.stack.append(self.newline(self.intend, level-1) + ']')

    def parse(self, o, level=0):
        if o is None:
            self.stack.append('null')
        elif o is True:
            self.stack.append('true')
        elif o is False:
            self.stack.append('false')
        elif isinstance(o, (int, float)):
            self.stack.append(str(o))
        elif isinstance(o, str):
            self.stack.append(self.str(o))
        elif isinstance(o, (list, tuple)):
            self.parse_list(o, level)
        elif isinstance(o, dict):
            self.parse_dict(o, level)
        elif isinstance(o, unicode):
            self.stack.append(self.unicode(o))
        else:
            raise Exception('invalid json type %s!' % o)

    def dump(self, o=None):
        """
        Formatting dict object

        :param o: type(dict) a dict object
        :return: type(string) json string
        """
        self.parse(o, 0)
        return ''.join(self.stack)

    def dumps(self, s=''):
        """
        Formatting dict object

        :param o: type(dict) a dict object
        :return: type(string) json string
        """
        return self.dump(json.loads(s))

