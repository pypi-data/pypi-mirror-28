#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time		: 16/01/2018 9:17 AM
# @Author	: chang.feng
# @File		: micli.py


import os
import sys
try:
    import ConfigParser
except ImportError:
    import configparser as ConfigParser
import argparse

import yagmail


from storage import Storage
from logger import get_logger


logger = get_logger()


def get_argparse():
    parser = argparse.ArgumentParser(description='A mail client in CLI')
    parser.add_argument('-s', action='store', dest='subject', required=True, help='specify a subject(must be in quotes if it has spaces)')
    parser.add_argument('-a', action='store', nargs='*', dest='attaches', required=False, help='attach file(s) to the message')
    parser.add_argument('-f', action='store', dest='conf', required=False, help='specify an alternative .emcli.conf file')
    parser.add_argument('-r', action='store', nargs='*', dest='recipients', required=True, help='recipient who you are sending the mail to')
    parser.add_argument('-v', action='version', version='%(prog)s 0.3')

    return parser.parse_args()


def get_config_file(config_file):
    if config_file is None:
        config_file = os.path.expanduser('~/.imcli.conf')
    return config_file


def get_meta_from_config(config_file):
    config = ConfigParser.ConfigParser()

    with open(config_file) as f:
        config.readfp(f)

    meta = Storage()
    for key in ['smtp_server', 'smtp_port', 'username', 'password']:
        try:
            val = config.get('DEFAULT', key)
        except (ConfigParser.NoSectionError, ConfigParser.NoOptionError) as err:
            logger.error(err)
            raise SystemExit(err)
        else:
            meta[key] = val

    return meta


def get_mail_content():
    return sys.stdin.read()


def send_mail(meta):
    content = get_mail_content()
    body = [content]

    if meta.attaches:
        body.extend(meta.attaches)


    with yagmail.SMTP(user=meta.username, password=meta.password,
                      host=meta.smtp_server, port=int(meta.smtp_port)) as yag:
        logger.info('ready to send mail "{0}" to "{1}"'.format(meta.subject, meta.recipients))
        ret = yag.send(meta.recipients, meta.subject, body)


def main():
    parser = get_argparse()
    config_file = get_config_file(parser.conf)

    if not os.path.exists(config_file):
        logger.error('{0} is not exists'.format(config_file))
        raise SystemExit()
    else:
        meta = get_meta_from_config(config_file)

    meta.subject = parser.subject
    meta.recipients = parser.recipients
    meta.attaches = parser.attaches

    if meta.attaches:
        for attach in meta.attaches:
            if not os.path.exists(attach):
                logger.error('{0} is not exists'.format(attach))
                raise SystemExit()

    send_mail(meta)


if __name__ == '__main__':
    main()
