#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import unicode_literals

import logging
import json
import shutil
import os

import ljudge

from config import conf


class NoTestDataException(Exception):
    pass


class NoSpecialJudgeException(Exception):
    pass


class JudgeTask(object):

    def __init__(self, message, save_result_callback):
        task = json.loads(message)
        self.id = task['id']
        self.code = task["code"]
        self.language = task["language"]
        self.testdata_id = str(task["testdata_id"])
        self.time_limit = str(task["time_limit"])
        self.memory_limit = str(task["memory_limit"])
        self.validator = str(task["validator"])

        self.result = {}

        self.save_result_callback = save_result_callback

        logging.info("Task id is: %s" % self.id)

    def run(self):
        self._clean_files()
        try:
            self._prepare_temp_dir()

            self._dump_code_to_file()

            self._prepare_testdata_file()
        except NoTestDataException as e:
            self.result = 'NoTestDataError'
        except NoSpecialJudgeException as e:
            self.result = 'NoSpecialJudgeException'
        except Exception as e:
            self.result = 'System Error'
            logging.exception(e)
        else:
            self._run()

        self._save_result()

        self._clean_files()

    def _prepare_temp_dir(self):
        logging.info("Prepare temp dir")
        os.mkdir(conf.tmp_path)

    def _dump_code_to_file(self):
        logging.info("Dump code to file")
        filename = "Main." + self.language
        self.code_file = os.path.join(conf.tmp_path, filename)
        with open(self.code_file, 'w') as code_file:
            code_file.write(self.code.encode('utf-8'))

    def _prepare_testdata_file(self):
        logging.info("Prepare testdata")
        self.input_file = os.path.join(
            conf.testdata_path, self.testdata_id, "in.in")
        self.output_file = os.path.join(
            conf.testdata_path, self.testdata_id, "out.out")
        if not os.path.exists(self.input_file) or\
                not os.path.exists(self.output_file):
            raise NoTestDataException
        if self.validator == 'Special Validator':
            self.spj_code_file = os.path.join(
                conf.testdata_path, self.testdata_id, "specialjudge.cpp")
            if not os.path.exists(self.spj_code_file):
                # 不存在spj程序, 2016/10/22 由于老版SPJ题不存在spj.cpp, 导致judge site崩溃
                raise NoSpecialJudgeException()

    @staticmethod
    def _parse_ljudge_result(ljudge_res):
        result = {
            'status': '',
            'time': 0,
            'memory': 0,
            'compiler_output': '',
        }
        if not ljudge_res['compilation']['success']:
            result['status'] = 'Compile Error'
            result['compiler_output'] = ljudge_res['compilation']['log']
            return result
        if not ljudge_res.get('checkerCompilation', dict(success=True)).\
                get('success'):
            result['status'] = 'Spj Compile Error'
            return result
        testcase = ljudge_res['testcases'][0]   # oj 单case
        status_map = {
            'ACCEPTED': 'Accepted',
            'PRESENTATION_ERROR': 'Presentation Error',
            'WRONG_ANSWER': 'Wrong Answer',
            'NON_ZERO_EXIT_CODE': 'Non Zero Exit Code',
            'MEMORY_LIMIT_EXCEEDED': 'Memory Limit Exceeded',
            'TIME_LIMIT_EXCEEDED': 'Time Limit Exceeded',
            'OUTPUT_LIMIT_EXCEEDED': 'Output Limit Exceeded',
            'FLOAT_POINT_EXCEPTION': 'Float Point Error',
            'SEGMENTATION_FAULT': 'Segmentation Fault',
            'RUNTIME_ERROR': 'Runtime Error',
            'INTERNAL_ERROR': 'System Error',
        }
        result['status'] = status_map.get(testcase['result'], 'System Error')
        result['time'] = int(testcase.get('time', 0)*1000)      # s to ms
        result['memory'] = int(testcase.get('memory', 0)/1024)  # B to KB
        return result

    def _run(self):
        logging.info("GO!GO!GO!")
        opts = {
            'max-cpu-time': int(self.time_limit) / 1000,
            'max-real-time': 20.0,                              # 最多运行20s
            'max-memory': '{0}K'.format(self.memory_limit),
            'user-code': self.code_file,
            'max-compiler-real-time': 10,
            'max-compiler-memory': '256M',
            'testcase': {
                'input': self.input_file,
                'output': self.output_file,
            }
        }
        if self.validator == 'Special Validator':
            opts['checker-code'] = self.spj_code_file
        self.result = self._parse_ljudge_result(ljudge.run(opts))

    def _save_result(self):
        logging.info("Save result, result is %s" % self.result['status'])
        self.save_result_callback(
            id=self.id,
            run_time=self.result['time'],
            run_memory=self.result['memory'],
            compiler_output=self.result['compiler_output'],
            status=self.result['status'])

    def _clean_files(self):
        logging.info("Clean files")
        if os.path.exists(conf.tmp_path):
            shutil.rmtree(conf.tmp_path)
