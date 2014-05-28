#!/usr/bin/env python
# encoding: utf-8


import time
import uuid

from client import Client
from request import *
import config
class Proxy(object):

    _instance = None
    _key = ''
    _secret = ''
    _siteId = ''

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Proxy, cls).__new__(
                    cls, *args, **kwargs
                    )
            cls._key = 'key'
            cls._secret = 'secret'
            cls._siteId = str(uuid.uuid4())
        return cls._instance

    def get_submission(self):
        dateTime = time.strftime('%Y-%m-%d %X', time.localtime(time.time()))
        request = GetSubmissionRequest(self._siteId, dateTime, config.availableCompiler, config.availableValidator)
        client = Client()
        response = client.send_request(request, 'Get Submission')
        return response

    def heart_beat(self):
        pass

    def online(self):
        dateTime = time.strftime('%Y-%m-%d %X', time.localtime(time.time()))
        request = OnlineRequest(self._siteId, self._secret, self._key, dateTime)
        client = Client()
        response = client.send_request(request, 'Online')
        return response

    def offline(self):
        dateTime = time.strftime('%Y-%m-%d %X', time.localtime(time.time()))
        request = OfflineRequest(self._siteId, self._key, self._secret, dateTime)
        client = Client()
        response = client.send_request(request, 'Offline')
        return response

    def update_result(self, submissionId, judgeResult, runTime, runMemory,
            compilerOutput, coreOutput, validatorOutput, programOutput, dateTime):
        request = UpdateResultRequest(self._siteId, submissionId, judgeResult, runTime, runMemory,
            compilerOutput, coreOutput, validatorOutput, programOutput, dateTime)
        client = Client()
        response = client.send_request(request, 'Update Result')
        return response

    def update_state(self, submissionId, newState, dateTime):
        request = UpdateResultRequest(self._siteId, submissionId, newState, dateTime)
        client = Client()
        response = client.send_result(request, 'Update State')
        return response


