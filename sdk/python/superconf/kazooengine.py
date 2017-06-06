# coding=utf-8
# author=veficos

from kazoo.client import KazooClient


class KazooEngine(KazooClient):
    def __init__(self, timeout=10.0, *args, **kwargs):
        super(KazooEngine, self).__init__(timeout=timeout, *args, **kwargs)
        self.start(timeout)

    def __del__(self):
        self.stop()
