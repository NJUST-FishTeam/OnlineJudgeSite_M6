#!/usr/bin/env python
# encoding: utf-8

import sys
sys.path.append("..")

import os
import socket

import start.config as config

class DataClient(object):

    def __init__(self):
        self.data_path = config.dataPath
        self.host = config.datahost
        self.port = config.dataport


    def _mkdir(self, path):
        if not os.path.isdir(path):
            os.makedirs(path)

    def _touch(self, filename):
        with open(filename, 'a'):
            os.utime(filename, None)


    def checkout_md5(self, md5_value, _type, testDataId):
        path = config.dataPath + '/' + testDataId
        self._mkdir(path)

        if _type == 'IN':
            filename = config.dataPath + '/' + testDataId + '/' + 'in.check'
        elif _type == 'OUT':
            filename = config.dataPath + '/' + testDataId + '/' + 'out.check'

        self._touch(filename)
        fp = open(filename, 'w+')
        _md5 = fp.readline()
        fp.write(md5_value)
        fp.close()
        if _md5 == md5_value:
            return True
        else:
            return False


    def update_data(self, testDataId, filename):
        con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            con.connect((self.host, self.port))
        except socket.error, msg:
            config.logger.critical("DataClient connect to dataserver  failed. Error code: %s, Message: %s" % (msg[0], msg[1]))
        else:
            config.logger.info("DataClient connect to dataserver successed.")

        con.send(str(testDataId + "/" + filename))

        path = config.dataPath + '/' + testDataId + '/'
        filename = path + filename
        if not os.path.isdir(path):
            os.mkdir(path)
        with open(filename, 'a'):
            os.utime(filename, None)
        os.remove(filename)

        try:
            fp = open(filename, 'a')
        except IOError, e:
            config.logger.error(filename + ' : ' + e)
        while True:
            data = con.recv(65535)
            if not data:
                break
            fp.write(data)
        fp.close()
        con.close()


