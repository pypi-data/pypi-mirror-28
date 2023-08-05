#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time		: 16/01/2018 10:15 AM
# @Author	: chang.feng
# @File		: logger.py

import logging


def get_logger(log_level = logging.INFO):
    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)

    formatter = logging.Formatter("%(asctime)s [micli] [%(levelname)s] : %(message)s", "%Y-%m-%d %H:%M:%S")

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger.handlers = [handler]

    return logger