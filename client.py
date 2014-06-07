#!/usr/bin/env python
# encoding: utf-8


import re
import socket
import time

import config
from en_de_coder import MyEncoder


class Client(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Client, cls).__new__(
                    cls, *args, **kwargs
                    )
        return cls._instance

    hasConnected = False
    con = ''

    def connect(self):
        while not self.hasConnected:
            self.con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            host = config.host
            port = config.port
            try:
                self.con.settimeout(60)
                self.con.connect((host, port))
            except socket.error, msg:
                config.logger.error("client connect failed. Error code: %s, Message: %s" % (msg[0], msg[1]))
                return False
            else:
                self.hasConnected = True
                config.logger.info("连接已建立，ip： %s, port: %s" % (host, port))
                return True
        return True

    def rmatch(self, content):
        pattern = '(?P<Content><Response type=\"(?P<Type>.*?)\">(?P<Response>.*?)</Response>)'
        match = re.search(pattern, content)
        if match:
            _content = match.group("Response")
            _type = match.group("Type")
            return _content, _type
        else:
            return None

    def match(self, content, _type):
        temp = '<Request type=\"%s\">%s</Request>' % (_type, content)
        return temp

    def send_request(self, request, _type):
	# config.logger.debug(request)
        request = MyEncoder().encode(request)
        request = self.match(request, _type)
	# config.logger.debug(request)
        try:
            self.con.sendall(request)
        except Exception:
            config.logger.critical("Send request message failed.")
            self.con.close()
            self.hasConnected = False
            config.logger.info("连接已经关闭.")
        response = ''
        while True:
            data  = self.con.recv(1024)
            response += data
            # print 'length=', len(data)
            if data.endswith('南京理工大学开放式在线评测系统'):
                break
            #if len(data) < 1024:
            #    break
            #time.sleep(1)
        # print "Type of response : ", type(response)
        # print "Response :", response
        # _content, _type = self.rmatch(response)
        # response = MyDecoder().decode(_content)
        response, _type = self.rmatch(response)
        # print 'Response1 : ', response
        response = eval(response)
        # print 'Type1 : ', type(response)
	# config.logger.debug(response)
        return response


