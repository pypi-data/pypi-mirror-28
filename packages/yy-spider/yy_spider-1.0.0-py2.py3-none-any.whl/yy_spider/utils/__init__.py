# coding:utf8
"""
@author: xsren 
@contact: bestrenxs@gmail.com
@site: xsren.me

@version: 1.0
@file: __init__.py.py
@time: 30/12/2017 1:31 PM

"""

import hashlib


def md5(src):
    """md5加密"""
    m = hashlib.md5()
    if isinstance(src, str):
        src = src.encode("utf8")
    m.update(src)
    return m.hexdigest()
