#!/usr/bin/env python
# -*- coding: utf-8 -*-

from util import ObjectDict


conf = ObjectDict()
conf.testdata_path = ""
conf.tmp_path = ""
conf.mysql_user = ""
conf.mysql_password = ""
conf.mysql_host = "localhost"
conf.mysql_db_name = ""
conf.rmq_host = "localhost"
conf.rmq_port = 5672
conf.rmq_queue = "submit_task"
conf.rmq_user = "guest"
conf.rmq_password = "guest"
