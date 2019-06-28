#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/6/25 11:27
# @Author  : Jandy
# @Email   : jandyqin@gmail.com
# @File    ：test_base.py
# @Software: PyCharm
import json
import re
import unittest

import jsonpath as jsonpath

from common.http_request import http_request
from common.logger import log
from common.read_config import config
from common.utils import *
from common.do_excel import ReadExcel
from common.read_config import config
from common.constant import data_path
import os

class TestBase():
    saveDatas = {}  # 公共参数数据池（全局可用）
    publicHeaders = {}
    caseList = []
    rooUrlEndWithSlash = False
    rootUrl=''
    replaceParamPattern = re.compile(r'\${(.*?)}', re.M | re.I)  # 替换符，如果数据中包含“${}”则会被替换成公共参数中存储的数据
    funPattern = re.compile(r'__(\w*?)\((([\w:.$]*,?)*)\)', re.M | re.I)  # 截取自定义方法正则表达式：__xxx(ooo)

    def __init__(self):
        self.params = dict(config.items('params'))  # 读取param，并将值保存到公共数据
        self.setSaveDates(self.params)
        self.publicHeaders = dict(config.items('headers'))  # headers，并将值保存到publicHeaders,
        self.rootUrl = config.get('Host', 'rootUrl')  # 获取host配置的请求跟路径
        self.rooUrlEndWithSlash = self.rootUrl.endswith('/')
        # FunctionUtil()
    def setSaveDates(self, dict):
        '''将新的词典更新到参数池'''
        self.saveDatas.update(dict)

    def buildParam(self, param):
        '''
        组件预处理
        :param param:
        :return:
        '''
        param = self.getCommonParam(param)
        it = self.funPattern.finditer(param)
        for matcher in it:
            funcName = matcher.group(1)
            args = matcher.group(2)
            if FunctionUtil().isFunction(funcName):
                value = FunctionUtil().getValue(funcName, args.split(","))
                param = param.replace(matcher.group(), str(value))
            # matcher = self.replaceParamPattern.search(param)
        return param

    def savePreParam(self, preParam):
        '''
        将参数加入参数池中
        :param param:
        :return:
        '''
        if StringUtil().isEmpty(preParam):
            return
        preParamArr = preParam.split(";")
        for prepar in preParamArr:
            if StringUtil().isEmpty(prepar):
                continue
            key = prepar.split('=')[0]
            value = prepar.split('=')[1]

            log.info('存储{0}参数，值为：{1}。'.format(key, value))
            self.saveDatas[key] = value

    def getCommonParam(self, param):
        '''
        取公共参数 并替换参数
        :param param:
        :return:
        '''
        param = str(param)
        if (StringUtil().isEmpty(str=param)):
            return ''
        # matcher = self.replaceParamPattern.search(param)  # 取公共参数正则
        it = self.replaceParamPattern.finditer(param)  # 取公共参数正则
        for matcher in it:
            replaceKey = matcher.group(1)
            # 从公共参数池中获取值
            value = self.getSaveData(replaceKey)
            param = param.replace(matcher.group(), str(value))

        return param

    def getSaveData(self, replaceKey=None):
        '''
        获取公共数据池中的数据
        :param replaceKey:
        :return:
        '''
        try:
            return self.saveDatas[replaceKey]
        except Exception:
            log.error("格式化参数失败，公共参数中找不到{0}".format(replaceKey))
            return ''

    def verifyResult(self, sourchData, verifyStr, contains=False):
        '''
        验证数据
        :param sourchData:
        :param verifyStr:
        :param contains:
        :return:
        '''
        if (StringUtil().isEmpty(verifyStr)):
            return
        allVerify = self.getCommonParam(verifyStr)
        log.info('验证数据：{0}'.format(allVerify))
        if contains:
            AssertUtil().contains(sourchData, allVerify)
        else:
            pattern = re.compile("([^;]*)=([^;]*)")
            it = pattern.finditer(allVerify)
            for matcher in it:
                actualValue = self.getBuildValue(sourchData, matcher.group(1))
                exceptValue = self.getBuildValue(sourchData, matcher.group(2))
                log.info('验证转换后的值{0}={1} '.format(actualValue, exceptValue))

                param = allVerify.replace(matcher.group(), str(''))
                AssertUtil().contains(actualValue, exceptValue)
                # return self.assertEquals(actualValue, exceptValue, "验证预期结果。")

    def getBuildValue(self, sourchJson, key):
        '''
        获取格式化后的值
        :param sourchJson:
        :param key:
        :return:
        '''
        key = "".join(key.split())
        match = self.funPattern.finditer(key)
        if key.startswith("$."):
            key = self.myFormat(eval(str(jsonpath.jsonpath(sourchJson, key))))
        elif match != None:
            for matcher in match:
                args = matcher.group(2)
                argArr = args.split(",")
                for index in range(len(argArr)):
                    arg = argArr[index]
                    if arg.startswith("$."):
                        argArr[index] = str(jsonpath.jsonpath(sourchJson, arg))
                        print(argArr)
                value = FunctionUtil().getValue(matcher.group(1), argArr)
                key = StringUtil().replaceFirst(key, matcher.group(), value)
        return key

    def saveResult(self, json, allSave):
        '''
        :param json:将被提取的json串。
        :param allSave:所有将被保存的数据：xx=$.jsonpath.xx;oo=$.jsonpath.oo，将$.jsonpath.
                        xx提取出来的值存放至公共池的xx中，将$.jsonpath.oo提取出来的值存放至公共池的oo中
        :return:
        '''

        if None == json or '' == json or None == allSave or '' == allSave:
            return
        allSave = self.getCommonParam(allSave)
        saves = allSave.split(";")
        pattern = re.compile("([^;=]*)=([^;]*)")
        for save in saves:
            it = pattern.finditer(save)
            for matcher in it:
                key = self.getBuildValue(json, matcher.group(1))
                value = self.getBuildValue(json, matcher.group(2))
                log.info("存储公共参数 {0} 值为：{1}.".format(key, value))
                if key.startswith("headers:"):
                    key = key.replace('headers:', '')
                    self.publicHeaders[key] = value
                    continue
                self.saveDatas[key] = value

    def myFormat(self,args):
        return args[0]

    def filterData(self, casedata=None):
        '''
        过滤数据，run标记为Y的执行。
        :param data:
        :return:
        '''
        data = []
        if casedata != None:
            caselist = casedata
        else:
            caselist = self.caseList
        for i in range(len(caselist)):
            # print(caselist[i].run)
            if StringUtil().isNotEmpty(getattr(caselist[i],'run')):
                data.append(caselist[i])
        return data
    def loadingDataConfig(self,Host,excel_name,Sheet_name):
        # 从配置文件中读取文件名，表单名，列数
        file_name = config.get('excel', 'excel_name')

        file_path = os.path.join(data_path, file_name)
        sheet_name = config.get('excel', 'Sheet_name')
        columns = config.get('excel', 'columns')
        self.rootUrl = config.get('Host',Host)  # 获取host配置的请求跟路径
        self.rooUrlEndWithSlash = self.rootUrl.endswith('/')
        self.params = dict(config.items('params'))  # 读取param，并将值保存到公共数据
        self.setSaveDates(self.params)
        self.publicHeaders = dict(config.items('headers'))  # headers，并将值保存到publicHeaders,
    def readExcelData(self):

        # 从配置文件中读取文件名，表单名，列数
        file_name = config.get('excel', 'excel_name')

        file_path = os.path.join(data_path, file_name)
        sheet_name = config.get('excel', 'Sheet_name')
        columns = config.get('excel', 'columns')
        self.rootUrl = config.get('Host', 'rootUrl')  # 获取host配置的请求跟路径
        self.rooUrlEndWithSlash = self.rootUrl.endswith('/')
        self.params = dict(config.items('params'))  # 读取param，并将值保存到公共数据
        self.setSaveDates(self.params)
        self.publicHeaders = dict(config.items('headers'))  # headers，并将值保存到publicHeaders,

        # 读取表格数据
        r = ReadExcel(file_path, sheet_name)
        cases = r.r_data_obj(columns)
        return cases

    def buildRequestParam(self, apiData):
        # preParam = super().buildParam(self.params)  # 分析处理预参数 （函数生成的参数）
        # super().savePreParam(preParam)  # 保存预存参数 用于后面接口参数中使用和接口返回验证中
        apiParam = self.buildParam(apiData.param)  # 分析处理预参数 （函数生成的参数）
        return apiParam

    def parseHttpRequest(self, url, method, param):
        publicHeaders = self.publicHeaders
        url = self.parseUrl(url)
        return http_request(url=url, method=method, json=param, headers=publicHeaders)

    def parseUrl(self, shortUrl):
        shortUrl = self.getCommonParam(shortUrl)
        if shortUrl.startswith('http'):
            return shortUrl
        if self.rooUrlEndWithSlash == shortUrl.startswith('/'):
            if self.rooUrlEndWithSlash:
                shortUrl = shortUrl.replace('/', '')
            else:
                shortUrl = '/' + shortUrl

        return self.rootUrl + shortUrl
