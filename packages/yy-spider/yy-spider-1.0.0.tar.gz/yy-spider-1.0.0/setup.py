# coding:utf8
"""
@author: xsren 
@contact: bestrenxs@gmail.com
@site: xsren.me

@version: 1.0
@file: setup.py.py
@time: 16/01/2018 10:28 AM

"""
import ssl

from setuptools import setup, find_packages

ssl._create_default_https_context = ssl._create_unverified_context

requires = []
with open("requirements.txt", 'r') as fh:
    for line in fh.readlines():
        requires.append(line.strip())

setup(
    name='yy-spider',
    version='1.0.0',
    description='一个增量式爬虫系统',
    long_description=open('README.md').read(),
    url='https://github.com/yy-spider/yy_spider',
    author='xsren',
    author_email='bestrenxs@gmail.com',
    license='BSD',
    include_package_data=True,
    # packages=['yy_spider'],
    packages=find_packages(exclude=('tests', 'tests.*')),
    entry_points={
        'console_scripts': ['yy_spider = yy_spider.run_spider:execute_spider',
                            'yy_server = yy_spider.run_server:execute_server']
    },
    classifiers=[
        'Framework :: Scrapy',
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='spider increment distribute',
    install_requires=requires,
)
