#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import

import os
import time

import config
from m6connector import M6Connector


isRunning = False


def _init():
    # for each in config.importpath:
    #     sys.path.append(os.path.join(os.getcwd(), each))
    if not os.path.isdir(config.data_dir):
        os.mkdir(config.data_dir)
    if not os.path.isdir(config.run_dir):
        os.mkdir(config.run_dir)
    with open(config.lastSource, 'a'):
        os.utime(config.lastSource, None)






def _judge_over():
    pass


def _work():
    m6connector = M6Connector()
    m6connector.on_load()
    submission = m6connector.get_submission()
    config.logger.info("已得到可用的判题请求")

    time.sleep(100)


def _engine():
    global isRunning
    isRunning = True
    while isRunning:
        _work()


if __name__ == "__main__":
    _init()
    while True:
        try:
            _engine()
        except Exception, e:
            config.logger.error(e)
        finally:
            isRunning = False


