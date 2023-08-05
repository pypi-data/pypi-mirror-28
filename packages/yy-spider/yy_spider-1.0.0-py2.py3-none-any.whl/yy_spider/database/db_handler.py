# coding:utf8
"""
@author: xsren 
@contact: bestrenxs@gmail.com
@site: xsren.me

@version: 1.0
@file: db_handler.py
@time: 30/12/2017 10:20 PM

"""

import time
import traceback

# 本地库
from yy_spider.message_bus import common
from pymongo import UpdateOne, ReplaceOne, InsertOne, UpdateMany
from pymongo.errors import BulkWriteError
from queue import Queue
from twisted.internet import defer


class DbHandler(object):
    def __init__(self, logger, mdb, conf, write_queues, task_queues, count_queue):
        self.logger = logger
        self.mdb = mdb
        self._conf = conf
        self.write_queues = write_queues
        self.task_queues = task_queues
        self.count_queue = count_queue

    def init_write_queue(self, coll_name):
        if not self.write_queues.get(coll_name, None):
            self.write_queues[coll_name] = Queue(maxsize=self._conf.WRITE_QUEUE_SIZE)

    def cleanup_handle_queue(self):
        self.logger.debug("clear ... cleanup begin")
        try:
            self._handle_write_queue()
            self._handle_count_queue()
        except BulkWriteError as bwe:
            self.logger.error(bwe.details)
            werrors = bwe.details['writeErrors']
            self.logger.error(werrors)
        except Exception as e:
            self.logger.error(str(e))
            traceback.print_exc()

        self.logger.debug("clear ... cleanup end")

    def _handle_write_queue(self):
        for coll_name, _queue in self.write_queues.items():
            t0 = time.time()
            requests = []
            qsize = _queue.qsize()
            while _queue.qsize() > 0:
                try:
                    req = _queue.get_nowait()
                    _queue.task_done()
                except Exception as e:
                    self.logger.error(str(e))
                    break
                requests.append(req)
            if len(requests) > 0:
                self.mdb[coll_name].bulk_write(requests, ordered=False)
            t_diff = time.time() - t0
            info = "handle_write_queue,coll:{},size:{},t_diff:{}".format(coll_name, qsize, t_diff)
            self.logger.info(info)

    def _handle_count_queue(self):
        if self.count_queue.qsize() > 0:
            t0 = time.time()
            requests = []
            qsize = self.count_queue.qsize()
            while self.count_queue.qsize() > 0:
                try:
                    tmp = self.count_queue.get_nowait()
                    self.count_queue.task_done()
                except Exception as e:
                    self.logger.error(str(e))
                    break
                requests.append(tmp)
            if len(requests) > 0:
                self.mdb[self._conf.STATS_COLL].bulk_write(requests, ordered=False)

            t_diff = time.time() - t0
            info = "handle_count_queue,size:{},t_diff:{}".format(qsize, t_diff)
            self.logger.info(info)

    @defer.inlineCallbacks
    def put_task_to_db(self, coll_name, data):
        """新加任务"""
        t0 = time.time()
        self.init_write_queue(coll_name)

        # 获取已经存在的task有哪些？
        res = yield self.mdb[coll_name].find({"_id": {"$in": list(set([t['_id'] for t in data]))}}, {'_id': 1})
        exists = [r['_id'] for r in res]
        self.save_stats_data(coll_name, common.NEW_TASK, len(data) - len(exists))
        # 更新数据
        for t in data:
            if t[b"_id"] not in exists:
                self.write_queues[coll_name].put(InsertOne(t))

        t_diff = time.time() - t0
        info = "{}, {}".format(coll_name, t_diff)
        self.logger.debug(info)
        defer.returnValue([])

    @defer.inlineCallbacks
    def get_task_from_db(self, coll_name, count, cond={}):
        """获取任务"""
        t0 = time.time()
        cond['status'] = common.NOT_CRAWL
        requests, ts = [], []
        tasks = yield self.mdb[coll_name].find(cond, limit=count)
        for task in tasks:
            requests.append(
                UpdateMany({'_id': task[b"_id"]}, {"$set": {"status": common.CRAWLING, "last_crawl_time": 0}})
            )
            task.pop('_id')
            ts.append(task)
        if len(requests) > 0:
            yield self.mdb[coll_name].bulk_write(requests, ordered=False)
        t_diff = time.time() - t0
        info = "total, {}, return : {}, use time : {}".format(coll_name, len(ts), t_diff)
        self.logger.debug(info)
        return ts

    def change_task_status(self, coll_name, data):
        """更新任务状态"""
        t0 = time.time()
        self.init_write_queue(coll_name)
        # 统计，记录成功的任务数
        success = [t['_id'] for t in data if t['status'] == common.CRAWL_SUCCESS]
        self.save_stats_data(coll_name, common.ONE_TASK, len(success))
        # 更新数据
        for t in data:
            self.write_queues[coll_name].put(
                UpdateMany({'_id': t['_id']}, {"$set": {'status': t['status']}})
            )
        t_diff = time.time() - t0
        info = "{}, {}".format(coll_name, t_diff)
        self.logger.debug(info)

    def put_data_to_db(self, coll_name, data):
        """新增数据，如果已经存在则替换旧的数据"""
        t0 = time.time()
        self.init_write_queue(coll_name)
        # 统计，记录抓取的数据条数
        self.save_stats_data(coll_name, common.ONE_DATA, len(data))
        for t in data:
            self.write_queues[coll_name].put(ReplaceOne({'_id': t['_id']}, t, upsert=True))
        t_diff = time.time() - t0
        info = "{}, {}".format(coll_name, t_diff)
        self.logger.debug(info)

    def save_stats_data(self, coll_name, _type, count):
        """存储统计数据"""
        date = time.strftime("%Y-%m-%d", time.localtime())
        # 单个collection
        u1 = UpdateOne({'date': date, 'coll_name': coll_name, "_type": _type},
                       {'$inc': {'total': count}}, upsert=True)
        # 总体
        u2 = UpdateOne({'date': date, 'coll_name': "all", "_type": _type}, {'$inc': {'total': count}},
                       upsert=True)
        self.count_queue.put(u1)
        self.count_queue.put(u2)
