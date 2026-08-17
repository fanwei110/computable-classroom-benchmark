import numpy as np
import matplotlib.pyplot as plt

# ==================== 参数设定 ====================
mu = np.array([0.071, 0.124])         # 期望年收益
sigma = np.array([0.163, 0.289])      # 年化波动率
rho_list = [0.15, 0.45, 0.75]        # 相关系数列表

# 结果字典初始化
result = {
    'mvp_vol_at_rho45': None,
    'frontier_vol_at_target': None,
    'figure_path': 'mean_variance_frontier.png'
}

# ==================== 核心计算函数 ====================
def calc_portfolio_stats(w, mu, cov):
    """计算组合的期望收益和波动率"""
    port_mu = np.dot(w, mu)
    port_sigma = np.sqrt(np.dot(w, np.dot(cov, w)))
    return port_mu, port_sigma

# ==================== 计算特定指标 ====================
# 针对相关系数 0.45 构造协方差矩阵
rho45 = 0.45
cov45 = np.array([[sigma[0]**2, rho45 * sigma[0] * sigma[1]],
                  [rho45 * sigma[0] * sigma[1], sigma[1]**2]])

ones = np.ones(2)
inv_cov45 = np.linalg.inv(cov45)

# 1. 计算最小方差组合 (MVP)
# 公式: w_mvp = (Σ^-1 * 1) / (1^T * Σ^-1 * 1)
w_mvp45 = (inv_cov45 @ ones) / (ones @ inv_cov45 @ ones)
mvp_mu45, mvp_vol45 = calc_portfolio_stats(w_mvp45, mu, cov45)
result['mvp_vol_at_rho45'] = float(mvp_vol45)

# 2. 计算目标期望收益 10% 下的最小波动率
mu_target = 0.10
# 两资产满仓约束下: w1 + w2 = 1, w1*mu1 + w2*mu2 = mu_target
w1_target = (mu_target - mu[1]) / (mu[0] - mu[1])
w_target = np.array([w1_target, 1 - w1_target])
target_mu, target_vol = calc_portfolio_stats(w_target, mu, cov45)
result['frontier_vol_at_target'] = float(target_vol)

# ==================== 绘制均值-方差前沿 ====================
fig, ax = plt.subplots(figsize=(10, 7))

# 扫描权重范围（允许卖空，故包含负值及大于1的值）
w_range = np.linspace(-1.0, 2.0, 1000)

for rho in rho_list:
    # 构造当前相关系数下的协方差矩阵
    cov = np.array([[sigma[0]**2, rho * sigma[0] * sigma[1]],
                    [rho * sigma[0] * sigma[1], sigma[1]**2]])
    
    port_mus = []
    port_sigmas = []
    
    # 在组合权重上扫描画出前沿
    for w1 in w_range:
        w = np.array([w1, 1 - w1])
        port_mu, port_sigma = calc_portfolio_stats(w, mu, cov)
        port_mus.append(port_mu)
        port_sigmas.append(port_sigma)
        
    port_mus = np.array(port_mus)
    port_sigmas = np.array(port_sigmas)
    
    # 按收益率排序，避免画线时出现折返
    sorted_idx = np.argsort(port_mus)
    port_mus_sorted = port_mus[sorted_idx]
    port_sigmas_sorted = port_sigmas[sorted_idx]
    
    # 绘制前沿曲线
    ax.plot(port_sigmas_sorted, port_mus_sorted, label=f'$\\rho = {rho:.2f}$')
    
    # 计算并标出当前相关系数的最小方差组合 (MVP)
    inv_cov = np.linalg.inv(cov)
    w_mvp = (inv_cov @ ones) / (ones @ inv_cov @ ones)
    mu_mvp, sigma_mvp = calc_portfolio_stats(w_mvp, mu, cov)
    
    ax.scatter(sigma_mvp, mu_mvp, marker='o', s=50, zorder=5)
    ax.annotate(f'MVP ($\\rho={rho:.2f}$)\n$\sigma={sigma_mvp:.2%}$', 
                (sigma_mvp, mu_mvp), 
                textcoords="offset points", xytext=(10, 5), ha='left', fontsize=9)

# ==================== 图形格式设定与保存 ====================
ax.set_xlabel('Volatility (Annualized)', fontsize=12)
ax.set_ylabel('Expected Return (Annualized)', fontsize=12)
ax.set_title('Mean-Variance Frontiers for Two Risky Assets', fontsize=14)
ax.legend(fontsize=11)
ax.grid(True, linestyle='--', alpha=0.7)

# 保存图形
plt.savefig(result['figure_path'], dpi=300, bbox_inches='tight')
plt.close()

# ==================== 输出结果 ====================
print("Result dictionary:")
for k, v in result.items():
    print(f"{k}: {v}")
