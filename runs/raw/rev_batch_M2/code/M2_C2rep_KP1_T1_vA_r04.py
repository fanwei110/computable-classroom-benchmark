import numpy as np
from scipy.optimize import minimize  # 可用于替代方法，此处主要使用闭式解

# 1. 输入数据
volatility = np.array([0.187, 0.243, 0.312])
corr_matrix = np.array([
    [1.00,  0.21, -0.13],
    [0.21,  1.00,  0.37],
    [-0.13, 0.37,  1.00]
])

# 2. 构造协方差矩阵：cov[i,j] = corr[i,j] * sigma_i * sigma_j
cov_matrix = corr_matrix * volatility[:, np.newaxis] * volatility[np.newaxis, :]

# 3. 全局最小方差组合（允许卖空，满仓）
# 闭式解: w = (Σ^{-1} 1) / (1^T Σ^{-1} 1)
ones = np.ones(len(volatility))
inv_cov = np.linalg.inv(cov_matrix)
numerator = inv_cov @ ones          # Σ^{-1} 1
denominator = ones @ numerator      # 1^T Σ^{-1} 1
weights = numerator / denominator

# 4. 组合年化波动率
portfolio_var = weights @ cov_matrix @ weights
portfolio_vol = np.sqrt(portfolio_var)

# 5. 按要求存入 result 字典
result = {
    'mvp_weights': weights.tolist(),  # 转为列表以便展示
    'mvp_vol_annual': portfolio_vol.item()  # 得到原生Python float
}

# 打印结果以供课堂查看
if __name__ == "__main__":
    print("Global Minimum Variance Portfolio (allow short selling, fully invested)")
    print("Weights:", result['mvp_weights'])
    print(f"Annualized Volatility: {result['mvp_vol_annual']:.4f}")
