import baostock as bs
import pandas as pd

# 登陆系统
lg = bs.login(user_id="anonymous", password="123456")
# 显示登陆返回信息
print(lg.error_code)
print(lg.error_msg)
# 详细指标参数，参见“历史行情指标参数”章节
rs = bs.query_history_k_data("sh.601398",
    "date,code,open,high,low,close,volume,amount,adjustflag",
    start_date='2017-01-01', end_date='2017-01-31', 
    frequency="d", adjustflag="3")
print(rs.error_code)
print(rs.error_msg)
# 获取具体的信息
result = pd.DataFrame(columns=["date","code","open","high","low","close","volume","amount","adjustflag"])
while (rs.error_code == '0') & rs.next():
    # 分页查询，将每页信息合并在一起
    result = result.append(rs.get_row_data(), ignore_index=True)
result.to_csv("D:\\history_k_data.csv", index=False)
print(result)
# 登出系统
bs.logout()
