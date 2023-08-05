#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time		: 16/01/2018 10:26 AM
# @Author	: chang.feng
# @File		: storage.py


class Storage(dict):
    """
    Storage() -> storage object like dictionary expect
    `obj.foo` can be used in addition to `obj['foo']`
    """
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError as k:
            raise AttributeError(k)

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, item):
        try:
            del self[item]
        except KeyError as k:
            raise SystemExit(k)

    def __repr__(self):
        """ rewrite `__repr__` method """
        return '<Storage ' + dict.__repr__(self) + '>'
