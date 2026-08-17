import numpy as np

# 输入参数
vol_A_annual = 0.184  # 资产 A 的年化波动率
vol_B_annual = 0.297  # 资产 B 的年化波动率
weight_A = 0.6        # 资产 A 的权重
weight_B = 0.4        # 资产 B 的权重
corr_before = 0.3     # 变化前的相关系数
corr_after = 0.8      # 变化后的相关系数

# 计算组合波动率的函数
def calculate_portfolio_vol(vol_A, vol_B, weight_A, weight_B, corr):
    cov = corr * vol_A * vol_B
    var_A = vol_A ** 2
    var_B = vol_B ** 2
    portfolio_var = (weight_A ** 2) * var_A + (weight_B ** 2) * var_B + 2 * weight_A * weight_B * cov
    portfolio_vol = np.sqrt(portfolio_var)
    return portfolio_vol

# 计算变化前后的组合波动率
vol_before_annual = calculate_portfolio_vol(vol_A_annual, vol_B_annual, weight_A, weight_B, corr_before)
vol_after_annual = calculate_portfolio_vol(vol_A_annual, vol_B_annual, weight_A, weight_B, corr_after)

# 存储结果
result = {
    'vol_before_annual': vol_before_annual,
    'vol_after_annual': vol_after_annual
}

# 输出结果（可选，用于验证）
print(result)
