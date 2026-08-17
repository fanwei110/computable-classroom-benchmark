import numpy as np
import pandas as pd
from scipy.optimize import minimize

# 输入参数：波动率（年化，小数形式）
vols = np.array([0.187, 0.243, 0.312])

# 相关系数矩阵
corr_matrix = np.array([
    [1.0,  0.21, -0.13],
    [0.21, 1.0,   0.37],
    [-0.13, 0.37,  1.0]
])

# 构建协方差矩阵 Sigma = diag(vols) * corr * diag(vols)
D = np.diag(vols)
cov_matrix = D @ corr_matrix @ D

# 全局最小方差组合：在满仓(A)且允许卖空下，最小化 w' Σ w
# 约束: sum(w) = 1
n_assets = 3
initial_guess = np.ones(n_assets) / n_assets

# 目标函数: 组合方差
def portfolio_var(weights):
    return weights @ cov_matrix @ weights

constraints = ({'type': 'eq', 'fun': lambda w: np.sum(w) - 1.0})
# 无边界限制 => 允许卖空
bounds = None

result_opt = minimize(portfolio_var, initial_guess, method='SLSQP',
                      bounds=bounds, constraints=constraints)

mvp_weights = result_opt.x
mvp_var = result_opt.fun
mvp_vol_annual = np.sqrt(mvp_var)  # 年化波动率

# 以小数形式输出，权重保留足够精度
result = {
    'mvp_weights': mvp_weights,
    'mvp_vol_annual': mvp_vol_annual
}

# 打印清晰结果供课堂展示
print("=== 全局最小方差组合 (MVP) ===")
print(f"资产1权重: {mvp_weights[0]:.6f}")
print(f"资产2权重: {mvp_weights[1]:.6f}")
print(f"资产3权重: {mvp_weights[2]:.6f}")
print(f"权重和: {np.sum(mvp_weights):.8f}")
print(f"年化波动率: {mvp_vol_annual:.6f} ({mvp_vol_annual*100:.2f}%)")
print(f"\n字典 result = {result}")
