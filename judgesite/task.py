#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
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
        self.status_id = str(task["status_id"])
        self.code = task["code"]
        self.language = task["language"]
        self.testdata_id = str(task["testdata_id"])
        self.time_limit = str(task["time_limit"])
        self.memory_limit = str(task["memory_limit"])

    def go(self):
        self._clean_files()

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
        self.code_file = os.path.join(conf.tmp_path, filename)
        code_file = io.open(self.code_file, 'w', encoding='utf8')
        code_file.write(self.code)
        code_file.close()

    def _prepare_testdata_file(self):
        input_file = os.path.join(conf.testdata_path, self.testdata_id, "in.in")
        output_file = os.path.join(conf.testdata_path, self.testdata_id, "out.out")
        shutil.copy(input_file, conf.tmp_path)
        shutil.copy(output_file, conf.tmp_path)

    def _run(self):
        commands = ["sudo", "./Core", "-c", self.code_file, "-t",
                    self.time_limit, "-m", self.memory_limit, "-d",
                    conf.tmp_path]

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
        if os.path.exists(conf.tmp_path):
            shutil.rmtree(conf.tmp_path)