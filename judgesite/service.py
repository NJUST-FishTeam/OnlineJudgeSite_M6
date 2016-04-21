#!/usr/bin/env python
# -*- coding: utf-8 -*-


import logging
import pika
import json

from config import conf
from task import JudgeTask


class JudgeSite(object):

    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=conf.rmq_host, port=conf.rmq_port))
        self.channel = self.connection.channel()

        # judge_task_queue
        self.channel.queue_declare(queue=conf.judge_task_queue, durable=True)
        self.channel.queue_bind(queue=conf.judge_task_queue,
                                exchange=conf.judge_exchange,
                                routing_key=conf.judge_task_queue)
        # judge_result_queue
        self.channel.queue_declare(queue=conf.judge_result_queue, durable=True)
        self.channel.queue_bind(queue=conf.judge_result_queue,
                                exchange=conf.judge_exchange,
                                routing_key=conf.judge_result_queue)

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

    def save_result(self, id, run_time=0, run_memory=0, compiler_output="", status="SystemError"):
        def ensure_unicode(s, encoding='utf-8'):
            return s.decode(encoding) if isinstance(s, str) else s
        compiler_output = ensure_unicode(compiler_output)
        status = ensure_unicode(status)
        body = {
            u'id': id,
            u'data': {
                u'run_time': run_time,
                u'run_memory': run_memory,
                u'compiler_output': compiler_output,
                u'status': status
            }

        }
        self.channel.basic_publish(
            exchange=conf.judge_exchange,
            routing_key=conf.judge_result_queue,
            body=json.dumps(body, ensure_ascii=False),  # We shouldn't mix unicode with str
            properties=pika.BasicProperties(
                delivery_mode=2,  # make message persistent
            ))
