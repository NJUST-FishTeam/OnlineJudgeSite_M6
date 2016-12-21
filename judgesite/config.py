#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import namedtuple

import requests

Configure = namedtuple("Configure", [
    'testdata_path',
    'tmp_path',
    'rmq_host',
    'rmq_port',
    'rmq_user',
    'rmq_password',
    'judge_task_queue',
    'database_host',
    'database_port',
    'database_user',
    'database_passwd',
    'database_name',
    'redis_host',
    'redis_port',
    'judge_exchange'
])

conf = Configure(
    testdata_path="/home/shuwei/project/fishteam/catProject/judgenode/testdata/",
    tmp_path="/home/shuwei/project/fishteam/catProject/judgenode/tmp/",
    rmq_host="localhost",
    rmq_port=5672,
    rmq_user="guest",
    rmq_password="guest",
    judge_task_queue="judge_task",
    judge_exchange="judge_exchange",
    database_host="localhost",
    database_port=3306,
    database_user="root",
    database_passwd="root",
    database_name="fishteam_cat",
    redis_host="localhost",
    redis_port=6379
)
