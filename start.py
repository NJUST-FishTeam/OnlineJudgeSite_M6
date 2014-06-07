#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import

import os

import config
from judge import judge
from m6connector import M6Connector

isRunning = False


def _init():
    if not os.path.isdir(config.data_dir):
        os.mkdir(config.data_dir)
    if not os.path.isdir(config.run_dir):
        os.mkdir(config.run_dir)
    with open(config.lastSource, 'a'):
        os.utime(config.lastSource, None)


def _work():
    m6connector = M6Connector()
    m6connector.on_load()
    config.logger.info("等待判题请求")
    submission = m6connector.get_submission()
    config.logger.info("已得到可用的判题请求")

    if submission['validator'] == 'Text Validator':
        is_spj = False
        spj_lang = 0
    else:
        is_spj = True
        spj_lang = submission['spj_type']

    lang = submission['compiler']
    if lang == 'GCC':
        lang = config.LANG_C
    elif lang == 'GPP':
        lang = config.LANG_CPP
    elif lang == 'Java':
        lang = config.LANG_JAVA

    config.logger.info("开始判题")
    result = judge(config.lastSource, lang, submission['testDataId'],
            submission['timeLimit'], submission['memoryLimit'], is_spj, spj_lang)

    result['submissionId'] = submission['submissionId']

    m6connector.send_result(result)
    config.logger.info("判题完成")


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


