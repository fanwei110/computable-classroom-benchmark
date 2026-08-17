import numpy as np

# 给定的资产参数
sigma_A = 0.184  # 资产 A 的年化波动率
sigma_B = 0.297  # 资产 B 的年化波动率
w_A = 0.6        # 资产 A 的权重
w_B = 0.4        # 资产 B 的权重

# 相关系数变化
rho_before = 0.3
rho_after = 0.8

# 计算组合方差的各部分
# 组合方差公式: sigma_p^2 = w_A^2 * sigma_A^2 + w_B^2 * sigma_B^2 + 2 * w_A * w_B * sigma_A * sigma_B * rho
var_independent = (w_A ** 2) * (sigma_A ** 2) + (w_B ** 2) * (sigma_B ** 2)
cross_term_coeff = 2 * w_A * w_B * sigma_A * sigma_B

# 计算相关系数变化前的组合方差与波动率
var_before = var_independent + cross_term_coeff * rho_before
vol_before_annual = np.sqrt(var_before)

# 计算相关系数变化后的组合方差与波动率
var_after = var_independent + cross_term_coeff * rho_after
vol_after_annual = np.sqrt(var_after)

# 将结果存入指定格式的字典
result = {
    'vol_before_annual': vol_before_annual,
    'vol_after_annual': vol_after_annual
}
