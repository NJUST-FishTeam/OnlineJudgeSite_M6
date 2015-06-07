#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import namedtuple

Configure = namedtuple("Configure", [
    'testdata_path',
    'tmp_path',
    'mysql_user',
    'mysql_password',
    'mysql_host',
    'mysql_db_name',
    'rmq_host',
    'rmq_port',
    'rmq_queue',
    'rmq_user',
    'rmq_password',
    'access_key',
    'api_url'
])


conf = Configure(
    testdata_path="",
    tmp_path="",
    mysql_user="",
    mysql_password="",
    mysql_host="",
    mysql_db_name="",
    rmq_host="",
    rmq_port=5672,
    rmq_queue="task",
    rmq_user="guest",
    rmq_password="guest",
    access_key="",
    api_url="",
)
