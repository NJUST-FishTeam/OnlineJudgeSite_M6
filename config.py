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
