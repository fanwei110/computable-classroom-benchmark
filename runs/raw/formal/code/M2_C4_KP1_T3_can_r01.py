import numpy as np
import pandas as pd

# 资产年化波动率（小数形式）
vol_A = 0.184      # 年化波动率 18.4%
vol_B = 0.297      # 年化波动率 29.7%

# 组合权重（A 占 60%，B 占 40%）
w_A = 0.6
w_B = 0.4
weights = np.array([w_A, w_B])

# 资产的年化标准差（对角矩阵）
std_devs = np.diag([vol_A, vol_B])

# 相关性矩阵的构建函数
def build_cov_matrix(rho):
    """根据相关系数 rho 构建协方差矩阵"""
    corr_matrix = np.array([[1.0, rho],
                           [rho, 1.0]])
    cov_matrix = std_devs @ corr_matrix @ std_devs
    return cov_matrix

# 组合年化波动率计算函数
def portfolio_volatility(weights, cov_matrix):
    """计算组合权重为 weights，协方差矩阵为 cov_matrix 时的组合年化波动率"""
    var = weights.T @ cov_matrix @ weights
    return float(np.sqrt(var))

# 构建两种情景的协方差矩阵
cov_rho_03 = build_cov_matrix(0.3)   # 相关系数 0.3
cov_rho_08 = build_cov_matrix(0.8)   # 相关系数 0.8

# 计算两个情景下的组合波动率（小数形式）
vol_before_annual = portfolio_volatility(weights, cov_rho_03)
vol_after_annual  = portfolio_volatility(weights, cov_rho_08)

# 结果字典
result = {
    'vol_before_annual': vol_before_annual,
    'vol_after_annual':  vol_after_annual
}

# 打印结果以便验证
if __name__ == "__main__":
    print(f"相关系数 0.3 时组合年化波动率: {vol_before_annual:.6f}")
    print(f"相关系数 0.8 时组合年化波动率: {vol_after_annual:.6f}")
    print("结果字典:")
    print(result)
