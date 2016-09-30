#!/usr/bin/env python
# -*- coding: utf-8 -*-


import logging
import pika
import json

import redis
import MySQLdb as mdb
from config import conf
from task import JudgeTask


class JudgeSite(object):

    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=conf.rmq_host, port=conf.rmq_port))
        self.channel = self.connection.channel()

        # judge_task_queue
        self.channel.queue_declare(queue=conf.judge_task_queue, durable=True)
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(self._consume, queue=conf.judge_task_queue)

    def _consume(self, ch, method, properties, body):
        logging.info("GOT A TASK!")
        task = JudgeTask(body, self.save_result)
        task.go()
        self.channel.basic_ack(delivery_tag=method.delivery_tag)
        logging.info("TASK IS DONE!")

    def run(self):
        self.channel.start_consuming()

    def update_database(self, id, status, detail, score, compiler_output):
        logging.info("Start updating database")
        config = {
            'host': conf.database_host,
            'port': conf.database_port,
            'user': conf.database_user,
            'passwd': conf.database_passwd,
            'db': conf.database_name,
            'charset': 'utf8'
        }
        conn = mdb.connect(**config)
        cursor = conn.cursor()
        try:
            value = {
                'compiler_output': compiler_output,
                'status': status,
                'score': score,
                'detail': detail,
                'id': id
            }
            sql = """UPDATE `submit_status` SET compilerOutput = %(compiler_output)s,
                status = %(status)s, score = %(score)s, detail = %(detail)s WHERE id = %(id)s"""
            cursor.execute(sql, value)
            conn.commit()
        except Exception, e:
            logging.error("Update database error!")
            logging.error(e)
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

    def update_redis(self, contest_id, user_id, problem_id, score, highest_score):
        _redis = redis.Redis(connection_pool=redis.ConnectionPool(
            host=conf.redis_host,
            port=conf.redis_port,
            db=0)
        )
        logging.info("Start updating redis!")
        hashtable_name = "contestscore:{0}:{1}".format(str(contest_id), str(user_id))
        if highest_score:
            old_score = _redis.hget(hashtable_name, problem_id)
            if old_score is None or old_score < score:
                _redis.hset(hashtable_name, problem_id, score)
        else:
            _redis.hset(hashtable_name, problem_id, score)

    def save_result(self, id, status, user_id, case_count, case_score,
        contest_id, problem_id, highest_score, compiler_output=None):
        result = 'Accepted'
        cur_score = 0
        if compiler_output is None:
            for index, sta in enumerate(status['result']):
                if sta['status'] == 'Accepted':
                    cur_score += case_score[index]
                else:
                    result = 'Wrong Answer'
            compiler_output = ''
        else:
            result = 'Compile Error'
        status = str(status).replace('\'', '"')
        self.update_database(id, result, status, cur_score, compiler_output)
        if compiler_output is None:
            self.update_redis(contest_id, user_id, problem_id, cur_score, highest_score)
