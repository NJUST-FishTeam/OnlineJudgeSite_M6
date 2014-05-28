#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: zsl

from hashlib import md5

import config


#make and return the md5 of the file(filename)
def md5_file(filename):
    m = md5()
    try:
        a_file = open(filename,'rb')  #需要使用二进制格式读取文件内容
    except IOError:
        config.logger.error("Can not open %s" % filename)
        # print 'Can not open %s' % filename
    m.update(a_file.read())
    try:
        a_file.close()
    except IOError:
        config.logger.error("Can not close %s" % filename)
        # print 'Can not close %s' % filename
    return m.hexdigest()


#make and return the md5 of (string)
def md5_string(string):
    m = md5() #获取一个MD5加密算法对象
    m.update(string) #指定要加密的字符串
    return m.hexdigest() #获取加密后的16进制字符串


#read the md5 of (filename)
def get_md5(filename):
    try:
        fp = open(filename,'r')
    except IOError:
        config.logger.error("Can not open %s" % filename)
        # print 'Can not open %s ' % filename
    try:
        file_md5 = fp.readline().strip()
    except IOError:
        config.logger.error("Can not read from %s" % filename)
        # print 'Can not read from %s' % filename
    else:
        return file_md5


