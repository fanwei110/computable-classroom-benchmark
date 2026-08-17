import numpy as np
from scipy.optimize import minimize

# 输入数据
vol = np.array([0.187, 0.243, 0.312])
corr = np.array([
    [1.0, 0.21, -0.13],
    [0.21, 1.0, 0.37],
    [-0.13, 0.37, 1.0]
])

# 1. 构造协方差矩阵
# 协方差公式: cov(i,j) = corr(i,j) * vol(i) * vol(j)
cov_matrix = np.outer(vol, vol) * corr

# 2. 求最小方差权重（允许做空，权重和为1）
# 对于允许做空、权重和为1的最小方差组合，有闭式解：
# w = (Σ^{-1} * 1) / (1' * Σ^{-1} * 1)
n_assets = len(vol)
ones = np.ones(n_assets)
inv_cov = np.linalg.inv(cov_matrix)

w_mvp = inv_cov @ ones / (ones @ inv_cov @ ones)

# 确保权重精确求和为1
w_mvp = w_mvp / np.sum(w_mvp)

# 3. 计算组合波动率
# 组合方差 = w' Σ w
portfolio_variance = w_mvp.T @ cov_matrix @ w_mvp
# 年化波动率（输入数据已经是年化的，所以结果也是年化的）
portfolio_vol = np.sqrt(portfolio_variance)

# 4. 输出结果
result = {
    'mvp_weights': w_mvp.tolist(),
    'mvp_vol_annual': float(portfolio_vol)
}

# 打印结果供课堂展示
print("最小方差组合结果：")
print("-" * 40)
for i, w in enumerate(w_mvp):
    print(f"资产{i+1}权重: {w:.4f} ({w*100:.2f}%)")
print(f"\n组合权重之和: {np.sum(w_mvp):.6f}")
print(f"\n组合年化波动率: {portfolio_vol:.4f} ({portfolio_vol*100:.2f}%)")
print("\n协方差矩阵:")
print(cov_matrix)
print("\nresult字典:")
print(result)
