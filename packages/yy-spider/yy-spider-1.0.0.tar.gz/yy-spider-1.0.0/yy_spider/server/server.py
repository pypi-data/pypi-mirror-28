# coding:utf8
"""
@author: xsren 
@contact: bestrenxs@gmail.com
@site: xsren.me

@version: 1.0
@file: server.py
@time: 30/12/2017 9:56 PM

"""

import struct
import threading
import time

import msgpack
from yy_spider import utils
from yy_spider.database import get_mongo_db
from yy_spider.database.db_handler import DbHandler
from yy_spider.message_bus import common
from queue import Queue
from twisted.internet.protocol import Factory
from twisted.internet.protocol import Protocol


class ServerProtocal(Protocol):
    def __init__(self, users, logger, db, conf):
        self.users = users
        self.logger = logger
        self._conf = conf
        self.db = db
        self.name = None
        self.state = "FIRST"
        self.buffer = b''
        self.data_length = 0

    def connectionMade(self):
        info = "connection from", self.transport.getPeer()
        self.logger.debug(info)

    def connectionLost(self, reason):
        info = "Lost connection from", self.transport.getPeer(), reason.getErrorMessage()
        self.logger.warning(info)
        if self.name in self.users:
            del self.users[self.name]

    def dataReceived(self, data):
        if self.state == "FIRST":
            self.handle_first(data)
        else:
            self.handle_data(data)

    # 验证密码
    def handle_first(self, data):
        data = data.decode('utf8')
        tmp = data.split('@@@***')
        if len(tmp) < 2:
            self.transport.abortConnection()
        else:
            name = tmp[0]
            pwd = tmp[1]
            if utils.md5(name + self._conf.SOCKET_KEY) == pwd:
                self.name = name
                self.users[name] = self
                self.state = "DATA"
                self.transport.write(b"OK!!")
            else:
                self.transport.abortConnection()

    def handle_data(self, data):
        self.buffer += data
        while True:
            if self.data_length <= 0:
                if len(self.buffer) >= 4:
                    self.data_length = struct.unpack('>I', self.buffer[:4])[0]
                    if self.data_length > 1024 * 1024:
                        utils.send_email("data length:%s" % self.data_length)
                        self.transport.abortConnection()
                    self.buffer = self.buffer[4:]
                else:
                    return
            if len(self.buffer) >= self.data_length:
                tmp_data = self.buffer[:self.data_length]
                self.buffer = self.buffer[self.data_length:]
                self.data_length = 0
                self.process_data(tmp_data)
                return
            else:
                return

    def process_data(self, data):
        rj = msgpack.unpackb(data, encoding='utf-8')
        if rj['type'] == common.REQUEST_MESSAGE:
            coll_name = rj["coll_name"]
            action = rj["action"]
            data = rj["data"]
            self.handle_request(coll_name, action, data)
        elif rj['type'] == common.ECHO_MESSAGE:
            pass
        else:
            info = "not support message:%s" % rj['type']
            self.logger.warning(info)
            self.transport.abortConnection()

    def send_msg(self, msg):
        msg = struct.pack('>I', len(msg)) + msg
        self.my_send(msg)

    def my_send(self, msg):
        total_sent = 0
        msg_len = len(msg)
        while total_sent < msg_len:
            if len(msg) > 4:
                self.transport.write(msg[:4])
                msg = msg[4:]
            else:
                self.transport.write(msg)
            total_sent = total_sent + 4

    def handle_request(self, coll_name, action, data):
        db = self.db
        if action == common.PUT_TASK:
            d = db.put_task_to_db(coll_name, data)
            d.addCallback(self.handle_success)
            d.addErrback(self.handle_failure)
        elif action == common.GET_TASK:
            d = db.get_task_from_db(coll_name, data['count'], data.get('cond', {}))
            d.addCallback(self.handle_success)
            d.addErrback(self.handle_failure)
        elif action == common.PUT_DATA:
            db.put_data_to_db(coll_name, data)
            self.handle_success([])
        elif action == common.CHANGE_TASK_STATUS:
            db.change_task_status(coll_name, data)
            self.handle_success([])

    def handle_success(self, res):
        res = {
            'type': common.RESPONSE_MESSAGE,
            'status': common.OK,
            'data': res,
        }
        _res = msgpack.packb(res)
        self.send_msg(_res)

    def handle_failure(self, err):
        res = {
            'type': common.RESPONSE_MESSAGE,
            'status': common.FAIL,
            'data': [],
        }
        _res = msgpack.packb(res)
        self.send_msg(_res)
        self.logger.error(err)


class ServerFactory(Factory):
    def __init__(self, conf, logger):
        self.users = {}
        write_queues = {}
        task_queues = {}
        count_queue = Queue(maxsize=conf.COUNT_QUEUE_SIZE)

        mdb = get_mongo_db(conf.MONGO_USER, conf.MONGO_PASSWORD, conf.MONGO_HOST, conf.MONGO_PORT, conf.MONGO_DB)
        self._logger = logger
        self._conf = conf
        self.db = DbHandler(logger, mdb, conf, write_queues, task_queues, count_queue)

        ts = []
        # 开一个线程定时清理
        t1 = threading.Thread(target=self.sched_cleanup, args=())
        ts.append(t1)
        for t in ts:
            t.setDaemon(True)
            t.start()
        logger.info("__init__ finish")

    def buildProtocol(self, addr):
        return ServerProtocal(self.users, self._logger, self.db, self._conf)

    def sched_cleanup(self):
        """定时清理"""
        while True:
            time.sleep(self._conf.CLEANUP_INTERVAL)
            self.cleanup()

    def cleanup(self):
        self.db.cleanup_handle_queue()
