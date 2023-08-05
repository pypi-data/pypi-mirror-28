# -*- coding:utf-8 -*-
"""
字符串方法
@author: baostock.com
@group : baostock.com
@contact: baostock@163.com
"""
import datetime


def add_zero_for_string(content, length, direction):
    """
    在str的左或右添加0
    :param str:待修改的字符串
    :param length:总共的长度
    :param direction:方向，True左，False右
    :return:
    """
    content = str(content)
    str_len = len(content)
    if str_len < length:
        while str_len < length:
            if direction:
                content = "0" + content
            else:
                content = content + "0"

            str_len = len(content)
    return content

def is_valid_date(str):
    """
    判断是否是一个有效的日期字符串
    :param str:
    :return: 符合格式返回True,
    """
    try:
        datetime.datetime.strptime(str, "%Y-%m-%d")
        return True
    except:
        return False
