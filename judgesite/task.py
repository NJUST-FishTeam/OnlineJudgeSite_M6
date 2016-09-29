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

class NoLanguageException(Exception):
    pass


class JudgeTask(object):

    def __init__(self, message, save_result_callback):
        task = json.loads(message)
        self.id = task['statusid']
        self.code = task["code"]
        self.language = task["lang"]
        self.testdata_id = str(task["testdataid"])
        self.time_limit = str(task["timelimit"])
        self.memory_limit = str(task["memorylimit"])
        self.case_count = int(task["casecount"])
        self.case_score = task["casescore"]
        self.contest_id = str(task["contestid"])
        self.problem_id = str(task["problemid"])
        self.user_id = task["userid"]
        self.highest_score = int(task["highest_score"])

        self.lang = 0
        self.compiler_output = None
        self.result = {"result":[]}

        self.save_result_callback = save_result_callback

        logging.info("Task id is: %s" % self.id)

    def go(self):
        self._clean_files()

        try:
            self._prepare_temp_dir()

            self._dump_code_to_file()

            self._compile_code_exec()

            if self.compiler_output is None:
                self._prepare_exec_file()
                self._judge()

            self._save_result()

            self._clean_files()

        except NoTestDataException, e:
            self.result = 'NoTestDataError'
        except NoLanguageException, e:
            self.result = 'NoLanguageError'

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

    def _compile_code_exec(self):
        if self.language == 'cpp':
            self.lang = '2'
            commands = ["g++", self.code_file, "-o", "Main", "-static", "-w",
                "-lm", "-std=c++11", "-O2", "-DONLINE_JUDGE"]
        elif self.language == 'c':
            self.lang = '1'
            commands = ["gcc", self.code_file, "-o", "Main", "-static", "-w",
                "-lm", "-std=c11", "-O2", "-DONLINE_JUDGE"]
        elif self.language == 'java':
            self.lang = '3'
            commands = ["javac", self.code_file, "-d", "."]
        else:
            raise NoLanguageException
        try:
            subprocess.check_output(commands, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            self.compiler_output = e.output
        except OSError, e:
            logging.error(e)

    def _prepare_exec_file(self):
        if self.language in ['cpp', 'c']:
            exec_file_name_src = 'Main'
            exec_file_name_dst = 'a.out'
        else:
            exec_file_name_src = 'Main.class'
            exec_file_name_dst = 'Main.class'
        exec_file_src = os.path.join(os.getcwd(), exec_file_name_src)
        exec_file_dst = os.path.join(conf.tmp_path, exec_file_name_dst)
        shutil.copyfile(exec_file_src, exec_file_dst)
        commands = ['chmod', '775', exec_file_dst]
        if self.language in ['cpp', 'c']:
            subprocess.call(commands)

    def _prepare_testdata_file(self, file_id):
        logging.info("Prepare testdata %s" % file_id)
        input_file_src = os.path.join(
            conf.testdata_path, self.testdata_id, str(file_id)+".in")
        output_file_src = os.path.join(
            conf.testdata_path, self.testdata_id, str(file_id)+".out")
        input_file_dst = os.path.join(conf.tmp_path, "in.in")
        output_file_dst = os.path.join(conf.tmp_path, "out.out")
        if not os.path.exists(input_file_src) or not os.path.exists(output_file_src):
            raise NoTestDataException
        shutil.copyfile(input_file_src, input_file_dst)
        shutil.copyfile(output_file_src, output_file_dst)

    def _judge(self):
        logging.info("Start Judge!")
        for i in range(self.case_count):
            self._prepare_testdata_file(i)
            self._run()
            self._read_result()
        logging.info("Finish Judge!")

    def _run(self):
        logging.info("GO!GO!GO!")
        commands = ["sudo", "./Core", "-t", self.time_limit,
            "-m", self.memory_limit, "-d", conf.tmp_path, "-l", self.lang]
        subprocess.call(commands)

    def _read_result(self):
        logging.info("Read one case result")
        result_file = open(os.path.join(conf.tmp_path, "result.txt"), 'r')
        status = result_file.readline().strip()
        run_time = result_file.readline().strip()
        run_memory = result_file.readline().strip()
        others = result_file.readline().strip()
        one_case_result = dict((["status", status], ["runtime", run_time],
            ["runmemory", run_memory], ["message", others]))
        self.result["result"].append(one_case_result)

    def _save_result(self):
        logging.info("Save result, result is %s" % self.result)
        if self.compiler_output:
            self.result = ""
        self.save_result_callback(
            id = self.id,
            status = self.result,
            user_id = self.user_id,
            case_count = self.case_count,
            case_score = self.case_score,
            contest_id = self.contest_id,
            problem_id = self.problem_id,
            highest_score = self.highest_score,
            compiler_output = self.compiler_output
        )

        self.lang = 0
        self.compiler_output = None
        self.result = {"result":[]}

    def _clean_files(self):
        logging.info("Clean files")
        if os.path.exists(conf.tmp_path):
            shutil.rmtree(conf.tmp_path)
