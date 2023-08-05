# coding:utf8
"""
@author: xsren 
@contact: bestrenxs@gmail.com
@site: xsren.me

@version: 1.0
@file: dianping_spider.py
@time: 07/01/2018 8:49 PM

"""
import time

from lxml.html import fromstring

from yy_spider.client.spiders.base_spider import BaseSpider
from yy_spider.message_bus import common


class Spider(BaseSpider):
    """"""

    def __init__(self, conf, logger, task_queue, result_queue):
        BaseSpider.__init__(self, conf, logger, task_queue, result_queue)

    def init_seed(self):
        """"""
        task = {'_id': 'http://jandan.net/duan'}
        self._task_queue.put(task)

    def crawl(self, task):
        """"""
        url = task['_id']
        headers = {'Host': 'jandan.net'}
        res = self.crawl_url(url, headers=headers)
        doc = fromstring(res.text)
        ns = doc.xpath('//ol[@class="commentlist"]/li')
        ds = []
        index = 0
        for _n in ns:
            author = _n.xpath('./div//div[@class="author"]/strong')[0].text
            text = _n.xpath('./div//div[@class="text"]/p')[0].text
            d = {'_id': "{}?index={}".format(url, index),
                 'author': author,
                 'text': text}
            ds.append(d)
            index += 1
            # print("{} : {}".format(author, text))

        self._result_queue.put((common.PUT_DATA, "jiandan", ds))

        next_page_nodes = doc.xpath('//div[@class="cp-pagenavi"]/a[@title="Older Comments"]')
        if len(next_page_nodes) > 0:
            new_task = {'_id': 'http:{}'.format(next_page_nodes[0].xpath('./@href')[0])}
            self._task_queue.put(new_task)
            time.sleep(3)
