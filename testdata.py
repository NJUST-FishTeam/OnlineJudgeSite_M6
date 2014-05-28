#!/usr/bin/env python
# encoding: utf-8


import os
import socket

import config

class DataClient(object):

    def __init__(self):
        self.data_path = config.data_dir
        self.host = config.datahost
        self.port = config.dataport


    def _mkdir(self, path):
        if not os.path.isdir(path):
            os.makedirs(path)


    def _touch(self, filename):
        with open(filename, 'a'):
            os.utime(filename, None)


    def checkout_md5(self, md5_value, _type, testDataId):
        path = self.data_path + '/' + testDataId
        self._mkdir(path)

        if _type == 'IN':
            filename = self.data_path + '/' + testDataId + '/' + 'in.check'
        elif _type == 'OUT':
            filename = self.data_path + '/' + testDataId + '/' + 'out.check'

        self._touch(filename)
        fp = open(filename, 'r')
        _md5 = fp.readline()
        fp.close()
        fp = open(filename, 'w')
        fp.write(md5_value)
        fp.close()
        # print '_md5=', _md5, ']'
        # print 'md5_value=', md5_value, ']'
        if _md5 == md5_value:
            return True
        else:
            return False


    def update_data(self, testDataId, filename):
        con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            con.connect((self.host, self.port))
        except socket.error, msg:
            config.logger.error("DataClient connect to dataserver  failed. Error code: %s, Message: %s" % (msg[0], msg[1]))
        else:
            config.logger.info("DataClient connect to dataserver successed.")

        con.send(str(testDataId + "/" + filename))

        path = self.data_path + '/' + testDataId + '/'
        filename = path + filename
        if not os.path.isdir(path):
            os.makedirs(path)
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


