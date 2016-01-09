#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import namedtuple

import requests

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
mysql_setting = requests.get(
    'http://etcc.in.njoj.org:8009/services/mysql-01/configures/production/').json()['data']
rabbitmq_setting = requests.get(
    'http://etcc.in.njoj.org:8009/services/rabbitmq-01/configures/production/').json()['data']
judge_site_setting = requests.get(
    'http://etcc.in.njoj.org:8009/services/judge-site/configures/default/').json()['data']

conf = Configure(
    testdata_path="",
    tmp_path="",
    mysql_user=mysql_setting['USER'],
    mysql_password=mysql_setting['PASSWORD'],
    mysql_host=mysql_setting['HOST'],
    mysql_db_name="fishteam_onlinejudge",
    rmq_host=rabbitmq_setting['HOST'],
    rmq_port=rabbitmq_setting['PORT'],
    rmq_user=rabbitmq_setting['USER'],
    rmq_password=rabbitmq_setting['PASSWORD'],
    rmq_queue=judge_site_setting['rmq_queue'],
    access_key=judge_site_setting['access_key'],
    api_url=judge_site_setting['api_url'],
)
