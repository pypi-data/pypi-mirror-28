#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time		: 16/01/2018 9:11 AM
# @Author	: chang.feng
# @File		: setup.py

from setuptools import setup


setup(
    name='micli',
    version=0.2,
    author='vincent',
    author_email='hienha@163.com',
    url='https://github.com/hienha/emcli',
    description='A simple email client in terminal.',
    packages=['micli'],
    install_requires=['yagmail'],
    tests_require=['nose', 'tox'],
    entry_points={
        'console_scripts': [
            'micli=micli:main'
        ]
    }
)
