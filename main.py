#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from judgesite.service import JudgeSite


def main():
    logging.basicConfig(format='%(levelname)s:%(asctime)s %(filename)s %(funcName)s %(lineno)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
    logging.info("Judge Node starting...")
    srv = JudgeSite()
    srv.run()


if __name__ == "__main__":
    main()