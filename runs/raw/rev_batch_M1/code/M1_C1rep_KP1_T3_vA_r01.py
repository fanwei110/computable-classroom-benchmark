import math

# 给定参数
sigma_A = 0.184
sigma_B = 0.297
w_A = 0.6
w_B = 0.4
rho_before = 0.3
rho_after = 0.8

# 计算前后的组合波动率
vol_before = math.sqrt(w_A**2 * sigma_A**2 + w_B**2 * sigma_B**2 + 2 * w_A * w_B * sigma_A * sigma_B * rho_before)
vol_after = math.sqrt(w_A**2 * sigma_A**2 + w_B**2 * sigma_B**2 + 2 * w_A * w_B * sigma_A * sigma_B * rho_after)

# 存入结果字典
result = {
    'vol_before_annual': vol_before,
    'vol_after_annual': vol_after
}

result
