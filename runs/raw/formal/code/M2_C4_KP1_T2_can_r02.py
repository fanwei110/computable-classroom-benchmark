import os
import numpy as np
import matplotlib.pyplot as plt

# ------------------------------
# 资产参数（小数表示）
# ------------------------------
r1 = 0.071                # 资产1期望年收益
r2 = 0.124                # 资产2期望年收益
sigma1 = 0.163            # 资产1年化波动率
sigma2 = 0.289            # 资产2年化波动率
var1 = sigma1 ** 2
var2 = sigma2 ** 2
cov_scale = sigma1 * sigma2   # 乘积 σ1·σ2，用于计算协方差

# 目标期望收益（用于 ρ=0.45 时的前沿波动率计算）
target_return = 0.10

# 三种相关系数
rhos = [0.15, 0.45, 0.75]

# 扫描权重的范围（允许卖空），覆盖足够宽的 w1 以展示前沿形状
w1_range = np.linspace(-0.8, 1.8, 2000)
w2_range = 1.0 - w1_range

# ------------------------------
# 解析函数：给定相关系数，计算满仓下的最小方差组合权重与波动率
# ------------------------------
def minimum_variance_portfolio(rho):
    """返回 (w1_mvp, sigma_mvp) 均为小数"""
    cov = rho * cov_scale
    denom = var1 + var2 - 2 * cov
    # 全局最小方差组合权重（允许卖空）
    w1_opt = (var2 - cov) / denom
    w2_opt = 1.0 - w1_opt
    var_p = (w1_opt**2 * var1 + w2_opt**2 * var2 +
             2 * w1_opt * w2_opt * cov)
    sigma_p = np.sqrt(var_p)
    return w1_opt, sigma_p

# ------------------------------
# 绘图准备
# ------------------------------
fig, ax = plt.subplots(figsize=(8, 6))
colors = ['#1f77b4', '#ff7f0e', '#2ca02c']  # 三条曲线的颜色

result = {}  # 用于存放最终输出

# 分别处理每个相关系数
for rho, color in zip(rhos, colors):
    # 协方差
    cov_12 = rho * cov_scale
    # 扫描组合的波动率和期望收益
    portfolio_var = (w1_range**2 * var1 +
                     w2_range**2 * var2 +
                     2 * w1_range * w2_range * cov_12)
    portfolio_sigma = np.sqrt(portfolio_var)
    portfolio_return = w1_range * r1 + w2_range * r2

    # 绘制前沿曲线（按波动率排序以保证曲线连续）
    sort_idx = np.argsort(portfolio_sigma)
    ax.plot(portfolio_sigma[sort_idx], portfolio_return[sort_idx],
            color=color, linewidth=2, label=f'ρ = {rho}')

    # 计算并标记最小方差组合
    w1_mvp, sigma_mvp = minimum_variance_portfolio(rho)
    w2_mvp = 1.0 - w1_mvp
    return_mvp = w1_mvp * r1 + w2_mvp * r2
    ax.scatter(sigma_mvp, return_mvp, color=color, edgecolors='black',
               s=80, zorder=5, marker='D',
               label=f'MVP ρ={rho} (σ={sigma_mvp:.4f})')

    # 若为 ρ=0.45，保存所需计算结果
    if rho == 0.45:
        result['mvp_vol_at_rho45'] = float(sigma_mvp)

        # 计算目标收益 10% 对应的组合权重（满仓约束）
        w1_target = (target_return - r2) / (r1 - r2)
        w2_target = 1.0 - w1_target
        var_target = (w1_target**2 * var1 + w2_target**2 * var2 +
                      2 * w1_target * w2_target * (0.45 * cov_scale))
        sigma_target = np.sqrt(var_target)
        result['frontier_vol_at_target'] = float(sigma_target)

        # 在图上标出该目标收益点（可选，便于观察）
        ax.scatter(sigma_target, target_return, color=color, edgecolors='black',
                   s=80, zorder=5, marker='s',
                   label=f'Target 10% ρ=0.45 (σ={sigma_target:.4f})')

# ------------------------------
# 图形修饰
# ------------------------------
ax.set_xlabel('Portfolio Volatility (σ)', fontsize=12)
ax.set_ylabel('Expected Return (μ)', fontsize=12)
ax.set_title('Mean-Variance Frontiers for Different Correlation Coefficients',
             fontsize=14)
ax.legend(loc='best', fontsize=9)
ax.grid(True, alpha=0.3)

# 保存图形
figure_name = 'mean_variance_frontier.png'
figure_path = os.path.abspath(figure_name)
fig.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close(fig)

result['figure_path'] = figure_path

# ------------------------------
# 输出结果（供检查）
# ------------------------------
print("Calculation results:")
print(f"  MVP annualized volatility (ρ=0.45): {result['mvp_vol_at_rho45']:.6f}")
print(f"  Minimum vol for target return 10% (ρ=0.45): {result['frontier_vol_at_target']:.6f}")
print(f"  Figure saved at: {result['figure_path']}")

# 最终结果字典 result 已包含所有要求内容
