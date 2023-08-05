#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: setup.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-04-16 22:19:36 (CST)
# Last Update:星期一 2018-01-08 11:23:26 (CST)
#          By: jianglin
# Description:
# **************************************************************************
from setuptools import setup

setup(
    name='Flask-Maple',
    version='0.5.2',
    url='https://github.com/honmaple/flask-maple',
    license='BSD',
    author='honmaple',
    author_email='xiyang0807@gmail.com',
    description='captcha ,bootstrap,easy login and more flask tips.',
    long_description='easy to use captcha ,bootstrap and login and more flask tips.Please visit https://github.com/honmaple/flask-maple',
    packages=['flask_maple'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask',
        'Flask-Assets',
        'Flask-Login',
        'Flask-Babelex',
    ],
    classifiers=[
        'Environment :: Web Environment', 'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent', 'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ])
