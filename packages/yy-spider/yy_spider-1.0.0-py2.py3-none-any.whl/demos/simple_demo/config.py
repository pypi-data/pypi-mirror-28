# coding:utf8
"""
@author: xsren 
@contact: bestrenxs@gmail.com
@site: xsren.me

@version: 1.0
@file: config.py
@time: 30/12/2017 1:01 PM

"""

# 采集客户端相关
# DOWNLOAD_SLEEP_TIME = 0.1
# proxy相关
DELETE_PROXY_URL = ''
GET_PROXY_URL = ''


# 存储任务的collection
TASK_COLL = ''

SPIDER_CLASS = "demos.simple_demo.jiandan_spider"

# 消息总线相关
SOCKET_KEY = 'aded5%^&*^%#dasd$aaa'
SOCKET_USERNAME = 'spider'

"""server相关"""
# mongo
MONGO_USER = 'test'
MONGO_PASSWORD = 'test2017'
MONGO_HOST = '127.0.0.1'
MONGO_PORT = 27017
MONGO_DB = 'test'
STATS_COLL = 'test_stats'