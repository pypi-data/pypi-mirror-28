# coding:utf8
"""
@author: xsren 
@contact: bestrenxs@gmail.com
@site: xsren.me

@version: 1.0
@file: __init__.py
@time: 26/12/2017 11:14 AM

"""
import importlib

import gevent
from gevent.queue import Queue
from yy_spider.settings import Settings
from yy_spider.utils.yy_logger import get_logger


class SpiderRunner(object):
    """"""

    def __init__(self, config, gevent_number=None):

        if config:
            conf = Settings(config)
        else:
            conf = Settings()

        if gevent_number:
            conf.THREAD_NUM = gevent_number
            conf.TASK_QUEUE_LIMIT = gevent_number * 5
            conf.RESULT_QUEUE_LIMIT = gevent_number * 100

        self._conf = conf
        self._logger = get_logger(self.__module__)

    def run(self):
        """运行爬虫程序
        1、初始化task queue和result queue
        2、初始化message_bus，用于通信
        3、启动指定数量的协程用于抓取和解析
        """
        task_queue = Queue(self._conf.TASK_QUEUE_LIMIT)
        result_queue = Queue(self._conf.RESULT_QUEUE_LIMIT)
        gevent_threads = []
        message_bus_moudle = importlib.import_module(self._conf.MESSAGE_BUS)
        # 跟服务器建立两个连接，一个专门收任务，一个专门发送结果
        if self._conf.TASK_COLL:
            recv_message_bus = message_bus_moudle.MessageBus(self._conf, task_queue, result_queue, self._logger)
            gevent_threads.append(gevent.spawn(recv_message_bus.get_tasks))
        send_message_bus = message_bus_moudle.MessageBus(self._conf, task_queue, result_queue, self._logger)
        gevent_threads.append(gevent.spawn(send_message_bus.save_result))
        for x in range(self._conf.THREAD_NUM):
            spider_module = importlib.import_module(self._conf.SPIDER_CLASS)
            spider = spider_module.Spider(self._conf, self._logger, task_queue, result_queue)
            gevent_threads.append(gevent.spawn(spider.run))
        gevent.joinall(gevent_threads)
