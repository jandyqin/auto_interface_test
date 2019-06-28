# #!/usr/bin/python3
# # -*- coding: utf-8 -*-
# # @Time    : 2019/6/17 12:14
# # @Author  : Jandy
# # @Email   : jandyqin@gmail.com
# # @File    ：testcase.py
# # @Software: PyCharm
# import json
# import re
# import unittest
# import os
#
# from common.logger import log
# from common.test_base import TestBase, StringUtil
#
# from librarys.ddt import ddt,data
#
# #创建测试类
# @ddt
# class RegisterTestcase(unittest.TestCase,TestBase):
#     #重写父类__init__方法
#     # def __init__(self,methodName,case_obj):
#     #     self.data = eval(case_obj.data)
#     #     self.expected = eval(case_obj.expected)
#     #     self.row =case_obj.case_id +1
#     #     super().__init__(methodName)
#
#     # def setUp(self):
#     #     print('执行测试用例前执行')
#     # def tearDown(self):
#     #     print('测试用例执行后执行')
#     tb=TestBase()
#     cases = tb.filterData()
#
#     @data(*cases)
#     def test_normal(self,case):
#         '''
#
#         :param case: 测试用例对象
#         :return:
#         '''
#
#         apiParam = TestBase().buildRequestParam(case)
#         response = TestBase().parseHttpRequest(case.url, case.method, eval(apiParam))
#         responseData=response.json()
#         print('responseData:{}'.format(responseData))
#         if response.status_code == 200:
#             super().saveResult(responseData, case.save)  # 对返回结果进行提取保存。
#             # return super().verifyResult(responseData, case.verify)  # 验证预期信息
#             verifyStr=case.verify
#             if (StringUtil().isEmpty(verifyStr)):
#                 return
#             allVerify = self.getCommonParam(verifyStr)
#             log.info('验证数据：{0}'.format(allVerify))
#             if False:
#                 AssertUtil().contains(sourchData, allVerify)
#             else:
#                 pattern = re.compile("([^;]*)=([^;]*)")
#                 it = pattern.finditer(allVerify)
#                 for matcher in it:
#                     actualValue = self.getBuildValue(responseData, matcher.group(1))
#                     exceptValue = self.getBuildValue(responseData, matcher.group(2))
#                     log.info('验证转换后的值:{0}=?{1} '.format(actualValue, exceptValue))
#
#                     param = allVerify.replace(matcher.group(), str(''))
#                     # AssertUtil().contains(actualValue, exceptValue)
#             try:
#                 log.debug('actualValue:{0}=exceptValue:{1}'.format(str(actualValue), str(exceptValue)))
#                 self.assertEqual(str(actualValue), str(exceptValue))
#             except AssertionError as e :
#                 # print('测试用例执行]不通过')
#                 resul = '失败'
#                 log.error(e)
#                 raise e
#             else:
#                 resul = '通过'
#
#                 # print('测试用例执行通过')
#             finally:
#                 log.info('用例id为:{}，用例标题为:{}，结果是:{}'.format(case.case_row_id-1, case.desc, resul))
#                 r = ReadExcel(file_name,sheet_name)
#                 r.write(case.case_row_id,8,resul)
#
# if __name__ =='__main__':
#     unittest.main()