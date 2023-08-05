import baostock as bs

# 登陆系统
lg = bs.login(user_id="anonymous", password="123456")
# 显示登陆返回信息
print(lg.error_code)
print(lg.error_msg)
rs = bs.query_history_k_data("sh.601398",
                             "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus",
                             start_date='2017-01-01', end_date='2017-01-31', frequency="d", adjustflag="3")
# 获取具体的信息
data = rs.get_data()
while (rs.error_code == '0') & rs.next():
    # 分页查询，将每页信息合并在一起
    data.append(rs.get_data())

# 显示查询数据
print(data)
# 登出系统
bs.logout()
