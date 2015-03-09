#!/usr/bin/env python
# -*- coding: utf-8 -*-


import pika


class JudgeSite(object):

    def __init__(self, host='localhost', port=5672, queue='submit_task', user='guest', password='guest'):
        self.host = host
        self.port = port
        self.queue = queue
        self.user = user
        self.password = password

        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host, port=self.port))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue)

        self.channel.basic_consume(self._consume, queue=self.queue, no_ack=True)

    def _consume(self, ch, method, properties, body):
        print " [x] Received %r" % (body,)

    def run(self):
        self.channel.start_consuming()