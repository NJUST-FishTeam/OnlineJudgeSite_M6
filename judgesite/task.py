#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import shutil
import subprocess
import os

from config import conf
from models import save_result


class JudgeTask(object):

    def __init__(self, message):
        task = json.loads(message)
        self.submit_type = task["submit_type"]
        self.status_id = task["status_id"]
        self.code = task["code"]
        self.language = task["language"]
        self.testdata_id = task["testdata_id"]
        self.time_limit = task["time_limit"]
        self.memory_limit = task["memory_limit"]

    def go(self):
        self._prepare_temp_dir()

        self._dump_code_to_file()

        self._prepare_testdata_file()

        self._run()

        self._read_result()

        self._save_result()

        self._clean_files()

    def _prepare_temp_dir(self):
        os.mkdir(conf.tmp_path)

    def _dump_code_to_file(self):
        filename = "Main." + self.language
        code_file = open(os.path.join(conf.tmp_path, filename), 'w')
        self.code_file = code_file
        code_file.write(self.code)
        code_file.close()

    def _prepare_testdata_file(self):
        input_file = os.path.join(conf.testdata_path, "in.in")
        output_file = os.path.join(conf.testdata_path, "out.out")
        shutil.copy(input_file, conf.tmp_path)
        shutil.copy(output_file, conf.tmp_path)

    def _run(self):
        commands = []
        commands.append("sudo")
        commands.append("./Core")
        commands.append("-c")
        commands.append(self.code_file)
        commands.append("-t")
        commands.append(self.time_limit)
        commands.append("-m")
        commands.append(self.memory_limit)
        commands.append("-d")
        commands.append(conf.tmp_path)

        subprocess.call(commands)

    def _read_result(self):
        result_file = open(os.path.join(conf.tmp_path, "result.txt"), 'r')
        self.result = result_file.readline().strip()
        self.run_time = result_file.readline().strip()
        self.run_memory = result_file.readline().strip()
        self.others = result_file.read()

    def _save_result(self):
        save_result(status_id=self.status_id,
                    type=self.submit_type,
                    run_time=self.run_time,
                    run_memory=self.run_memory,
                    compiler_output=self.others,
                    status=self.result)

    def _clean_files(self):
        shutil.rmtree(conf.tmp_path)