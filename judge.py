#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import

import config
import os
import shutil
import subprocess

def judge(source_code_path, lang, test_data_id,
        time_limit=1000, memory_limit=65535,
        spj=False, spj_lang=config.LANG_UNKOWN):
    '''
    判题模块对外提供的接口

    输入：
    source_code_path 源代码路径
    lang             程序语言，见config文件
    test_data_id     测试数据的ID
    time_limit       时间限制
    memory_limit     内存限制
    spj              是否是SpecialJudge
    spj_lang         SpecialJudge程序使用的语言

    输出：
    返回一个字典
    result = {
            'status':'System Error', # 判题结果，System Error是默认状态
            'run_time':'0',          # 运行时间
            'run_memory':'0',        # 运行内存
            'extra_message':''       # 额外信息，如编译错误信息
        }
    '''

    code_path = _prepare_files(source_code_path, lang, test_data_id, spj)
    _run_core(code_path, time_limit, memory_limit, spj, spj_lang)
    _clean_files()

    return _get_result()

def _prepare_files(source_code_path, lang, test_data_id, spj=False):
    # 准备代码文件
    if lang == config.LANG_C:
        code = os.path.join(config.run_dir, 'code.c')
    elif lang == config.LANG_CPP:
        code = os.path.join(config.run_dir, 'code.cpp')
    elif lang == config.LANG_JAVA:
        code = os.path.join(config.run_dir, 'Main.java')

    shutil.copyfile(source_code_path, code)

    # 准备输入输出测试数据
    input_file = os.path.join(config.data_dir, str(test_data_id), 'in.in')
    output_file = os.path.join(config.data_dir, str(test_data_id), 'out.out')

    shutil.copy(input_file, config.run_dir)
    shutil.copy(output_file, config.run_dir)

    # 准备SpecialJudge程序
    if spj:
        spj_flie = os.path.join(config.data_dir, str(test_data_id), 'SpecialJudge')
        shutil.copy(spj_flie, config.run_dir)

    return code

def _clean_files():
    shutil.rmtree(config.run_dir)
    os.mkdir(config.run_dir)

def _run_core(code_path, time_limit, memory_limit, spj=False, spj_lang=config.LANG_UNKOWN):
    parameter = []
    parameter.append("sudo")
    parameter.append(config.core_dir)
    parameter.append("-c")
    parameter.append(code_path)

    parameter.append("-t")
    parameter.append(str(time_limit))

    parameter.append("-m")
    parameter.append(str(memory_limit))

    parameter.append("-d")
    parameter.append(config.run_dir)

    if spj:
        parameter.append("-s")
        parameter.append("-S")
        parameter.append(str(spj_lang))

    subprocess.call(parameter)

def _get_result():
    result = {
            'status':'System Error',
            'run_time':'0',
            'run_memory':'0',
            'extra_message':''
        }
    try:
        result_file = open(os.path.join(config.run_dir, 'result.txt'))
    except IOError, e:
        config.logger.error("无判题结果文件")
        config.logger.error(e)
    else:
        result['status'] = result_file.readline()
        result['run_time'] = result_file.readline()
        result['run_memory'] = result_file.readline()
        result['extra_message'] = result.read()

    return result


