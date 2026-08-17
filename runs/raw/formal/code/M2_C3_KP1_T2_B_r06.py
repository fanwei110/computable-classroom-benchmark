import numpy as np
import matplotlib.pyplot as plt
import os

# 资产参数
r1, r2 = 0.071, 0.124
sigma1, sigma2 = 0.163, 0.289
rhos = [0.15, 0.45, 0.75]

# 生成组合权重（资产1的权重）
w_range = np.linspace(-0.5, 1.5, 1000)  # 包含一些杠杆/卖空，以便完整展示前沿

# 绘图
plt.figure(figsize=(10, 6))
colors = ['blue', 'green', 'red']
min_var_points = {}  # 存储最小方差点 (sigma, ret, corr)

for rho, color in zip(rhos, colors):
    cov = rho * sigma1 * sigma2
    # 组合方差和收益
    portfolio_sigma = np.sqrt(w_range**2 * sigma1**2 + (1 - w_range)**2 * sigma2**2 +
                              2 * w_range * (1 - w_range) * cov)
    portfolio_ret = w_range * r1 + (1 - w_range) * r2
    
    # 最小方差组合权重、收益、风险
    w_min = (sigma2**2 - cov) / (sigma1**2 + sigma2**2 - 2 * cov)
    ret_min = w_min * r1 + (1 - w_min) * r2
    sigma_min = np.sqrt(w_min**2 * sigma1**2 + (1 - w_min)**2 * sigma2**2 +
                        2 * w_min * (1 - w_min) * cov)
    min_var_points[rho] = (sigma_min, ret_min)
    
    # 绘制前沿
    plt.plot(portfolio_sigma, portfolio_ret, color=color, label=f'ρ = {rho}')
    # 标出最小方差点
    plt.scatter(sigma_min, ret_min, color=color, marker='*', s=150, edgecolor='black', zorder=5)

# 计算 rho=0.45 时的特定指标
rho45 = 0.45
cov45 = rho45 * sigma1 * sigma2
w_min_45 = (sigma2**2 - cov45) / (sigma1**2 + sigma2**2 - 2 * cov45)
sigma_min_45 = np.sqrt(w_min_45**2 * sigma1**2 + (1 - w_min_45)**2 * sigma2**2 +
                       2 * w_min_45 * (1 - w_min_45) * cov45)

# 目标收益 10% 对应的波动率（唯一组合）
target_ret = 0.10
w_target = (target_ret - r2) / (r1 - r2)
sigma_target = np.sqrt(w_target**2 * sigma1**2 + (1 - w_target)**2 * sigma2**2 +
                       2 * w_target * (1 - w_target) * cov45)

# 图中标出目标收益点
plt.scatter(sigma_target, target_ret, color='black', marker='X', s=150, zorder=6, label=f'Target {target_ret:.0%}')
plt.axhline(y=target_ret, color='gray', linestyle='--', linewidth=0.8)

plt.xlabel('Volatility (σ)')
plt.ylabel('Expected Return')
plt.title('Two-Asset Efficient Frontiers')
plt.legend()
plt.grid(True)

# 保存图片
fig_path = 'effective_frontier.png'
plt.savefig(fig_path, dpi=200, bbox_inches='tight')
plt.close()

# 构造结果字典
result = {
    'mvp_vol_at_rho45': float(sigma_min_45),
    'frontier_vol_at_target': float(sigma_target),
    'figure_path': os.path.abspath(fig_path)
}

# 输出结果
print(result)
# {'mvp_vol_at_rho45': 0.16167..., 'frontier_vol_at_target': 0.20238..., 'figure_path': '/.../effective_frontier.png'}
