#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/6/17 11:52
# @Author  : Jandy
# @Email   : jandyqin@gmail.com
# @File    ：run.py
# @Software: PyCharm
import unittest
import os

from common.read_config import config
from librarys.HTMLTestRunnerNew import HTMLTestRunner
from common.constant import testcase_path
from common.constant import report_path

# from HTMLTestRunnerNew import HTMLTestRunner
#获取报告文件名
report_name = config.get('report','report_name')
#创建测试集合
suite = unittest.TestSuite()
#创建加载套件
loader = unittest.TestLoader()
suite.addTest(loader.discover(testcase_path))



with open(os.path.join(report_path,report_name),'wb+') as f:
    runner = HTMLTestRunner(
        stream=f,
        verbosity=2,
        title='接口测试',
        description='api测试',
        tester='jandy')
    runner.run(suite)