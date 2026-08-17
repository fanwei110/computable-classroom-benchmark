import numpy as np
from scipy.optimize import minimize

# 1. 构造协方差矩阵
vols = np.array([0.187, 0.243, 0.312])  # 年化波动率
corr = np.array([
    [1.00, 0.21, -0.13],
    [0.21, 1.00,  0.37],
    [-0.13, 0.37, 1.00]
])

# 协方差矩阵 Σ = diag(vol) @ corr @ diag(vol)
cov_matrix = np.diag(vols) @ corr @ np.diag(vols)

# 2. 求最小方差组合权重（允许卖空，满仓约束）
n_assets = len(vols)
ones = np.ones(n_assets)

# 目标函数：w'Σw
def portfolio_variance(w):
    return w.T @ cov_matrix @ w

# 约束：w.sum() = 1
constraints = ({'type': 'eq', 'fun': lambda w: w.sum() - 1})

# 初始猜测：等权重
w0 = np.ones(n_assets) / n_assets

# 优化
res = minimize(portfolio_variance, w0, constraints=constraints)
mvp_weights = res.x

# 3. 组合波动率
mvp_vol_annual = np.sqrt(portfolio_variance(mvp_weights))

# 4. 填充结果字典
result = {
    'mvp_weights': mvp_weights.tolist(),
    'mvp_vol_annual': float(mvp_vol_annual)
}

print(result)
