import numpy as np
import scipy  # 依据要求导入，虽然未直接使用
import pandas as pd
import matplotlib.pyplot as plt

# 给定参数
sigma_A = 0.184  # 资产A年化波动率
sigma_B = 0.297  # 资产B年化波动率
weight_A = 0.6   # A的权重
weight_B = 0.4   # B的权重

rho_before = 0.3  # 变化前的相关系数
rho_after = 0.8   # 变化后的相关系数

# 计算组合方差 (年化)
# Var(p) = w_A^2 * sigma_A^2 + w_B^2 * sigma_B^2 + 2 * w_A * w_B * rho * sigma_A * sigma_B
var_before = (weight_A**2 * sigma_A**2 +
              weight_B**2 * sigma_B**2 +
              2 * weight_A * weight_B * rho_before * sigma_A * sigma_B)

var_after = (weight_A**2 * sigma_A**2 +
             weight_B**2 * sigma_B**2 +
             2 * weight_A * weight_B * rho_after * sigma_A * sigma_B)

# 年化波动率 = 标准差
vol_before_annual = np.sqrt(var_before)
vol_after_annual = np.sqrt(var_after)

# 按要求存入字典
result = {
    'vol_before_annual': vol_before_annual,
    'vol_after_annual': vol_after_annual
}

# 打印结果以便查看
print(result)
