#!/usr/bin/env python
# encoding: utf-8

import sys
sys.path.append("..")

from connector.m6connector import M6Connector
import config
def _complie(submission):
    config.logger.info("开始编译")
    pass

def _judge(submission):
    config.logger.info("开始判题")
    pass

def _validate(submission):
    config.logger.info("开始验证")
    pass

def _judge_over():
    pass

def work():
    m6connector = M6Connector()
    m6connector.on_load()
    submission = m6connector.get_submission()
    config.logger.info("已得到可用的判题请求")
    _complie(submission)
    _judge(submission)
    _validate(submission)

