# -*- coding:utf-8 -*-
"""
获取默认socket
@author: baostock.com
@group : baostock.com
@contact: baostock@163.com
"""
import socket
import baostock.common.contants as cons
import baostock.common.context as context

class SocketUtil(object):
    """Socket工具类"""
    # 记录第一个被创建对象的引用
    instance = None
    # 记录是否执行过初始化动作
    init_flag = False

    def __new__(cls, *args, **kwargs):
        # 1. 判断类属性是否是空对象
        if cls.instance is None:
            # 2. 调用父类的方法，为第一个对象分配空间
            cls.instance = super().__new__(cls)
        # 3. 返回类属性保存的对象引用
        return cls.instance

    def __init__(self):
        SocketUtil.init_flag = True

#         # 1. 判断是否执行过初始化动作
#         if SocketUtil.init_flag:
#             return
#         # 2. 如果没有执行过，在执行初始化动作
#         self.instance = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         self.instance.connect((cons.BAOSTOCK_SERVER_IP, cons.BAOSTOCK_SERVER_PORT))
#         # 3. 修改类属性的标记
#         SocketUtil.init_flag = True

    def connect(self):
        """创建连接"""
        try:
            mySockect = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            mySockect.connect((cons.BAOSTOCK_SERVER_IP, cons.BAOSTOCK_SERVER_PORT))
        except Exception:
            print("服务器连接失败，请稍后再试。")
        setattr(context, "default_socket", mySockect)


def get_default_socket():
    """获取默认连接"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((cons.BAOSTOCK_SERVER_IP, cons.BAOSTOCK_SERVER_PORT))
    except Exception:
        print("服务器连接失败，请稍后再试。")
        return None
    return sock


def send_msg(msg):
    """发送消息，并接受消息 """
    try:
        # default_socket = get_default_socket()
        if hasattr(context, "default_socket"):
            default_socket = getattr(context, "default_socket")
            if default_socket is not None:
                # str 类型 -> bytes 类型
                msg += "\n"  # 在消息结尾追加“消息之间的分隔符”
                default_socket.send(bytes(msg, encoding='utf-8'))
                receive = ""
                while True:
                    recv = default_socket.recv(1024)
                    temp_data = bytes.decode(recv)
                    # 判断是否存在消息结束符
                    receive += temp_data
    #                 if not temp_data:
    #                     break
                    if receive.endswith("\n"):
                        break
                # default_socket.close()
                return receive
            else:
                return None
        else:
            print("you don't login.")
    except Exception as ex:
        print(ex)
        print("接收数据异常，请稍后再试。")
