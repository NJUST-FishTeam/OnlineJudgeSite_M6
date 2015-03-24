#!/usr/bin/env python
# -*- coding: utf-8 -*-


import logging
import pika

from config import conf
from task import JudgeTask


class JudgeSite(object):

    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=conf.rmq_host, port=conf.rmq_port))
        self.channel = self.connection.channel()

        self.channel.basic_consume(self._consume, queue=conf.rmq_queue, no_ack=True)

    def _consume(self, ch, method, properties, body):
        #print " [x] Received %r" % (body,)
        logging.info("GOT A TASK!")
        task = JudgeTask(body)
        task.go()
        logging.info("TASK IS DONE!")

    def run(self):
        self.channel.start_consuming()