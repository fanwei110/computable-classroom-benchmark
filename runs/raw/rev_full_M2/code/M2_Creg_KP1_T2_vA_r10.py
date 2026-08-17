import numpy as np
from scipy.optimize import minimize
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

# =========================
# 参数设定
# =========================
mu1 = 0.071
mu2 = 0.124
sigma1 = 0.163
sigma2 = 0.289
mu_target = 0.10

rhos = [0.15, 0.45, 0.75]

# 生成组合权重用于绘制前沿（卖空、满仓）
w_range = np.linspace(-3.0, 4.0, 1000)  # 足够宽的权重范围

# 存储结果
frontier_data = {}

# =========================
# 计算前沿与最小方差组合
# =========================
plt.figure(figsize=(10, 7))

for rho in rhos:
    cov = rho * sigma1 * sigma2
    # 组合期望收益与方差
    portfolio_returns = w_range * mu1 + (1 - w_range) * mu2
    portfolio_variances = (w_range**2 * sigma1**2
                           + (1 - w_range)**2 * sigma2**2
                           + 2 * w_range * (1 - w_range) * cov)
    portfolio_volatilities = np.sqrt(portfolio_variances)

    # 最小方差组合（解析解）
    w_mvp = (sigma2**2 - cov) / (sigma1**2 + sigma2**2 - 2 * cov)
    mu_mvp = w_mvp * mu1 + (1 - w_mvp) * mu2
    var_mvp = (w_mvp**2 * sigma1**2
               + (1 - w_mvp)**2 * sigma2**2
               + 2 * w_mvp * (1 - w_mvp) * cov)
    sigma_mvp = np.sqrt(var_mvp)

    # 绘制前沿
    plt.plot(portfolio_volatilities * 100, portfolio_returns * 100,
             label=f'ρ = {rho}')
    # 标出最小方差组合
    plt.scatter(sigma_mvp * 100, mu_mvp * 100,
                marker='o', s=60, zorder=5,
                label=f'MVP ρ={rho}' if rho == rhos[0] else "")

    # 保存数据以备后续使用
    frontier_data[rho] = {
        'weights': w_range,
        'returns': portfolio_returns,
        'volatilities': portfolio_volatilities,
        'mvp_w': w_mvp,
        'mvp_mu': mu_mvp,
        'mvp_sigma': sigma_mvp
    }

# =========================
# 特殊要求：ρ = 0.45
# =========================
rho_special = 0.45
data_special = frontier_data[rho_special]

# 最小方差组合年化波动率
mvp_vol_at_rho45 = data_special['mvp_sigma']

# 目标收益 10% 下的组合（唯一权重）
w_target = (mu_target - mu2) / (mu1 - mu2)
cov_special = rho_special * sigma1 * sigma2
var_target = (w_target**2 * sigma1**2
              + (1 - w_target)**2 * sigma2**2
              + 2 * w_target * (1 - w_target) * cov_special)
frontier_vol_at_target = np.sqrt(var_target)

# =========================
# 绘图美化
# =========================
plt.xlabel('年化波动率 (%)')
plt.ylabel('期望年收益 (%)')
plt.title('两只风险资产的均值-方差前沿')
plt.legend(loc='upper left')
plt.grid(True, alpha=0.3)

# 坐标轴格式化为百分比
ax = plt.gca()
ax.xaxis.set_major_formatter(PercentFormatter())
ax.yaxis.set_major_formatter(PercentFormatter())

plt.tight_layout()

# 保存图像
figure_path = 'mean_variance_frontier.png'
plt.savefig(figure_path, dpi=150)
plt.close()

# =========================
# 汇总结果
# =========================
result = {
    'mvp_vol_at_rho45': mvp_vol_at_rho45,
    'frontier_vol_at_target': frontier_vol_at_target,
    'figure_path': figure_path
}

# 打印结果以符合自包含可复现要求
print("计算结果：")
print(f"相关系数0.45时最小方差组合年化波动率: {mvp_vol_at_rho45:.4f} ({mvp_vol_at_rho45*100:.2f}%)")
print(f"目标收益10%时最小年化波动率（ρ=0.45）: {frontier_vol_at_target:.4f} ({frontier_vol_at_target*100:.2f}%)")
print(f"图像已保存至: {figure_path}")
print("\n字典 result =", result)
