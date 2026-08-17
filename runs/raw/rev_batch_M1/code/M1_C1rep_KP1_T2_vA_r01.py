import numpy as np
import matplotlib.pyplot as plt
import os

# 资产参数
mu1, mu2 = 0.071, 0.124
vol1, vol2 = 0.163, 0.289

# 相关系数
rhos = [0.15, 0.45, 0.75]

# 计算最小方差组合
def calculate_mvp(rho):
    cov = rho * vol1 * vol2
    sigma = np.array([[vol1**2, cov], [cov, vol2**2]])
    ones = np.array([1, 1])
    sigma_inv = np.linalg.inv(sigma)
    w_mvp = ones @ sigma_inv / (ones @ sigma_inv @ ones)
    vol_mvp = np.sqrt(w_mvp @ sigma @ w_mvp)
    mu_mvp = w_mvp @ np.array([mu1, mu2])
    return w_mvp, mu_mvp, vol_mvp

# 计算给定收益下的最小波动率
def calculate_min_vol_for_target(rho, target_return):
    cov = rho * vol1 * vol2
    sigma = np.array([[vol1**2, cov], [cov, vol2**2]])
    mu = np.array([mu1, mu2])

    # 约束条件
    A = np.array([[1, 1], [mu1, mu2]])
    b = np.array([1, target_return])

    # 解方程
    A_inv = np.linalg.inv(A)
    w = A_inv @ b
    vol = np.sqrt(w @ sigma @ w)
    return vol

# 绘制有效前沿
plt.figure(figsize=(10, 6))

for rho in rhos:
    # 计算MVP
    w_mvp, mu_mvp, vol_mvp = calculate_mvp(rho)

    # 生成不同权重组合
    weights = np.linspace(0, 1, 100)
    portfolio_vols = []
    portfolio_returns = []

    for w in weights:
        portfolio_return = w * mu1 + (1 - w) * mu2
        portfolio_vol = np.sqrt(w**2 * vol1**2 + (1 - w)**2 * vol2**2 + 2 * w * (1 - w) * rho * vol1 * vol2)
        portfolio_vols.append(portfolio_vol)
        portfolio_returns.append(portfolio_return)

    # 绘制前沿
    plt.plot(portfolio_vols, portfolio_returns, label=f'ρ={rho}')

    # 标记MVP
    plt.scatter(vol_mvp, mu_mvp, color='red')
    plt.text(vol_mvp, mu_mvp, f'MVP (ρ={rho})', fontsize=9, verticalalignment='bottom')

# 添加标签和图例
plt.title('Efficient Frontier with Different Correlations')
plt.xlabel('Portfolio Volatility (Annualized)')
plt.ylabel('Portfolio Expected Return (Annualized)')
plt.legend()
plt.grid(True)

# 保存图片
figure_path = 'efficient_frontier.png'
plt.savefig(figure_path)
plt.close()

# 计算所需结果
mvp_vol_at_rho45 = calculate_mvp(0.45)[2]
frontier_vol_at_target = calculate_min_vol_for_target(0.45, 0.10)

# 创建结果字典
result = {
    'mvp_vol_at_rho45': mvp_vol_at_rho45,
    'frontier_vol_at_target': frontier_vol_at_target,
    'figure_path': os.path.abspath(figure_path)
}

print(result)
