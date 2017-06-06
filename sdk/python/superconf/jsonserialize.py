# coding=utf-8
# author=veficos

import os

from .serialize import Serialize


class JsonSerialize(Serialize):
    def __init__(self, local_filename='superconf.json', remote_filename='superconf.json', *args, **kwargs):
        self.local_filename = local_filename
        self.remote_filename = remote_filename
        super(JsonSerialize, self).__init__(*args, **kwargs)

    def __setitem__(self, key, value):
        if key in ['filename']:
            self.__dict__[key] = value
        else:
            super(JsonSerialize, self).__setitem__(key, value)

    def __getitem__(self, key):
        if key in ['filename']:
            return self.__dict__[key]
        return super(JsonSerialize, self).__getitem__(key)

    def guarantee(self):
        if not os.path.exists(self.local_filename):
            with open(self.local_filename, 'w') as fp:
                fp.write(self.dumps())

        if not os.path.exists(self.remote_filename):
            self.dump()

    def load(self):
        if os.path.exists(self.local_filename) and os.path.getsize(self.local_filename):
            with open(self.local_filename, 'r') as local_fp, \
                    open(self.remote_filename) as remote_fp:
                self.loads(local_fp.read())
                self.loads(remote_fp.read())

    def dump(self):
        with open(self.remote_filename, 'w') as fp:
            fp.write(self.dumps())
