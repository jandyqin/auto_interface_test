#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/6/17 11:55
# @Author  : Jandy
# @Email   : jandyqin@gmail.com
# @File    ：logger.py
# @Software: PyCharm
import logging
import os.path
import time
import sys

from common.constant import log_path
from common.read_config import config

class MyLog:
    def __init__(self, log_name):
        self.log_name = log_name

    def my_log(self, msg, level):
        logger = logging.getLogger(self.log_name)
        logger.setLevel('DEBUG')
        # 日志输出格式
        formatter = logging.Formatter('%(asctime)s-%(levelname)s-%(filename)s-%(name)s-日志信息：%(message)s')
        # 日志输出器 控制台 指定文件
        ch = logging.StreamHandler()
        ch.setLevel('DEBUG')
        ch.setFormatter(formatter)
        # log_time = time.strftime('%Y-%m-%d')  # 获取时间G:\devCode\auto_test_interface\test_result
        # log_path = os.path.dirname(
        #     os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0]))))) + '/test_result/log/'
        # path = log_path + str(log_time) + '.log'

        # 日志存放地址
        fh = logging.FileHandler(file_path, encoding='UTF-8')
        fh.setLevel('DEBUG')
        fh.setFormatter(formatter)

        logger.addHandler(ch)
        logger.addHandler(fh)

        if level == 'DEBUG':
            logger.debug(msg)
        elif level == 'INFO':
            logger.info(msg)
        elif level == 'WARNING':
            logger.warning(msg)
        elif level == 'ERROR':
            logger.error(msg)
        elif level == 'CRITICAL':
            logger.critical(msg)

        logger.removeHandler(ch)
        logger.removeHandler(fh)

    def debug(self, msg):
        self.my_log(msg, 'DEBUG')

    def info(self, msg):
        self.my_log(msg, 'INFO')

    def warning(self, msg):
        self.my_log(msg, 'WARNING')

    def error(self, msg):
        self.my_log(msg, 'ERROR')

    def critical(self, msg):
        self.my_log(msg, 'CRITICAL')

class MyLogging:

    def create_mylog(self,name,level,file_path):
        '''

        :param name:日志收集器名字
        :param level:日志等级
        :param file_path:日志路径
        :return:返回日志收集器
        '''
        # 创建日志收集器
        my_log = logging.getLogger(name)
        #设置日志收集器级别
        my_log.setLevel(level)

        #日志输出渠道
        # 创建一个日志输出渠道，输出到控制台
        l_s =logging.StreamHandler()
        l_s.setLevel('DEBUG')

        #创建一个日志输出渠道，输出到文件
        l_f =logging.FileHandler(file_path,encoding='utf8')
        l_f.setLevel('DEBUG')


        #将日志输出渠道添加打收集器中
        my_log.addHandler(l_s)
        my_log.addHandler(l_f)

        #设置日志输出格式
        ft ='%(asctime)s - [%(filename)s-->line:%(lineno)d] - %(levelname)s: %(message)s'
        # ft = '%(asctime)s-%(levelname)s-%(filename)s-%(name)s-日志信息：%(message)s'
        ft = logging.Formatter(ft)
        l_s.setFormatter(ft)
        l_f.setFormatter(ft)

        #返回日志收集器
        return my_log
# 获取配置文件中日志收集器的名字
log_name = config.get('log','logger_name')
# 获取配置文件中的日志级别
log_level =config.get('log','level').upper()
#日志文件名
file_name =config.get('log','log_name')
#日志文件路径
file_path = os.path.join(log_path,str(time.strftime('%Y-%m-%d')) + file_name)

#创建日志收集器
log =MyLogging().create_mylog(log_name,log_level,file_path)
#输出日志
# my_log.debug('debug级别')
# my_log.info('info级别')
# my_log.warning('warning级别')
# my_log.error('error级别')
# my_log.critical('critical日志级别')
