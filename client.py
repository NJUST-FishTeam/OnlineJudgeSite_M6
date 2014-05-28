#!/usr/bin/env python
# encoding: utf-8


import re
import socket

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
        request = MyEncoder().encode(request)
        request = self.match(request, _type)
        try:
            self.con.sendall(request)
        except Exception:
            config.logger.critical("Send request message failed.")
            self.con.close()
            self.hasConnected = False
            config.logger.info("连接已经关闭.")
        response = self.con.recv(65535)
        # print "Type of response : ", type(response)
        # print "Response :", response
        # _content, _type = self.rmatch(response)
        # response = MyDecoder().decode(_content)
        response, _type = self.rmatch(response)
        # print 'Response1 : ', response
        response = eval(response)
        # print 'Type1 : ', type(response)
        return response


