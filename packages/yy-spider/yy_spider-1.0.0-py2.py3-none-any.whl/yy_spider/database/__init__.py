# coding:utf8
"""
@author: xsren 
@contact: bestrenxs@gmail.com
@site: xsren.me

@version: 1.0
@file: __init__.py.py
@time: 30/12/2017 10:00 PM

"""
from pymongo import MongoClient


def get_mongo_db(user, password, host, port, db):
    """"""
    mc = MongoClient(host, port)
    if user or password:
        mc[db].authenticate(user, password)
    return mc[db]

