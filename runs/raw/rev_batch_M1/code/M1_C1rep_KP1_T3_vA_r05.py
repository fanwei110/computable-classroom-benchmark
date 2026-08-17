import math

# 输入参数
sigma_A = 0.184
sigma_B = 0.297
w_A = 0.6
w_B = 0.4
rho_before = 0.3
rho_after = 0.8

# 计算变化前的波动率
vol_before = math.sqrt(w_A**2 * sigma_A**2 + w_B**2 * sigma_B**2 + 2 * w_A * w_B * sigma_A * sigma_B * rho_before)
vol_before_annual = vol_before  # 题目中给出的波动率已是年化值

# 计算变化后的波动率
vol_after = math.sqrt(w_A**2 * sigma_A**2 + w_B**2 * sigma_B**2 + 2 * w_A * w_B * sigma_A * sigma_B * rho_after)
vol_after_annual = vol_after  # 题目中给出的波动率已是年化值

# 存入结果字典
result = {
    'vol_before_annual': round(vol_before_annual * 100, 4),  # 转换为百分比并保留4位小数
    'vol_after_annual': round(vol_after_annual * 100, 4)
}
