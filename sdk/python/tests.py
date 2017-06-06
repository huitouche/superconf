# coding=utf-8
# author=veficos


from superconf.superconf import SuperConf
from superconf.kazooengine import KazooEngine
from superconf.jsonserialize import JsonSerialize
from superconf.jsonformatter import JsonFormatter
from superconf.engine import Engine

import unittest
import os
import time


class TestSuperConf(unittest.TestCase):

    def test_local(self):
        conf = SuperConf(serialize=JsonSerialize(),
                         engine=Engine())

        self.assertTrue(conf.local.deploy == 'dev')
        self.assertTrue(conf.local.zookeeper == {'host': '127.0.0.1:31081,127.0.0.1:31082'})
        self.assertTrue(conf.local.zookeeper.host == '127.0.0.1:31081,127.0.0.1:31082')

    def test_remote(self):
        conf = SuperConf(serialize=JsonSerialize(remote_filename=''.join([str(os.getpid()), '-', 'superconf.json'])),
                            engine=KazooEngine(
                                hosts=SuperConf(JsonSerialize(), engine=Engine()).local.zookeeper.host
                            ), root='superconf')

        @conf.register('.union.mysql.read_db')
        def __read_db(cfg):
            self.assertTrue(cfg == {
                "charset": "utf8mb4",
                "host": "127.0.0.1",
                "port": 3306,
                "database": "test",
                "maxConnections": 3,
                "minFreeConnections": 1,
                "user": "root",
                "password": "",
            })

        @conf.register('.union.mysql.write_db')
        def __write_db(cfg):
            self.assertTrue(cfg == {
                "charset": "utf8mb4",
                "host": "127.0.0.1",
                "port": 3306,
                "database": "test",
                "maxConnections": 3,
                "minFreeConnections": 1,
                "user": "root",
                "password": "",
            })

        self.assertTrue(conf.local.deploy == 'dev')
        self.assertTrue(conf.local.zookeeper == {'host': '127.0.0.1:31081,127.0.0.1:31082'})
        self.assertTrue(conf.local.zookeeper.host == '127.0.0.1:31081,127.0.0.1:31082')
        time.sleep(0.5)
        self.assertTrue(conf.remote.union.mysql.read_db == {
            'charset': 'utf8mb4',
            'host': '127.0.0.1',
            'port': 3306,
            'database': 'test',
            'maxConnections': 3,
            'minFreeConnections': 1,
            'user': 'root',
            'password': '',
        })
        self.assertTrue(conf.remote.union.mysql.read_db.charset == 'utf8mb4')
        self.assertTrue(conf.remote.union.mysql.read_db.host == '127.0.0.1')
        self.assertTrue(conf.remote.union.mysql.read_db.port == 3306)
        self.assertTrue(conf.remote.union.mysql.read_db.database == 'test')
        self.assertTrue(conf.remote.union.mysql.read_db.maxConnections == 3)
        self.assertTrue(conf.remote.union.mysql.read_db.minFreeConnections == 1)
        self.assertTrue(conf.remote.union.mysql.read_db.user == 'root')
        self.assertTrue(conf.remote.union.mysql.read_db.password == '')
        self.assertTrue(conf.remote.union.mysql.write_db == {
            'charset': 'utf8mb4',
            'host': '127.0.0.1',
            'port': 3306,
            'database': 'test',
            'maxConnections': 3,
            'minFreeConnections': 1,
            'user': 'root',
            'password': '',
        })
        self.assertTrue(conf.remote.union.mysql.write_db.charset == 'utf8mb4')
        self.assertTrue(conf.remote.union.mysql.write_db.host == '127.0.0.1')
        self.assertTrue(conf.remote.union.mysql.write_db.port == 3306)
        self.assertTrue(conf.remote.union.mysql.write_db.database == 'test')
        self.assertTrue(conf.remote.union.mysql.write_db.maxConnections == 3)
        self.assertTrue(conf.remote.union.mysql.write_db.minFreeConnections == 1)
        self.assertTrue(conf.remote.union.mysql.write_db.user == 'root')
        self.assertTrue(conf.remote.union.mysql.write_db.password == '')
