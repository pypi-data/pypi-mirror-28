# -*- coding:utf-8 -*-
"""
获取历史行情
@author: baostock.com
@group : baostock.com
@contact: baostock@163.com
"""
import zlib
import baostock.util.socketutil as sock
import baostock.util.stringutil as strUtil
import baostock.data.resultset as rs
from baostock.data.messageheader import *
import datetime
import time


# 公开调用方法
def query_history_k_data(code, fields, start_date=None, end_date=None,
                         frequency='d', adjustflag='3'):

    return __query_history_k_data_page(1, 10000000, code, fields, start_date, end_date, frequency, adjustflag)


# 私有实际调用方法
def __query_history_k_data_page(cur_page_num, per_page_count, code, fields, start_date, end_date,
                         frequency, adjustflag):
    data = rs.ResultData()
    if code is None or code == "":
        print("股票代码为不能为空，请检查")
        data.error_msg = "股票代码为不能为空，请检查"
        data.error_code = cons.BSERR_PARAM_ERR
        return data
    if len(code) != 9:
        print("股票代码格式错误，请检查")
        data.error_msg = "股票代码格式错误，请检查"
        data.error_code = cons.BSERR_PARAM_ERR
        return data
    if fields is None or code == "":
        data.error_msg = "指示简称不能为空，请检查"
        data.error_code = cons.BSERR_PARAM_ERR
        print("指示简称不能为空，请检查")
        return data
    if start_date is None or code == "":
        start_date = "2015-01-01"
    if end_date is None or code == "":
        end_date = time.strftime("%Y-%m-%d", time.localtime())
    if start_date != "" and end_date != "":
        if (strUtil.is_valid_date(start_date) and strUtil.is_valid_date(end_date)):
            start_date_time = datetime.datetime.strptime(start_date, '%Y-%m-%d')
            end_date_time = datetime.datetime.strptime(end_date, '%Y-%m-%d')
            if end_date_time < start_date_time:
                print("起始日期大于截至日期，请修改")
                data.error_code = cons.BSERR_START_BIGTHAN_END
                data.error_msg = "起始日期大于截至日期，请修改"
                return data
        else:
            print("日期格式不正确，请修改")
            return

    if frequency is None or frequency == "":
        print("频率（frequency）不可设置为空")
        data.error_msg = "频率（frequency）不可设置为空"
        data.error_code = cons.BSERR_PARAM_ERR
        return data
    if adjustflag is None or adjustflag == "":
        print("复权类型（adjustflag）不可设置为空")
        data.error_msg = "复权类型（adjustflag）不可设置为空"
        data.error_code = cons.BSERR_PARAM_ERR
        return data

    msg_body = "__query_history_k_data_page" + cons.MESSAGE_SPLIT + getattr(cons, "user_id") + cons.MESSAGE_SPLIT \
               + str(cur_page_num) + cons.MESSAGE_SPLIT + str(per_page_count) + cons.MESSAGE_SPLIT + code \
               + cons.MESSAGE_SPLIT + fields + cons.MESSAGE_SPLIT + start_date \
               + cons.MESSAGE_SPLIT + end_date + cons.MESSAGE_SPLIT + frequency \
               + cons.MESSAGE_SPLIT + adjustflag

    msg_header = to_message_header(cons.MESSAGE_TYPE_GETKDATA_REQUEST, len(msg_body))

    head_body = msg_header + msg_body
    crc32str = zlib.crc32(bytes(head_body, encoding='utf-8'))
    receive_data = sock.send_msg(head_body + cons.MESSAGE_SPLIT + str(crc32str))

    msg_header = receive_data[0:cons.MESSAGE_HEADER_LENGTH]
    msg_body = receive_data[cons.MESSAGE_HEADER_LENGTH:-1]

    header_arr = msg_header.split(cons.MESSAGE_SPLIT)
    body_arr = msg_body.split(cons.MESSAGE_SPLIT)

    # data.version = header_arr[0]
    data.msg_type = header_arr[1]
    data.msg_body_length = header_arr[2]

    data.error_code = body_arr[0]
    data.error_msg = body_arr[1]

    if cons.BSERR_SUCCESS == data.error_code:
        data.method = body_arr[2]
        data.user_id = body_arr[3]
        data.cur_page_num = body_arr[4]
        data.per_page_count = body_arr[5]
        data.code = body_arr[6]
        data.fields = body_arr[7]
        data.start_date = body_arr[8]
        data.end_date = body_arr[9]
        data.frequency = body_arr[10]
        data.adjustflag = body_arr[11]
        data.data = body_arr[12]

    return data
