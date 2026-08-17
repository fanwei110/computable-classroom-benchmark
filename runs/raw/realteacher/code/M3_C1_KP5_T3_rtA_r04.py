import math

position = 2700000
annual_vol = 0.24

# 将年化波动率转换为日波动率 (假设一年256个交易日，sqrt(256)=16)
daily_vol = annual_vol / 16

# 95% 置信水平对应的Z分数
z_95 = 1.645

# 计算 95% 一日 VaR
var_95_1d = position * daily_vol * z_95

result = {
    'var_95_1d': var_95_1d
}
