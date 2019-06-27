#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/6/17 12:14
# @Author  : Jandy
# @Email   : jandyqin@gmail.com
# @File    ：testcase.py
# @Software: PyCharm

import unittest
import os

from common import api_test
from common.logger import log
from register import register1
import register
# from ddt import ddt,data
from common.do_excel import ReadExcel
from librarys.ddt import ddt, data
# from day17.log_pr03 import MyLogging
from common.read_config import *
from common.constant import data_path

# 从配置文件中读取文件名，表单名，列数
file_name = config.get('excel', 'excel_name')
file_path = os.path.join(data_path, file_name)
sheet_name = config.get('excel', 'Sheet_name')
columns = config.get('excel', 'columns')

# 读取表格数据
r = ReadExcel(file_path, sheet_name)
cases = r.r_data_obj(columns)

httpresul=api_test.ApiTest('rootUrl')
# 实例化日志收集器
# 创建测试类
@ddt
class RegisterTestcase(unittest.TestCase):
    # 重写父类__init__方法

    @data(*cases)
    def test__normal(self, case):
        '''

        :param case: 测试用例对象
        :return:
        '''
        resul = httpresul.apiTest(case)
        row = case.case_row_id
        print(case.desc)
        try:
            self.assertEqual(case.verify, resul)
        except AssertionError as e:
            # print('测试用例执行]不通过')
            resul = '失败'
            log.error(e)
            raise e
        else:
            resul = '通过'

            # print('测试用例执行通过')
        finally:
            # r = ReadExcel(file_name,sheet_name)
            log.info('用例id为:{}，用例标题为:{}，结果是:{}'.format(case.case_row_id - 1, case.desc, resul))
            r.write(row, 8, resul)


if __name__ == '__main__':
    unittest.main()
