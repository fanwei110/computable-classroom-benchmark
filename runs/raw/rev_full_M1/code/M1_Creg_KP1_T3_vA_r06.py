import numpy as np

def calculate_portfolio_volatility(vol_a, vol_b, weight_a, weight_b, corr):
    """
    计算资产组合的波动率
    :param vol_a: 资产A的年化波动率
    :param vol_b: 资产B的年化波动率
    :param weight_a: 资产A的权重
    :param weight_b: 资产B的权重
    :param corr: 资产A和B的相关系数
    :return: 组合的年化波动率
    """
    cov = corr * vol_a * vol_b
    portfolio_var = (weight_a ** 2) * (vol_a ** 2) + (weight_b ** 2) * (vol_b ** 2) + 2 * weight_a * weight_b * cov
    portfolio_vol = np.sqrt(portfolio_var)
    return portfolio_vol

# 输入参数
vol_a_annual = 0.184  # 资产A的年化波动率
vol_b_annual = 0.297  # 资产B的年化波动率
weight_a = 0.6        # 资产A的权重
weight_b = 0.4        # 资产B的权重
corr_before = 0.3     # 变化前的相关系数
corr_after = 0.8      # 变化后的相关系数

# 计算变化前后的组合波动率
vol_before_annual = calculate_portfolio_volatility(vol_a_annual, vol_b_annual, weight_a, weight_b, corr_before)
vol_after_annual = calculate_portfolio_volatility(vol_a_annual, vol_b_annual, weight_a, weight_b, corr_after)

# 存储结果
result = {
    'vol_before_annual': vol_before_annual,
    'vol_after_annual': vol_after_annual
}

# 输出结果（可选，用于验证）
print(result)
