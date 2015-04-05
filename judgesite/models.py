#!/usr/bin/env python
# -*- coding: utf-8 -*-


import requests
from sqlalchemy import create_engine
from sqlalchemy.sql import text

from config import conf

engine = create_engine("mysql://{0}:{1}@{2}/{3}?charset=utf8".format(conf.mysql_user,
                                                        conf.mysql_password,
                                                        conf.mysql_host,
                                                        conf.mysql_db_name),
                       pool_recycle=600)


def save_result(status_id=0, type='normal', run_time=0, run_memory=0, compiler_output="", status="SystemError"):
    conn = engine.connect()
    if type == 'normal':
        sql = text(
            '''
            update fishteam_submit_status set `compilerOutput` = :compiler_output, `runtime` = :run_time, `runmemory` = :run_memory, `status` = :status where `id` = :status_id;
            '''
        )
    else:
        sql = text(
            '''
            update fishteam_contest_status set `compilerOutput` = :compiler_output, `runtime` = :run_time, `runmemory` = :run_memory, `status` = :status where `id` = :status_id;
            '''
        )

    conn.execute(sql, compiler_output=compiler_output, run_time=run_time, run_memory=run_memory, status=status, status_id=status_id)
    update_counters(status_id, type)
    conn.close()


def update_counters(status_id, type):
    argument = {
        'status_id': status_id,
        'type': type,
        'access_key': conf.access_key,
    }
    requests.post(conf.api_url+"/Api/v1/updatecounter/", argument)