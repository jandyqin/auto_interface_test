#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/6/21 13:16
# @Author  : Jandy
# @Email   : jandyqin@gmail.com
# @File    ：read_config.py
# @Software: PyCharm


''
import os
import configparser
from common.constant import config_path
class Configure(configparser.ConfigParser):
    def __init__(self):
        # 实例化对象
        super().__init__()
        #读取配置文件
        self.read(os.path.join(config_path,'config.ini'),encoding='utf8')


config = Configure()
# print(config.get('log','log_name'))
# print(dict(config.items('excel')))