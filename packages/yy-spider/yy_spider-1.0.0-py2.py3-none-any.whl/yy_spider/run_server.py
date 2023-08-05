# coding:utf8
"""
@author: xsren 
@contact: bestrenxs@gmail.com
@site: xsren.me

@version: 1.0
@file: run_server.py
@time: 16/01/2018 1:24 PM

"""
from gevent import monkey

monkey.patch_all()
import getopt
import os
import sys

# sys.path.append(os.getcwd())

from yy_spider.server import ServerRunner


def print_spider_help():
    help = """
    -h
    -c --config 
    """
    print(help)


def execute_server():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hc:", ["config="])
    except getopt.GetoptError:
        print_spider_help()
        sys.exit(2)

    config = 'config.py'

    for opt, arg in opts:
        if opt == '-h':
            print_spider_help()
            sys.exit()
        elif opt in ("-c", "--config"):
            config = arg

    config = config.replace('.py', '').replace('/', '.')
    sr = ServerRunner(config)
    sr.run()


if __name__ == '__main__':
    execute_server()
