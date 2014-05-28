#!/usr/bin/env python
# encoding: utf-8


import time

from client import Client
from submission import Submission
from proxy import Proxy
from testdata import DataClient
import config

class M6Connector(object):
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(M6Connector, cls).__new__(
                    cls, *args, **kwargs
                    )
        return cls._instance

    is_online = False

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

        submissionId = response['submissionId']
        timeLimit = response['timeLimit']
        memoryLimit = response['memoryLimit']
        compiler = response['compiler']
        validator = response['validator']
        saveOutput = response['keepOutput']

        submission = Submission(submissionId, compiler, validator, timeLimit, memoryLimit, saveOutput)
        return submission


    def prepare(self, response):
        dataclient = DataClient()

        testDataId = response['testDataId']
        inputMd5 = response['inputMd5']
        outputMd5 = response['outputMd5']

        if not dataclient.checkout_md5(inputMd5, 'IN', testDataId):
            dataclient.update_data(testDataId, 'in.in')

        if not dataclient.checkout_md5(outputMd5, 'OUT', testDataId):
            dataclient.update_data(testDataId, 'out.out')


    def send_result(self):
        pass

    def update_state(self):
        pass


