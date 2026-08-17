import numpy as np
import pandas as pd
from scipy.optimize import minimize

# ===================== 输入数据 =====================
# 三只风险资产的年化波动率
vols = np.array([0.187, 0.243, 0.312])

# 相关系数矩阵
corr_matrix = np.array([
    [1.0,   0.21, -0.13],
    [0.21,  1.0,   0.37],
    [-0.13, 0.37,  1.0 ]
])

# ===================== 计算协方差矩阵 =====================
# 协方差 = 波动率_i * 波动率_j * 相关系数_ij
cov_matrix = np.outer(vols, vols) * corr_matrix

# ===================== 求解最小方差组合 =====================
# 目标函数：组合方差（最小化）
def portfolio_variance(weights):
    return weights @ cov_matrix @ weights

# 约束条件：满仓（权重之和为1）
constraints = ({'type': 'eq', 'fun': lambda w: np.sum(w) - 1.0})

# 初始猜测：等权重
n = len(vols)
initial_guess = np.ones(n) / n

# 优化求解（允许卖空，无边界限制）
result = minimize(portfolio_variance, initial_guess, 
                  constraints=constraints, method='SLSQP')

# ===================== 提取结果 =====================
mvp_weights = result.x
mvp_variance = result.fun
mvp_vol_annual = np.sqrt(mvp_variance)  # 年化波动率

# ===================== 输出结果 =====================
# 按要求存入字典
result_dict = {
    'mvp_weights': mvp_weights,
    'mvp_vol_annual': mvp_vol_annual
}

# 显示结果
print("=" * 60)
print("全局最小方差组合（Global Minimum Variance Portfolio）")
print("=" * 60)
print(f"资产1权重: {mvp_weights[0]:.6f} ({mvp_weights[0]*100:.2f}%)")
print(f"资产2权重: {mvp_weights[1]:.6f} ({mvp_weights[1]*100:.2f}%)")
print(f"资产3权重: {mvp_weights[2]:.6f} ({mvp_weights[2]*100:.2f}%)")
print(f"权重之和: {np.sum(mvp_weights):.6f}")
print(f"\n年化波动率: {mvp_vol_annual:.6f} ({mvp_vol_annual*100:.2f}%)")
print("\n验证：组合方差 = w'Σw")
print(f"组合方差: {mvp_variance:.8f}")
print("=" * 60)

# 最终结果字典
result = result_dict
