#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/6/25 10:26
# @Author  : Jandy
# @Email   : jandyqin@gmail.com
# @File    ：functions.py
# @Software: PyCharm
import abc
import six


class Function:

    def random(self, args):
        '''
        随机生成一个定长的字符串(不含中文)。param1:长度(非必填，默认为6)，param2：纯数字标识(非必填，默认为false)。
        :param args:
        :return:
        '''
        lenth = len(args)
        length = 6
        flag = 'false'
        if lenth > 0:
            length = args[0]
        if lenth > 1:
            flag = str(args[1])
        from common.utils import RandomUtil
        return RandomUtil().getRandom(length, flag)

    def randomText(self, args):
        '''
        随机生成一个定长的字符串(含中文)。param1:长度(非必填，默认为6)
        :param args:
        :return:
        '''
        return 'randomText'

    def randomStrArr(self, args):
        '''
        随机生成一个定长字符串数组。param1:数组长度(非必填，默认为1)，param2：单个字符串长度（非必填，默认6），param3：纯数字标识(非必填，默认为false)。
        :param args:
        :return:
        '''

        return 'randomStrArr'

    def date(self, args):
        '''
        生成执行该函数时的格式化字符串。param1为转换的格式，默认为‘yyyy-MM-dd’。
        :param args:
        :return:
        '''
        return 'date'

    def generateStrArrByStr(self, args):
        '''
        生成定长的字符串数组。param1:参数为数组长度 即生成参数个数，param2：字符串
        :param args:
        :return:
        '''
        return 'generateStrArrByStr'

    def sub(self, args):
        '''
        减数。第一个参数作为减数，其他参数均作为被减数。
        :param args:
        :return:
        '''
        return 'sub'

    def max(self, args):
        '''
        获取所有参数的最大值。
        :param args:
        :return:
        '''
        return 'max'

    def plus(self, args):
        '''
        将所有参数进行相加。//参数中其中有一个包含小数点将会返回带小数点的值
        :param args:
        :return:
        '''
        return 'plus'

    def multi(self, args):
        '''
        将所有参数相乘。
        :param args:
        :return:
        '''
        return 'multi'

    # def methods(self):
    #     return (list(filter(lambda m: not m.startswith("__") and not m.endswith("__") and callable(getattr(self, m)),
    #                         dir(self))))


if __name__ == '__main__':
    print(Function().methods())

#
# @six.add_metaclass(abc.ABCMeta)
# class Function(object):
#     @abc.abstractmethod
#     def execute(self, *args):
#         pass
#
#     @abc.abstractmethod
#     def getReferenceKey(self):
#         pass
#
#
# class DateFunction(Function):
#
#     def execute(self, *args):
#         pass
#
#     def getReferenceKey(self):
#         pass
#
#
# class MaxFunction(Function):
#
#     def execute(self, *args):
#         pass
#
#     def getReferenceKey(self):
#         pass
#
#
# class Md5Function(Function):
#
#     def execute(self, *args):
#         pass
#
#     def getReferenceKey(self):
#         pass
#
#
# class MultiFunction(Function):
#
#     def execute(self, *args):
#         pass
#
#     def getReferenceKey(self):
#         pass
#
#
# class PlusFunction(Function):
#
#     def execute(self, *args):
#
#         len = len(args)
#
#         length = 6
#
#         flag = False
#         if len > 0:
#             length = args[0]
#
#         if len > 1:
#             flag = str(args[1])
#
#         return RandomUtil.getRandom(length, flag)
#
#     def getReferenceKey(self):
#         return "random"
#
#
# class RandomFunction(Function):
#
#     def execute(self, *args):
#         pass
#
#     def getReferenceKey(self):
#         pass
#
#
# class RandomStrArrFucntion(Function):
#
#     def execute(self, *args):
#         pass
#
#     def getReferenceKey(self):
#         pass
#
#
# class RandomTextFunction(Function):
#
#     def execute(self, *args):
#         pass
#
#     def getReferenceKey(self):
#         pass
#
#
# class SubFunction(Function):
#
#     def execute(self, *args):
#         pass
#
#     def getReferenceKey(self):
#         pass
#
#
# def getRandomHanZi(length=1):
#     """
#      随机生成一个汉字
#     :param length: 长度
#     :return:
#     """
#     return RandomUtil.Unicode(length)
