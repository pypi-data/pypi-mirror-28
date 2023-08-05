# coding:utf8
"""
@author: xsren 
@contact: bestrenxs@gmail.com
@site: xsren.me

@version: 1.0
@file: increment_spider.py
@time: 25/12/2017 4:25 PM

"""
import time
import traceback

import requests
from yy_spider.common.yy_exceptions import InvalidTaskException, Http404Exception
from yy_spider.message_bus import common


class BaseSpider(object):
    """"""

    def __init__(self, conf, logger, task_queue, result_queue):
        self._conf = conf
        self._logger = logger
        self._task_queue = task_queue
        self._result_queue = result_queue
        self._change_session_limit = conf.CHANGE_SESSION_LIMIT
        self._last_crawl_count = 0
        self._session = None
        self.init_session()

    def run(self):
        """运行爬虫"""
        self.init_seed()
        while True:
            try:
                task = self._task_queue.get()
                self._logger.debug("begin to do task {}".format(task['_id']))
                self.crawl(task)
                if self._conf.TASK_COLL:
                    self._result_queue.put((common.CHANGE_TASK_STATUS, self._conf.TASK_COLL,
                                            [{'_id': task['_id'], 'status': common.CRAWL_SUCCESS}]))
                self._logger.debug("finish to do task {}".format(task['_id']))
            except InvalidTaskException as e:
                if self._conf.TASK_COLL:
                    self._result_queue.put((common.CHANGE_TASK_STATUS, self._conf.TASK_COLL,
                                            [{'_id': task['_id'], 'status': common.INVALID}]))
                self._logger.debug("finish to do task {}".format(task['_id']))
            except Exception as e:
                trace = traceback.format_exc()
                self._logger.error("error:{},trace:{}".format(str(e), trace))
                if self._conf.TASK_COLL:
                    self._result_queue.put((common.CHANGE_TASK_STATUS, self._conf.TASK_COLL,
                                            [{'_id': task['_id'], 'status': common.CRAWL_FAIL}]))
                self._logger.debug("finish to do task {}".format(task['_id']))

    def init_seed(self):
        """初始化种子"""

    def _update_headers(self, headers):
        self._conf.DEFAULT_HEADERS.update(headers)
        return self._conf.DEFAULT_HEADERS

    def crawl_url(self, url, method='get', headers={}, data={}, timeout=None):
        """抓取url, 尝试MAX_RETRY_TIME次"""
        try_times = 0
        self._logger.debug("begin to crawl url :{}".format(url))
        t0 = time.time()
        if not timeout:
            timeout = self._conf.DEFAULT_HTTP_TIMEOUT
        headers = self._update_headers(headers)
        while try_times < self._conf.MAX_RETRY_TIME:
            try_times += 1
            if self._last_crawl_count >= self._change_session_limit:  # 同一个session抓取一定的数量就应该reset
                self.init_session()
            try:
                res = getattr(self._session, method)(url, headers=headers, params=data, timeout=timeout)
                if res.status_code != 200:  # http status
                    if res.status_code == 404:
                        raise Http404Exception
                    raise Exception("status_code != 200")
                time.sleep(self._conf.DOWNLOAD_SLEEP_TIME)
                break
            except Exception as e:
                err_info = 'download html failed, url: {}, error:{}'.format(url, str(e))
                self._logger.error(err_info)
                if str(e) in self._conf.INVALID_TASK_ERRORS:
                    raise InvalidTaskException
                self._set_id_info_status(is_ok=0, err_info=err_info)
                self.init_session()

        if not res:
            raise Exception("res is None")

        if res.status_code != 200:  # http status
            raise Exception("status_code != 200")

        t_diff = time.time() - t0
        self._logger.debug("finish to crawl url :%s, use time:%s" % (url, t_diff))
        return res

    def init_session(self):
        self._logger.warning('begin to reset session')
        self._last_crawl_count = 0
        self._session = requests.Session()
        self._set_id_info()
        self._logger.warning('reset session success')

    def _set_cookie(self, cookies):
        """设置cookie，cookie是'k=v;k=v'格式的字符串"""
        if not cookies:
            return
        for s in cookies.split(';'):
            k = s.split('=')[0]
            v = s.split('=')[1]
            self.session.cookies.set(k, v)

    def _set_proxy(self, proxy):
        """设置代理信息"""
        if not proxy:
            return
        if proxy['schema'] == 'socks5':
            schema = "{}h".format(proxy['schema'])
        else:
            schema = proxy['schema']
        username = proxy['username']
        password = proxy['password']
        ip = proxy['ip']
        port = proxy['port']
        if username and password:
            proxies = {'http': '{}://{}:{}@{}:{}'.format(schema, username, password, ip, port),
                       'https': '{}://{}:{}@{}:{}'.format(schema, username, password, ip, port),
                       }
        else:
            proxies = {'http': '{}://{}:{}'.format(schema, ip, port),
                       'https': '{}://{}:{}'.format(schema, ip, port),
                       }
        self.session.proxies = proxies

    def _set_id_info(self):
        """设置身份信息信息，可能包括cookie，账号，代理等"""
        if not self._conf.ID_INFO_SERVER:
            return
        while True:
            try:
                url = 'http://{}/id_info'.format(self._conf.ID_INFO_SERVER)
                res = requests.get(url, headers={'TOKEN': self._conf.ID_INFO_TOKEN})
                d = res.json()['data']
                self._id = d['_id']
                self._set_cookie(d['cookies'])
                self._username = d['username']
                self._password = d['password']
                self._id_extra = d['extra']
                self._set_proxy(d['proxy'])
            except Exception as e:
                self._logger.warning("_set_id_info:{}".format(str(e)))
                time.sleep(10)

    def _set_id_info_status(self, is_ok, err_info):
        """设置身份信息信息，例如账号标记状态为不健康"""
        if not self._conf.ID_INFO_SERVER:
            return
        while True:
            try:
                url = 'http://{}/id_info/{}'.format(self._conf.ID_INFO_SERVER, self._id)
                data = {'is_ok': is_ok, 'err_info': err_info}
                res = requests.put(url, headers={'TOKEN': self._conf.ID_INFO_TOKEN}, data=data)
                if res.status_code != 200:
                    raise Exception('res.status_code!=200')
            except Exception as e:
                self._logger.warning("_set_id_info:{}".format(str(e)))
                time.sleep(10)
