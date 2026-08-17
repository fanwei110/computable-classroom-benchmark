import numpy as np
import matplotlib.pyplot as plt
import os

# 资产参数
mu = np.array([0.071, 0.124])  # 期望收益
sigma = np.array([0.163, 0.289])  # 波动率

# 相关系数
rhos = [0.15, 0.45, 0.75]

# 计算协方差矩阵
def get_cov_matrix(rho):
    cov = np.array([
        [sigma[0]**2, rho * sigma[0] * sigma[1]],
        [rho * sigma[0] * sigma[1], sigma[1]**2]
    ])
    return cov

# 计算最小方差组合
def calculate_mvp(cov):
    ones = np.ones(2)
    cov_inv = np.linalg.inv(cov)
    w = cov_inv @ ones / (ones @ cov_inv @ ones)
    mvp_vol = np.sqrt(w @ cov @ w)
    mvp_ret = w @ mu
    return w, mvp_ret, mvp_vol

# 计算有效前沿
def calculate_frontier(cov, target_returns=None):
    if target_returns is None:
        target_returns = np.linspace(mu.min(), mu.max(), 100)

    frontiers = []
    for r in target_returns:
        A = np.array([[mu @ np.linalg.inv(cov) @ mu, mu @ np.linalg.inv(cov) @ np.ones(2)],
                      [mu @ np.linalg.inv(cov) @ np.ones(2), np.ones(2) @ np.linalg.inv(cov) @ np.ones(2)]])
        b = np.array([r, 1])
        try:
            lambdas = np.linalg.solve(A, b)
            w = lambdas[0] * np.linalg.inv(cov) @ mu + lambdas[1] * np.linalg.inv(cov) @ np.ones(2)
            vol = np.sqrt(w @ cov @ w)
            frontiers.append((vol, r))
        except np.linalg.LinAlgError:
            continue

    frontiers = np.array(frontiers)
    return frontiers

# 绘图
plt.figure(figsize=(10, 6))

result = {}

for rho in rhos:
    cov = get_cov_matrix(rho)
    w_mvp, ret_mvp, vol_mvp = calculate_mvp(cov)
    frontier = calculate_frontier(cov)

    # 保存ρ=0.45时的最小方差组合波动率
    if rho == 0.45:
        result['mvp_vol_at_rho45'] = float(vol_mvp)

    # 绘制前沿
    plt.plot(frontier[:, 0], frontier[:, 1], label=f'ρ={rho}')
    plt.scatter(vol_mvp, ret_mvp, color='red', zorder=5)
    plt.text(vol_mvp, ret_mvp, f'MVP (ρ={rho})', fontsize=9, verticalalignment='bottom')

    # 计算目标收益10%时的最小波动率
    if rho == 0.45:
        target_return = 0.10
        # 找到最接近10%的点
        idx = np.argmin(np.abs(frontier[:, 1] - target_return))
        closest_return = frontier[idx, 1]
        if abs(closest_return - target_return) < 0.001:  # 允许一定误差
            result['frontier_vol_at_target'] = float(frontier[idx, 0])

# 图形设置
plt.title('Efficient Frontier with Different Correlations')
plt.xlabel('Volatility (σ)')
plt.ylabel('Expected Return (μ)')
plt.legend()
plt.grid(True)

# 保存图形
figure_path = 'efficient_frontier.png'
plt.savefig(figure_path)
plt.close()

result['figure_path'] = os.path.abspath(figure_path)

# 输出结果
print(result)
