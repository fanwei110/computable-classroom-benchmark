import numpy as np

# 给定的参数
w_A = 0.6         # 资产 A 的权重
w_B = 0.4         # 资产 B 的权重
vol_A = 0.184     # 资产 A 的年化波动率 18.4%
vol_B = 0.297     # 资产 B 的年化波动率 29.7%
rho_before = 0.3  # 变化前的相关系数
rho_after = 0.8   # 变化后的相关系数

# 投资组合方差公式: Var_p = w_A^2 * vol_A^2 + w_B^2 * vol_B^2 + 2 * w_A * w_B * vol_A * vol_B * rho
var_before = (w_A**2 * vol_A**2) + (w_B**2 * vol_B**2) + (2 * w_A * w_B * vol_A * vol_B * rho_before)
var_after = (w_A**2 * vol_A**2) + (w_B**2 * vol_B**2) + (2 * w_A * w_B * vol_A * vol_B * rho_after)

# 计算年化波动率 (标准差)
vol_before_annual = np.sqrt(var_before)
vol_after_annual = np.sqrt(var_after)

# 按照输出契约存入字典
result = {
    'vol_before_annual': vol_before_annual,
    'vol_after_annual': vol_after_annual
}
