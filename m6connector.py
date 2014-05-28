#!/usr/bin/env python
# encoding: utf-8

import subprocess
import time

from client import Client
from proxy import Proxy
from testdata import DataClient
import config

class M6Connector(object):

    _instance = None
    is_online = False

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(M6Connector, cls).__new__(
                    cls, *args, **kwargs
                    )
        return cls._instance


    def online(self):
        config.logger.info("尝试上线。。。。")
        try:
            proxy = Proxy()
            response = proxy.online()
            self.is_online = True
            config.logger.info("上线成功，节点ID：%s" % response['siteId'])
        except Exception, msg:
            config.logger.error("上线失败，错误信息：%s" % msg)


    def on_load(self):
        client = Client()
        while True:
            wait = 1
            success = client.connect()
            if success:
                break
            config.logger.warning("连接失败，%s s后重新连接." % wait)
            time.sleep(wait)
        if not self.is_online:
            self.online()
            config.logger.info("M6Connector 已经上线成功.")


    def _write_source_code(self, response):
        with open(config.lastSource, 'w') as fp:
            fp.write("//requestTime: %s\n" % response['dateTime'])
            fp.write("//submissionId: %s\n" % response['submissionId'])
            fp.write("//compiler: %s\n" % response['compiler'])
            fp.write("//validator: %s\n" % response['validator'])
            fp.write(response['sourceCode'])


    def get_submission(self):
        response = None
        is_valid = False
        while not is_valid:
            try:
                proxy = Proxy()
                response = proxy.get_submission()
            except Exception, e:
                config.logger.error(e)
                self.is_online = False
                self.on_load()
            if response['valid'] == 'true':
                is_valid = True
            time.sleep(2)

        self._write_source_code(response)
        self.prepare(response)

        return response


    def prepare(self, response):
        dataclient = DataClient()

        testDataId = response['testDataId']
        inputMd5 = response['inputMd5']
        outputMd5 = response['outputMd5']
        spjMd5 = response['spjMd5']

        if not dataclient.checkout_md5(inputMd5, 'IN', testDataId):
            dataclient.update_data(testDataId, 'in.in')

        if not dataclient.checkout_md5(outputMd5, 'OUT', testDataId):
            dataclient.update_data(testDataId, 'out.out')

        if not response['validator'] == 'Text Validator':
            if not dataclient.checkout_md5(spjMd5, 'SPJ', testDataId):
                dataclient.update_data(testDataId, 'SpecialJudge.' + response['spj_type'])
                try:
                    self._compile(config.data_dir + '/' + testDataId + '/', 'SpecialJudge.' + response['spj_type'], response['spj_type'])
                    config.logger.info('SpecialJudge %s compile successed.' % response['testDataId'])
                except:
                    config.logger.error('SpecialJudge compile failed.')


    def send_result(self, response):
        proxy = Proxy()
        proxy.update_result(
                response['submissionId'], response['status'],
                response['run_time'], response['run_memory'], response['extra_message'],
                '', '', '', time.strftime('%Y-%m-%d %X', time.localtime(time.time()))
                )


    def update_state(self):
        pass


    def _compile(self, path, name, _type):
        parameter = []
        if _type == 'java':
            parameter.append("javac")
            parameter.append(path + name)
            parameter.append("-o")
            parameter.append(path + "SpecialJudge")
        elif _type == 'cpp':
            parameter.append("g++")
            parameter.append(path + name)
            parameter.append("-O2")
            parameter.append("-o")
            parameter.append(path + "SpecialJudge")
        elif _type == 'c':
            parameter.append("gcc")
            parameter.append(path + name)
            parameter.append("-O2")
            parameter.append("-o")
            parameter.append(path + "SpecialJudge")

        subprocess.call(parameter)

