import numpy as np

# 参数
w_A = 0.6
w_B = 0.4
sigma_A = 0.184
sigma_B = 0.297
rho_before = 0.3
rho_after = 0.8

# 变化前的组合波动率
vol_before = np.sqrt(w_A**2 * sigma_A**2 + w_B**2 * sigma_B**2 + 2 * w_A * w_B * sigma_A * sigma_B * rho_before)
vol_before_annual = vol_before  # 已经是年化波动率

# 变化后的组合波动率
vol_after = np.sqrt(w_A**2 * sigma_A**2 + w_B**2 * sigma_B**2 + 2 * w_A * w_B * sigma_A * sigma_B * rho_after)
vol_after_annual = vol_after  # 已经是年化波动率

# 存入结果字典
result = {
    'vol_before_annual': vol_before_annual,
    'vol_after_annual': vol_after_annual
}

result