if __name__ == '__main__':
    # line = str({"account": "${account}", "hgh": "__random(8,true)", "pwd": "__random(20,FALSE)",
    #             "gg": "__randomStrArr(20,FALSE)"})
    # Matcher = TestBase().replaceParamPattern.search(line)
    # # TestBase().saveDatas[]
    # print(Matcher.group())
    # param = re.sub(r'\${(.*?)}', '', line, count=0, flags=0)
    # print(param)
    # print(TestBase().buildParam(param=line))


    json = {'msg': '操作成功', 'status': 100,
            'HeadPortrait': 'http://img01.ydm01.com/images/mobile/user195326/2019/20190102/201901021007161089.jpg',
            'funID': [120000, 120100, 120101, 120102, 120103, 100005, 999999, 999997], 'branchID': 82552,
            'userID': 195326,
            'token': '066e2d0b-d944-43c9-8cbd-b1a5f79096fb',
            'user_type': 0}
    allSave = 'token=$.token;headers:userID=$.funID'
    print('02{0}'.format(TestBase().saveResult(json, allSave)))
    print(TestBase().saveDatas)
    print(TestBase().publicHeaders)




    # for x in TestBase().filterData():
    #     print(getattr(x,'param'))
    #     print(x.__dict__)
    #     apiParam = TestBase().buildRequestParam(x)
    #     print(eval(apiParam))
    #     json = {"account":"13316521269","pwd":"896675512b24e11715f33d87728ef7ba"}
    #     print(json)
    #     url = 'https://saas.ydm01.cn/api/admin/ManagerStorePWDLogin'
    #     response = TestBase().parseHttpRequest(url, x.method, json)
    #     print(response)
        # responseData = json.dumps(response)
    # print(str(TestBase().filterData()[0].parparam))
