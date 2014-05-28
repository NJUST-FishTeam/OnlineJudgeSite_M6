#!/usr/bin/env python
# encoding: utf-8


import os
import logging
import logging.config



importpath = ['connector', 'protocol', 'tools']

dir_ = os.getcwd()

lastSource = os.path.join(dir_, "lastSource")
core_dir = os.path.join(dir_, "Core")
run_dir = os.path.join(dir_, "run_dir")
data_dir = os.path.join(dir_, "data_dir")


host = "192.168.0.121"
port = 27182
datahost = "192.168.0.121"
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
