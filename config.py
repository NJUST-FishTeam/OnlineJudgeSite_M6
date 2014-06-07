#!/usr/bin/env python
# encoding: utf-8


import os
import logging
import logging.config

import fcntl
import socket
import struct
import thread

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])


dir_ = os.getcwd()
lastSource = os.path.join(dir_, "lastSource")
core_dir = os.path.join(dir_, "Core")
run_dir = os.path.join(dir_, "run_dir")
data_dir = os.path.join(dir_, "data_dir")


host = "192.168.7.2"
# host = get_ip_address("wlan0")
port = 27182
datahost = "192.168.7.2"
# datahost = get_ip_address("wlan0")
dataport = 31415


logging.config.fileConfig("logging.conf")
logger = logging.getLogger("example1")


availableCompiler = ['gcc', 'g++', 'java']
availableValidator = ['Text Validator', 'Special Validator']


#language
LANG_UNKOWN = 0
LANG_C = 1
LANG_CPP = 2
LANG_JAVA = 3
