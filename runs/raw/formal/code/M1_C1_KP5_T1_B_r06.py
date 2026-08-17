import math

position = 185  # 仓位（万元）
annual_vol = 0.218  # 年化波动率
z_95 = 1.645  # 95%置信水平对应的z值
z_99 = 2.326  # 99%置信水平对应的z值

# 95%置信水平下的1天VaR
var_95_1d = position * z_95 * annual_vol * math.sqrt(1/252)

# 99%置信水平下的10天VaR
var_99_10d = position * z_99 * annual_vol * math.sqrt(10/252)

result = {
    'var_95_1d': round(var_95_1d, 4),  # 保留4位小数
    'var_99_10d': round(var_99_10d, 4)
}

print(result)
