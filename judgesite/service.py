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

    def update_submit_status(self, id, status, detail, score, compiler_output, cursor):
        logging.info("Start updating submit_status")
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

    def update_problem_solved_record(self, cur_score, is_solved, pro_solved_rec_id, cursor):
        logging.info("Start updating problem_solved_record")
        value = {'id': pro_solved_rec_id}
        sql = """SELECT `highest_score`, solved FROM `problem_solved_record` WHERE id = %(id)s"""
        cursor.execute(sql, value)
        fetch_result = cursor.fetchone()
        is_solved = max(is_solved, int(fetch_result[1]))
        highest_score = max(int(fetch_result[0]), cur_score)

        value = {
            'solved': is_solved,
            'id': pro_solved_rec_id,
            'last_score': cur_score,
            'highest_score': highest_score
        }
        sql = """UPDATE `problem_solved_record` SET last_score = %(last_score)s,
            highest_score = %(highest_score)s, solved = %(solved)s WHERE id = %(id)s"""
        cursor.execute(sql, value)

    def update_database(self, status, detail, status_id, cur_score, is_solved,
        compiler_output, pro_solved_rec_id, is_compile_error):
        logging.info('Start updating database')
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
            self.update_submit_status(status_id, status, detail, cur_score, compiler_output, cursor)
            if not is_compile_error:
                self.update_problem_solved_record(cur_score, is_solved, pro_solved_rec_id, cursor)
            conn.commit()
        except Exception, e:
            logging.error("Update database error!")
            logging.error(e)
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

    def save_result(self, status_id, detail, case_score,
            compiler_output, is_compile_error, pro_solved_rec_id):
        cur_score = 0
        if is_compile_error:
            detail = ''
            status = 'Compile Error'
        else:
            status = 'Accepted'
            for index, sta in enumerate(detail['result']):
                if sta['status'] == 'Accepted':
                    cur_score += case_score[index]
                else:
                    status = 'Wrong Answer'
            compiler_output = ''
            if status == 'Wrong Answer' and cur_score > 0:
                status = 'Partially Correct'
        detail = str(detail).replace('\'', '"')
        is_solved = 1 if status == 'Accepted' else 0

        self.update_database(
            status=status,
            detail=detail,
            status_id=status_id,
            cur_score=cur_score,
            is_solved=is_solved,
            compiler_output=compiler_output,
            is_compile_error=is_compile_error,
            pro_solved_rec_id=pro_solved_rec_id
        )
