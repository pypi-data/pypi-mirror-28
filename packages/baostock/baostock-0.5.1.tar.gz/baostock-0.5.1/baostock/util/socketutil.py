# -*- coding:utf-8 -*-
"""
获取默认socket
@author: baostock.com
@group : baostock.com
@contact: baostock@163.com
"""
import socket
import baostock.common.contants as cons


def get_default_socket():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((cons.BAOSTOCK_SERVER_IP, cons.BAOSTOCK_SERVER_PORT))
    except TimeoutError:
        print("服务器连接失败，请稍后再试。")
    return sock


def send_msg(content):
    try:
        default_socket = get_default_socket()
        default_socket.send(bytes(content, encoding='utf-8'))  # str 类型 -> bytes 类型

        receive = ""
        while True:
            recv = default_socket.recv(1024)
            temp_data = bytes.decode(recv)
            receive += temp_data
            if not temp_data:
                break
        default_socket.close()
        return receive
    except OSError:
        print("地址连接不正确。")
    except Exception:
        print("未成功发送数据。")

