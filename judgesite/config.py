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
    'judge_exchange',
    'judege_result_queue'
])
rabbitmq_setting = requests.get(
    'http://etcc.in.njoj.org:8009/services/rabbitmq-01/configures/production/').json()['data']
judge_site_setting = requests.get(
    'http://etcc.in.njoj.org:8009/services/judge-site/configures/default/').json()['data']

conf = Configure(
    testdata_path="",
    tmp_path="",
    rmq_host=rabbitmq_setting['HOST'],
    rmq_port=rabbitmq_setting['PORT'],
    rmq_user=rabbitmq_setting['USER'],
    rmq_password=rabbitmq_setting['PASSWORD'],
    judge_task_queue=judge_site_setting['judge_task_queue'],
    judge_exchange=judge_site_setting['judge_exchange'],
    judege_result_queue=judge_site_setting['judege_result_queue'],
)
