#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/6/25 11:27
# @Author  : Jandy
# @Email   : jandyqin@gmail.com
# @File    ：test_base.py
# @Software: PyCharm
import re
import unittest

import jsonpath as jsonpath

from common.logger import log
from common.utils import *


class TestBase(unittest.TestCase):
    saveDatas = {}  # 公共参数数据池（全局可用）

    replaceParamPattern = re.compile(r'\${(.*?)}', re.M | re.I)  # 替换符，如果数据中包含“${}”则会被替换成公共参数中存储的数据
    funPattern = re.compile(r'__(\w*?)\((([\w:.$]*,?)*)\)', re.M | re.I)  # 截取自定义方法正则表达式：__xxx(ooo)

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
                return self.assertEquals(actualValue, exceptValue, "验证预期结果。")

    def getBuildValue(self, sourchJson, key):
        '''
        获取格式化后的值
        :param sourchJson:
        :param key:
        :return:
        '''
        key = "".join(key.split())
        match  = self.funPattern.finditer(key)
        if key.startswith("$."):
            key = str(jsonpath.jsonpath(sourchJson, key))
        elif match  != None:
            for matcher in match:
                args = matcher .group(2)
                argArr = args.split(",")
                for index in range(len(argArr)):
                    arg = argArr[index]
                    if arg.startswith("$."):
                        argArr[index] = str(jsonpath.jsonpath(sourchJson, arg))
                value = FunctionUtil.getValue(matcher .group(1), argArr)
                key = StringUtil.replaceFirst(key, matcher .group(), value)
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
        for save in saves:
            pattern = re.compile("([^;=]*)=([^;]*)")

            it = pattern.finditer(save)
            for matcher in it:
                key = self.getBuildValue(json, matcher.group(1))
                value = self.getBuildValue(json, matcher.group(2))

                log.info("存储公共参数 {0} 值为：{1}.".format(key, value))
                self.saveDatas[key] = value

    def filterData(self, data):
        '''
        过滤数据，run标记为Y的执行。
        :param data:
        :return:
        '''
        return data


if __name__ == '__main__':
    line = str({"account": "${account}", "hgh": "__random(8,true)", "pwd": "__random(20,FALSE)",
                "gg": "__randomStrArr(20,FALSE)"})
    # Matcher = TestBase().replaceParamPattern.search(line)
    # # TestBase().saveDatas[]
    # print(Matcher.group())
    # param = re.sub(r'\${(.*?)}', '', line, count=0, flags=0)
    # print(param)
    print(TestBase().buildParam(param=line))
