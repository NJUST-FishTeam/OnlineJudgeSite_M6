#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import

import os
import sys

import config
import engine

def __init():
    for each in config.importpath:
        sys.path.append(os.path.join(os.getcwd(), each))

isRunning = False

def work():
    global isRunning
    isRunning = True
    while isRunning:
        engine.work()

if __name__ == "__main__":
    while True:
        try:
            work()
        except (), e:
            config.logger.error(e)
        finally:
            isRunning = False


