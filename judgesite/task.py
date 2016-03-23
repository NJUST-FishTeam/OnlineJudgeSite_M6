#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import io
import json
import shutil
import subprocess
import os

from config import conf


class NoTestDataException(Exception):
    pass


class JudgeTask(object):

    def __init__(self, message, save_result_callback):
        task = json.loads(message)
        print message
        self.id = task['id']
        self.code = task["code"]
        self.language = task["language"]
        self.testdata_id = str(task["testdata_id"])
        self.time_limit = str(task["time_limit"])
        self.memory_limit = str(task["memory_limit"])
        self.validator = str(task["validator"])

        self.result = ""
        self.run_time = 0
        self.run_memory = 0
        self.others = ""

        self.save_result_callback = save_result_callback

    def go(self):
        self._clean_files()

        try:
            self._compile_spj_exec()

            self._prepare_temp_dir()

            self._dump_code_to_file()

            self._prepare_testdata_file()
        except NoTestDataException, e:
            self.result = 'NoTestDataError'
        except Exception, e:
            raise e
        else:
            self._run()

            self._read_result()

        self._save_result()

        self._clean_files()

    def _compile_spj_exec(self):
        if self.validator == 'Special Validator':
            spj_exec_path = os.path.join(
                conf.testdata_path, self.testdata_id, "SpecialJudge")
            if not os.path.exists(spj_exec_path):
                spj_code_file = os.path.join(
                    conf.testdata_path, self.testdata_id, "specialjudge.cpp")
                commands = ["g++", spj_code_file, "-lm",
                            "-static", "-O2", "-w", '-o', spj_exec_path]
                subprocess.call(commands)

    def _prepare_temp_dir(self):
        logging.info("Prepare temp dir")
        os.mkdir(conf.tmp_path)

    def _dump_code_to_file(self):
        logging.info("Dump code to file")
        filename = "Main." + self.language
        self.code_file = os.path.join(conf.tmp_path, filename)
        code_file = io.open(self.code_file, 'w', encoding='utf8')
        code_file.write(self.code)
        code_file.close()

    def _prepare_testdata_file(self):
        logging.info("Prepare testdata")
        input_file = os.path.join(
            conf.testdata_path, self.testdata_id, "in.in")
        output_file = os.path.join(
            conf.testdata_path, self.testdata_id, "out.out")
        if not os.path.exists(input_file) or not os.path.exists(output_file):
            raise NoTestDataException
        shutil.copy(input_file, conf.tmp_path)
        shutil.copy(output_file, conf.tmp_path)
        if self.validator == 'Special Validator':
            spj_exec_path = os.path.join(
                conf.testdata_path, self.testdata_id, "SpecialJudge")
            shutil.copy(spj_exec_path, conf.tmp_path)

    def _run(self):
        logging.info("GO!GO!GO!")
        commands = ["sudo", "./Core", "-c", self.code_file, "-t",
                    self.time_limit, "-m", self.memory_limit, "-d",
                    conf.tmp_path]
        if self.validator == 'Special Validator':
            commands += ["-s", "-S", "2"]  # 2 = cpp
        subprocess.call(commands)

    def _read_result(self):
        logging.info("Read result")
        result_file = open(os.path.join(conf.tmp_path, "result.txt"), 'r')
        self.result = result_file.readline().strip()
        self.run_time = result_file.readline().strip()
        self.run_memory = result_file.readline().strip()
        self.others = result_file.read()

    def _save_result(self):
        logging.info("Save result")
        self.save_result_callback(
            id=self.id,
            run_time=self.run_time,
            run_memory=self.run_memory,
            compiler_output=self.others,
            status=self.result)

    def _clean_files(self):
        logging.info("Clean files")
        if os.path.exists(conf.tmp_path):
            shutil.rmtree(conf.tmp_path)
