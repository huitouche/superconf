# coding=utf-8
# author=veficos

import json
import sys

from .serialize import Serialize


def _new_visitor_data(value):
    if isinstance(value, dict):
        return VisitorData(value)
    return value


def _new_visitor_path(value):
    if isinstance(value, dict):
        return VisitorPath(value)
    return value


class VisitorData(dict):
    def __init__(self, *args, **kwargs):
        super(VisitorData, self).__init__(*args, **kwargs)

    def __setitem__(self, key, value):
        raise TypeError('VisitorData object does not support item assignment')

    def __setattr__(self, key, value):
        raise TypeError('VisitorData object does not support attr assignment')

    def __getattr__(self, key):
        return _new_visitor_data(self[key])

    def get(self, key=None):
        if key:
            return _new_visitor_data(self[key])
        return dict(super(VisitorData, self).get('objects'))


class VisitorPath(dict):
    def __init__(self, *args, **kwargs):
        super(VisitorPath, self).__init__(*args, **kwargs)

    def __setitem__(self, key, value):
        raise TypeError('VisitorPath object does not support item assignment')

    def __setattr__(self, key, value):
        raise TypeError('VisitorPath object does not support attr assignment')

    def __getitem__(self, key):
        subdir = super(VisitorPath, self).get('subdir')
        if subdir and subdir.get(key) is not None:
            return _new_visitor_path(subdir[key])
        return _new_visitor_data(super(VisitorPath, self).get('objects').get(key))

    def __getattr__(self, key):
        return self.__getitem__(key)

    def __str__(self):
        return str(super(VisitorPath, self).get('objects'))

    def get(self, key=None):
        if key:
            return _new_visitor_data(super(VisitorPath, self).get('objects').get(key))
        return _new_visitor_data(super(VisitorPath, self).get('objects'))


class SuperConf(object):
    def __init__(self, serialize=None, engine=None, root=None, *args, **kwargs):
        if serialize is None:
            self._serialize = Serialize()
        else:
            self._serialize = serialize

        if root is None:
            root = ''

        self.root = list(filter(lambda x: x, root.split('.')))

        self._engine = engine

        self._serialize.guarantee()

        self._serialize.load()

    def register(self, rule, *args, **kwargs):
        """
        Register for a remote monitoring nodes
        :param rule: type(string): remote path, link '.production.write_db'
        :param args:
        :param kwargs:
        :return: type(function): decorator
        """
        def decorator(f):
            self._add_rule(rule, f, *args, **kwargs)
            return f
        return decorator

    def _add_rule(self, rule, f, *args, **kwargs):
        if not self._engine:
            return

        paths = rule.split('.')
        path = '/'.join(paths[:1] + self.root + paths[1:])

        local_node = self._serialize['remote']
        for k in filter(lambda x: x, paths):
            local_node = local_node['subdir'][k]

        @self._engine.DataWatch(path)
        def event_watch(data, stat):
            try:
                if data:
                    remote_node = json.loads(bytes.decode(data))
                    self._merger_version(remote_node,
                                         stat.version,
                                         local_node,
                                         lambda: f(_new_visitor_data(remote_node), *args, **kwargs))
            except ValueError as e:
                self._engine.logger.warning('Invalid format in upstream configure file: %s, %s', str(data), str(e))
                raise e
            except Exception as e:
                self._engine.logger.warning('Failed to update the configuration file: %s:%s', str(data), str(e))
                raise e

    def _merger_version(self, remote_node, remote_version, local_node, action):
        if isinstance(local_node['version'], dict) or remote_version > local_node['version']:
            local_node.update({
                'version': remote_version,
                'objects': remote_node
            })
            action()
            self._serialize.dump()

    def __getitem__(self, key):
        return self.__getattr__(key)

    def __getattr__(self, key):
        try:
            if key == 'remote':
                return _new_visitor_path(self._serialize[key])
            return _new_visitor_data(self._serialize[key])
        except Exception as e:
            sys.stderr.write(str(e) + '\n')
            sys.stderr.write(self._serialize.dumps() + '\n')

    def __str__(self):
        return self._serialize.dumps()
