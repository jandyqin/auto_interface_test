#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/6/26 16:12
# @Author  : Jandy
# @Email   : jandyqin@gmail.com
# @File    ：api_test.py
# @Software: PyCharm
from common.http_request import http_request
from common.test_base import TestBase
from common.read_config import config


class ApiTest(TestBase):
    # def __init__(self,run,desc,method,url,param,verify,save,results):
    #     self.run=run
    #     #     self.desc = desc
    #     #     self.method = method
    #     #     self.url = url
    #     #     self.param = param
    #     #     self.verify = verify
    #     #     self.save = save
    #     #     self.results = results
    #     #     print('ApiTest__init__')
    rooUrlEndWithSlash = False
    publicHeaders={}
    def __init__(self, host):
        self.rootUrl = config.get('Host', host)  # 获取host配置的请求跟路径
        self.rooUrlEndWithSlash = self.rootUrl.endswith('/')
        self.params = dict(config.items('params'))  # 读取param，并将值保存到公共数据
        super().setSaveDates(self.params)
        self.publicHeaders = dict(config.items('headers'))  # headers，并将值保存到publicHeaders,

    def bean(self, args):
        print('args:{0}'.format(args.param))
        # for i in range(len(args)):
        #     print(args[i].param)
        return 'ok'

    def apiTest(self, apiData):
        apiParam = self.buildRequestParam(apiData)
        response = self.parseHttpRequest(apiData.url, apiData.method, apiParam)
        responseData = response.json()
        if response.status_code == 200:
            super().saveResult(responseData, apiData.save)  # 对返回结果进行提取保存。
            return super().verifyResult(responseData, apiData.verify)  # 验证预期信息

    def buildRequestParam(self, apiData):
        # preParam = super().buildParam(self.params)  # 分析处理预参数 （函数生成的参数）
        # super().savePreParam(preParam)  # 保存预存参数 用于后面接口参数中使用和接口返回验证中
        apiParam = super().buildParam(apiData.param)  # 分析处理预参数 （函数生成的参数）
        return apiParam

    def parseHttpRequest(self, url, method, param):
        publicHeaders = self.publicHeaders
        url = self.parseUrl(url)
        return http_request(url=url, method=method, json=param, headers=publicHeaders)

    def parseUrl(self, shortUrl):
        shortUrl = super().getCommonParam(shortUrl)
        if shortUrl.startswith('http'):
            return shortUrl
        if self.rooUrlEndWithSlash == shortUrl.startswith('/'):
            if self.rooUrlEndWithSlash:
                shortUrl = shortUrl.replace('/', '')
            else:
                shortUrl = '/' + shortUrl

        return self.rootUrl + shortUrl
if __name__ == '__main__':
    json = {'msg': '操作成功', 'status': 100,
            'HeadPortrait': 'http://img01.ydm01.com/images/mobile/user195326/2019/20190102/201901021007161089.jpg',
            'funID': [120000, 120100, 120101, 120102, 120103, 100005, 999999, 999997], 'branchID': 82552,
            'userID': 195326,
            'token': '066e2d0b-d944-43c9-8cbd-b1a5f79096fb',
            'user_type': 0}
    allSave = 'token=$.token;headers:userID=$.__getToken(token)'
    at=ApiTest('rootUrl')
    print('02{0}'.format(at.saveResult(json, allSave)))
    print(at.saveDatas)
    print(at.publicHeaders)
    # print(ApiTest().verifyResult(json, allSave))