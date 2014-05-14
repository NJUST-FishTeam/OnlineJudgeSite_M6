#!/usr/bin/env python
# encoding: utf-8

import logging
import logging.config



importpath = ['connector', 'protocol', 'tools']

lastSource = "/home/zozoz/judge/lastSource"
tempPath = "/home/zozoz/judge/temp"
validatorPath = "/home/zozoz/judge/validators"
dataPath = "/home/zozoz/judge/siteData"
errorPath = "/home/zozoz/judge/errorLog"
outPath = "/home/zozoz/judge/output"


host = "192.168.1.108"
port = 27182
datahost = "192.168.1.108"
dataport = 31415


logging.config.fileConfig("logging.conf")
logger = logging.getLogger("example1")


availableCompiler = ['gcc', 'g++', 'java']
availableValidator = ['Text Validator', 'Special Validator']
