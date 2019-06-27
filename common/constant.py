#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/6/21 13:14
# @Author  : Jandy
# @Email   : jandyqin@gmail.com
# @File    ：constant.py
# @Software: PyCharm


import os
#根目录
root_path = os.path.dirname(os.path.dirname(__file__))
#配置文件所在目录
config_path = os.path.join(root_path,'config')
#日志文件所在目录
log_path = os.path.join(root_path,'logs')
# 测试用例数据所在目录
data_path = os.path.join(root_path,'data')
# 测试报告所在目录
report_path = os.path.join(root_path,'reports')
# 测试用例类所在目录
testcase_path = os.path.join(root_path,'testcases')
# print(testcase_path)