#!/usr/bin/env python
# -*- coding: utf-8 -*-


from sqlalchemy import create_engine
from sqlalchemy.sql import text

from config import conf

engine = create_engine("mysql://{0}:{1}@{2}/{3}".format(conf.mysql_user,
                                                        conf.mysql_password,
                                                        conf.mysql_host,
                                                        conf.mysql_db_name),
                       encoding='utf-8')


def save_result(status_id=0, type='normal', run_time=0, run_memory=0, compiler_output="", status="SystemError"):
    if type == 'normal':
        table = 'fishteam_submit_status'
    else:
        table = 'fishteam_contest_status'

    sql = text(
        '''
        update :table set compilerOutput = :compiler_output, runtime = :runtime, runmemory = :run_memory, status = :status where id = :status_id;
        '''
    )
    engine.execute(sql, table=table, compiler_output=compiler_output, run_time=run_time, run_memory=run_memory, status=status, status_id=status_id)
