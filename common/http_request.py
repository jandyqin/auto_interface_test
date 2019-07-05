#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/6/27 10:19
# @Author  : Jandy
# @Email   : jandyqin@gmail.com
# @File    ：http_request.py
# @Software: PyCharm
import requests

from common.logger import log


def http_request(url=None, method=None, json=None, headers=None):
    try:

        log.info('请求的json：{0}'.format(json))
        log.info('请求的url：{0}'.format(url))
        log.info('请求的method：{0}'.format(method))
        log.info('请求的headers：{0}'.format(headers))
        if method.upper() == 'GET':
            try:
                response = requests.get(url=url, headers=headers, params=json)
            except Exception as  e:
                print('Error:GET请求方式错误报错{0}'.format(e))
                response = 'Error:GET请求方式错误报错{0}'.format(e)
                log.error(response)
        elif method.upper() == 'POST':

            try:
                response = requests.post(url=url, json=json, headers=headers)
            except Exception as  e:
                print('Error:POST请求方式错误报错{0}'.format(e))
                response = 'Error:POST请求方式错误报错{0}'.format(e)
                log.error(response)
        else:
            print('Error:请求方式错误报错{0}'.format(method))
            response = 'Error:请求方式错误报错{0}'.format(method)
            log.error(response)
    except Exception as  e:
        log.error(e)
        return e
    log.info('返回的数据：{0}'.format(response.json()))
    return response


if __name__ == '__main__':
    headers = {'content-type': 'application/json', 'charset': 'utf-8'}
    json = {"account": "13316521269", "pwd": "896675512b24e11715f33d87728ef7ba"}
    url = 'https://saas.ydm01.cn/api/admin/ManagerStorePWDLogin'
    res_login = http_request(url=url, method="post",
                             json=json, headers=headers)
    print(res_login)
