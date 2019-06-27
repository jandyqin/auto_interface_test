#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/6/25 10:26
# @Author  : Jandy
# @Email   : jandyqin@gmail.com
# @File    ：utils.py
# @Software: PyCharm
import random
import unittest

from common.functions import *
from common.logger import log


class RandomUtil:
    randomBase = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

    randomNumberBase = "0123456789"

    def getRandom(self, length, onlyNumber):

        if onlyNumber.upper() != 'FALSE':
            base = self.randomNumberBase
        else:
            base = self.randomBase
        str = []
        for i in range(int(length) + 1):
            chr = base[random.randint(0, len(base) - 1)]
            if i != 0 and chr != 0:
                str.append(chr)

        return ''.join(str)

    def Unicode(self, count=1):
        '''
        随机中文字符(unicode码中收录了2万多个汉字,包含很多生僻的繁体字)
        :param count:
        :return:
        '''
        a = 0
        str = ''
        while a < count:
            a += 1
            val = random.randint(0x4e00, 0x9fbf)
            str += chr(val)
        return str

    def GBK2312(self, count=1):
        '''
        随机中文字符(GBK2312收录了6千多常用汉字)
        :param count:
        :return:
        '''
        a = 0
        str = ''
        while a < count:
            a += 1
            head = random.randint(0xb0, 0xf7)
            body = random.randint(0xa1, 0xf9)  # 在head区号为55的那一块最后5个汉字是乱码,为了方便缩减下范围
            val = f'{head:x}{body:x}'
            str += bytes.fromhex(val).decode('gb2312')
        return str


class StringUtil:
    def isNotEmpty(self, str):
        return None != str and "" != str

    def isEmpty(self, str):
        return None == str or "" == str

    def replaceFirst(self, sourceStr, matchStr, replaceStr):
        '''
        :param sourceStr:   待替换字符串
	    :@param matchStr:   匹配字符串
	    :@param replaceStr: 目标替换字符串
        :return:
        '''
        return str(sourceStr).replace(matchStr, replaceStr)


class FunctionUtil:
    functionsMap = {}

    def __init__(self):
        for methods in ClassFinder().getAllAssignedClass():
            self.functionsMap[methods] = methods

    def isFunction(self, functionName):
        return self.functionsMap.__contains__(functionName)

    def getValue(self, functionName, args):
        return ClassFinder().getFunctionValue(functionName, args)
        # if functionName == 'random':
        #     # print('getValue_args:{0}'.format(args))
        #     return Function().random(args)


class ClassFinder:
    imp_module = 'functions'
    imp_class = 'Function'

    def __init__(self):
        import importlib
        ip_module = importlib.import_module('.', self.imp_module)
        ip_module_cls = getattr(ip_module, self.imp_class)
        self.cls_obj = ip_module_cls()

    def getAllAssignedClass(self):
        t = []
        for attr in dir(self.cls_obj):
            # 加载非__前缀的属性
            if attr[0] != '_':
                # print(attr)
                t.append(attr)
        return t

    def getFunctionValue(self, functionName, args):

        return getattr(self.cls_obj, functionName)(args)


class AssertUtil(unittest.TestCase):
    def contains(self, source, search):

        try:
            self.assertEqual(source, search)

        except AssertionError as e:
            # print('测试用例执行]不通过')
            resul = '预期:{0} 包含:{1}，实际为不包含'.format(source, search)
            log.error(e)
            raise e

        else:
            resul = '通过'
        # print('测试用例执行通过')
        finally:
            return resul
