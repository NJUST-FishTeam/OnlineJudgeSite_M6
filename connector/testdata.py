#!/usr/bin/env python
# encoding: utf-8

import sys
sys.path.append("..")

import socket

import start.config as config

class DataClient(object):

    def __init__(self):
        self.data_path = config.dataPath
        self.host = config.datahost
        self.port = config.dataport

    def update_data(self):
        con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            con.connect((self.host, self.port))
        except socket.error, msg:
            config.logger.critical("DataClient connect to dataserver  failed. Error code: %s, Message: %s" % (msg[0], msg[1]))
        else:
            config.logger.info("DataClient connect to dataserver successed.")


