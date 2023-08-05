# -*- coding:utf-8 -*-
"""
返回数据接口
@author: baostock.com
@group : baostock.com
@contact: baostock@163.com
"""
import baostock.common.contants as cons
import pandas as pd
import json


class ResultData(object):
    def __init__(self):
        """
        初始化方法
        """

        # 消息头
        self.version = cons.BAOSTOCK_CLIENT_VERSION
        self.msg_type = 0
        self.msg_body_length = 0

        # 消息体
        self.method = ""  # 方法名
        self.user_id = ""  # 用户账号
        self.error_code = cons.BSERR_NO_LOGIN  # 错误代码

        self.cur_page_num = 1  # 当前页码
        self.per_page_count = 10000  # 当前页条数
        self.code = ""  # 股票代码
        self.fields = ""  # 指示简称
        self.start_date = ""  # 开始日期
        self.end_date = ""  # 结束日期
        self.frequency = ""  # 数据类型
        self.adjustflag = ""  # 复权类型
        self.data = ""  # 数据值

        # self.request_id = 0
        # self.serial_id = 0

    def next(self):
        """
        判断是否还有后续数据
        :return: 有数据返回True，没有数据返回False
        """
        return False

    def get_data(self):
        """
        对返回结果进行处理
        :return:DataFrame类型
        """

        if self.data == "":
            return pd.DataFrame()

        # 对数据进行格式化
        js_data = json.loads(self.data)
        # 对列名进行拆分
        field_arr = self.fields.split(cons.ATTRIBUTE_SPLIT)

        i = 0
        while i < len(field_arr):
            # 去除空格
            field_arr[i] = field_arr[i].strip()
            i += 1
        # 组织返回数据
        df = pd.DataFrame(js_data['record'], columns=field_arr)
        return df
