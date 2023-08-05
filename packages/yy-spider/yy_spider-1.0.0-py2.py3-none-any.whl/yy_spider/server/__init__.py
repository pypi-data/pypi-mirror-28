# coding:utf8
"""
@author: xsren 
@contact: bestrenxs@gmail.com
@site: xsren.me

@version: 1.0
@file: __init__.py
@time: 26/12/2017 11:14 AM

"""
from __future__ import absolute_import

import atexit

from twisted.internet import reactor
from yy_spider.settings import Settings
from yy_spider.utils.yy_logger import get_logger

from .server import ServerFactory


class ServerRunner(object):
    """"""

    def __init__(self, config):
        if config:
            conf = Settings(config)
        else:
            conf = Settings()
        self._logger = get_logger()
        self._conf = conf

    def run(self):
        """"""
        port = self._conf.SOCKET_PORT
        factory = ServerFactory(self._conf, self._logger)
        reactor.listenTCP(port, factory)
        reactor.run()
        # 退出时做清理工作
        atexit.register(factory.cleanup)


def run():
    pass


if __name__ == '__main__':
    run()
