import numpy as np
import matplotlib.pyplot as plt
import os

# 资产参数
mu = np.array([7.1, 12.4])  # 收益率
vol = np.array([16.3, 28.9])  # 波动率
corr_list = [0.15, 0.45, 0.75]  # 相关系数列表

# 计算协方差矩阵
def get_cov_matrix(vol1, vol2, rho):
    cov = rho * vol1 * vol2
    return np.array([[vol1**2, cov], [cov, vol2**2]])

# 计算最小方差组合
def calculate_mvp(mu, cov):
    ones = np.ones(2)
    cov_inv = np.linalg.inv(cov)
    w = cov_inv @ ones / (ones.T @ cov_inv @ ones)
    mvp_vol = np.sqrt(w.T @ cov @ w)
    mvp_ret = w @ mu
    return w, mvp_ret, mvp_vol

# 计算有效前沿
def calculate_frontier(mu, cov):
    ones = np.ones(2)
    cov_inv = np.linalg.inv(cov)
    A = ones.T @ cov_inv @ ones
    B = ones.T @ cov_inv @ mu
    C = mu.T @ cov_inv @ mu
    D = A * C - B**2

    target_rets = np.linspace(min(mu), max(mu), 100)
    frontier_vols = []
    for ret in target_rets:
        w = (C - B * ret) * cov_inv @ ones / D + (A * ret - B) * cov_inv @ mu / D
        vol = np.sqrt(w.T @ cov @ w)
        frontier_vols.append(vol)
    return target_rets, frontier_vols

# 计算目标收益下的最小波动率
def calculate_vol_at_target(mu, cov, target_ret):
    ones = np.ones(2)
    cov_inv = np.linalg.inv(cov)
    A = ones.T @ cov_inv @ ones
    B = ones.T @ cov_inv @ mu
    C = mu.T @ cov_inv @ mu
    D = A * C - B**2

    w = (C - B * target_ret) * cov_inv @ ones / D + (A * target_ret - B) * cov_inv @ mu / D
    vol = np.sqrt(w.T @ cov @ w)
    return vol

# 主计算
result = {}
plt.figure(figsize=(10, 6))

for rho in corr_list:
    cov = get_cov_matrix(vol[0], vol[1], rho)
    target_rets, frontier_vols = calculate_frontier(mu, cov)
    w_mvp, mvp_ret, mvp_vol = calculate_mvp(mu, cov)

    # 绘制有效前沿
    plt.plot(frontier_vols, target_rets, label=f'ρ={rho}')

    # 标记最小方差点
    plt.scatter(mvp_vol, mvp_ret, color='red')
    plt.text(mvp_vol, mvp_ret, f'MVP (ρ={rho})', fontsize=9, verticalalignment='bottom')

    # 保存ρ=0.45时的MVP波动率
    if rho == 0.45:
        result['mvp_vol_at_rho45'] = round(mvp_vol, 2)

# 计算目标收益10%时的最小波动率
cov_45 = get_cov_matrix(vol[0], vol[1], 0.45)
result['frontier_vol_at_target'] = round(calculate_vol_at_target(mu, cov_45, 10), 2)

# 图形设置
plt.title('Efficient Frontier with Two Assets')
plt.xlabel('Portfolio Volatility (%)')
plt.ylabel('Portfolio Return (%)')
plt.legend()
plt.grid(True)

# 保存图形
figure_path = 'efficient_frontier.png'
plt.savefig(figure_path)
result['figure_path'] = os.path.abspath(figure_path)
plt.close()

print(result)
