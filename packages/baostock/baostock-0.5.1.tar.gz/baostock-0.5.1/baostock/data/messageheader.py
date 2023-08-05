# -*- coding:utf-8 -*-
"""
封装消息头
@author: baostock.com
@group : baostock.com
@contact: baostock@163.com
"""
from baostock.util.stringutil import *
import baostock.common.contants as cons


def to_message_header(msg_ype, total_msg_length):

    return_str = cons.BAOSTOCK_CLIENT_VERSION + cons.MESSAGE_SPLIT + msg_ype \
                 + cons.MESSAGE_SPLIT \
                 + add_zero_for_string(total_msg_length, 10, True)
    return return_str
