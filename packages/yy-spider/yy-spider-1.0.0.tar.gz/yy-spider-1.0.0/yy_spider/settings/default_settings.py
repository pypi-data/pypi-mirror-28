# coding:utf8
"""
@author: xsren 
@contact: bestrenxs@gmail.com
@site: xsren.me

@version: 1.0
@file: settings.py
@time: 25/12/2017 5:04 PM

"""

# 爬虫客户端相关
THREAD_NUM = 1
TASK_QUEUE_LIMIT = THREAD_NUM * 10
RESULT_QUEUE_LIMIT = 0
# 抓取相关
DEFAULT_HEADERS = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                   'Accept-Encoding': 'gzip, deflate',
                   'Accept-Language': 'zh,en-US;q=0.9,en;q=0.8,zh-CN;q=0.7,zh-TW;q=0.6',
                   'Cache-Control': 'max-age=0',
                   'Connection': 'keep-alive',
                   'Upgrade-Insecure-Requests': '1',
                   'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
MAX_RETRY_TIME = 5  # 最大重试次数
CHANGE_SESSION_LIMIT = 100
DEFAULT_HTTP_TIMEOUT = 30
DOWNLOAD_SLEEP_TIME = 0.1
INVALID_TASK_ERRORS = ["InvalidURL", "InvalidSchema", "MissingSchema",
                       "Http404Exception"]  # InvalidURL等错误可以直接认定为不合法的Task
# 身份信息服务器
ID_INFO_SERVER = ''
ID_INFO_TOKEN = ''

# 消息总线相关
MESSAGE_BUS = "yy_spider.message_bus.socket_bus"
SOCKET_HOST = '0.0.0.0'
SOCKET_PORT = 11201
SOCKET_KEY = 'aded5%^&*^%#dasd$'
SOCKET_USERNAME = 'spider'
SOCKET_ONE_TIME_SEND = 1024

"""server相关"""
# mongo
MONGO_USER = ''
MONGO_PASSWORD = ''
MONGO_HOST = '127.0.0.1'
MONGO_PORT = 27017
STATS_COLL = 'test_stats'
TASK_COLL = ''

# queue
COUNT_QUEUE_SIZE = 0
WRITE_QUEUE_SIZE = 0
TASK_QUEUE_SIZE = 0
CLEANUP_INTERVAL = 10
