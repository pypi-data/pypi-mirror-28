# coding:utf8
"""
@author: xsren 
@contact: bestrenxs@gmail.com
@site: xsren.me

@version: 1.0
@file: socket_bus.py
@time: 25/12/2017 4:48 PM

"""
import socket
import struct
import time

import msgpack
# 本地库
from yy_spider import utils

from . import common
from .base_bus import BaseBus


class MessageBus(BaseBus):
    def __init__(self, conf, task_queue, result_queue, logger):
        self.host = conf.SOCKET_HOST
        self.port = conf.SOCKET_PORT
        self.key = conf.SOCKET_KEY
        self.user_name = conf.SOCKET_USERNAME
        self._logger = logger
        self._task_queue = task_queue
        self._result_queue = result_queue
        self._conf = conf
        self.connect()

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.connect((self.host, self.port))
            self.sock.settimeout(60 * 10)
        except Exception as e:
            self._logger.error(str(e))
            self.reconnect(sleep_time=60)
            return

        self.auth()

    # server端需要认证
    def auth(self):
        password = utils.md5(self.user_name + self.key)
        try:
            token = "%s@@@***%s" % (self.user_name, password)
            self.sock.sendall(token.encode('utf8'))
            res = self.recvall(4)
            if res != b'OK!!':
                self._logger.error("invalid password!!!")
                self.reconnect(sleep_time=30)
                return
        except Exception as e:
            self._logger.error(str(e))
            self.reconnect(sleep_time=30)
            return

    def __del__(self):
        del self.sock

    def reconnect(self, sleep_time=15):
        self.__del__()
        time.sleep(sleep_time)
        self.connect()

    def send_msg(self, msg):
        msg1 = struct.pack('>I', len(msg)) + msg
        try:
            self.mysend(msg1)
            if len(msg) - 4 - 4 > 0:
                self._logger.info("send:%s" % (len(msg) - 4))
            return True
        except Exception as e:
            self._logger.error(str(e))
            self.reconnect(sleep_time=60)
            return False

    def mysend(self, msg):
        totalsent = 0
        MSGLEN = len(msg)
        while totalsent < MSGLEN:
            if len(msg) > self._conf.SOCKET_ONE_TIME_SEND:
                sent = self.sock.send(msg)
                msg = msg[sent:]
            else:
                sent = self.sock.send(msg)
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent

    def recv_msg(self):
        # Read message length and unpack it into an integer
        try:
            raw_msglen = self.recvall(4)
        except socket.timeout:
            self._logger.error('recv msg timeout ......')
            return None
        except Exception as e:
            self._logger.error(str(e))
            self.reconnect(sleep_time=60)
            return None

        if not raw_msglen:
            self._logger.warning("not raw_msglen")
            self.reconnect(sleep_time=60)
            return None
        msglen = struct.unpack('>I', raw_msglen)[0]
        # Read the message data

        try:
            return self.recvall(msglen)
        except Exception as e:
            self._logger.error(str(e))
            self.reconnect(sleep_time=60)
            return None

    def recvall(self, n):
        # Helper function to recv n bytes or return None if EOF is hit
        data = b''
        while len(data) < n:
            if n - len(data) > 4:
                packet = self.sock.recv(4)
            else:
                packet = self.sock.recv(n - len(data))
            if not packet:
                return None
            data += packet
        return data

    def get_tasks(self):
        """获取任务，放入任务队列"""
        while True:
            if self._task_queue.qsize() < self._conf.TASK_QUEUE_LIMIT:
                tasks = self.get_task(self._conf.TASK_COLL, self._conf.THREAD_NUM)
                self._logger.debug('get {} tasks'.format(len(tasks)))
                [self._task_queue.put([t]) for t in tasks]
                if len(tasks) == 0:
                    time.sleep(10)
            else:
                time.sleep(1)

    def save_result(self):
        """读取_result_queue中的数据，发给server"""
        while True:
            self._logger.debug("current result_queue qsize {}".format(self._result_queue.qsize()))
            if self._result_queue.qsize() > 0:
                res = self._result_queue.get()
                self.do_request(res[0], res[1], res[2])
            else:
                time.sleep(1)

    def do_request(self, action, coll_name, data):
        """"""
        req = {'type': common.REQUEST_MESSAGE,
               'action': action,
               'coll_name': coll_name,
               'data': data}
        _req = msgpack.packb(req)
        self.send_msg(_req)
        while True:
            res = self.recv_msg()
            if res:
                return msgpack.unpackb(res)

    def get_task(self, coll_name, count=1):
        data = {'count': count}
        return self.do_request(common.GET_TASK, coll_name, data)[b'data']

    def insert_data(self, coll_name, data):
        return self.do_request(common.PUT_DATA, coll_name, data)

    def update_data(self, coll_name, data):
        return self.do_request(common.UPDATE_DATA, coll_name, data)

    def insert_data_if_not_exist(self, coll_name, data):
        return self.do_request(common.INSERT_DATA_IF_NOT_EXIST, coll_name, data)

    def change_task_status(self, coll_name, data):
        return self.do_request(common.CHANGE_TASK_STATUS, coll_name, data)

    def put_task(self, coll_name, data):
        return self.do_request(common.PUT_TASK, coll_name, data)
