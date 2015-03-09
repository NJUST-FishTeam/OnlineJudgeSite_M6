#!/usr/bin/env python
# -*- coding: utf-8 -*-


from judgesite.service import JudgeSite


def build_server(host='localhost', port=5672, queue='submit_task', user='guest', password='guest'):
    srv = JudgeSite(host=host, port=port, queue=queue, user=user, password=password)
    return srv


def main():
    srv = build_server()
    srv.run()


if __name__ == "__main__":
    main()