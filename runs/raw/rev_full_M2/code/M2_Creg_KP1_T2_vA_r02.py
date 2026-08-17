import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

# ============================
# 参数设置
# ============================
# 期望年收益
mu = np.array([0.071, 0.124])
# 年化波动率
sig = np.array([0.163, 0.289])
# 需要考察的相关系数列表
rhos = [0.15, 0.45, 0.75]
# 目标相关系数
rho_target = 0.45
# 目标期望收益
target_return = 0.10

# ============================
# 组合计算函数
# ============================
def portfolio_stats(w1, mu, sig, rho):
    """根据资产1权重w1（满仓则w2 = 1 - w1）计算组合收益与波动率"""
    w2 = 1.0 - w1
    rp = w1 * mu[0] + w2 * mu[1]
    var = (w1**2 * sig[0]**2 +
           w2**2 * sig[1]**2 +
           2 * w1 * w2 * rho * sig[0] * sig[1])
    vol = np.sqrt(var)
    return rp, vol

def compute_mvp(mu, sig, rho):
    """计算最小方差组合 (MVP) 的权重、收益与波动率"""
    s1, s2 = sig[0], sig[1]
    cov = rho * s1 * s2
    w1_mvp = (s2**2 - cov) / (s1**2 + s2**2 - 2 * cov)
    rp_mvp, vol_mvp = portfolio_stats(w1_mvp, mu, sig, rho)
    return w1_mvp, rp_mvp, vol_mvp

# ============================
# 所需输出量的计算
# ============================
# 相关系数0.45下的MVP年化波动率
_, _, mvp_vol_at_rho45 = compute_mvp(mu, sig, rho_target)

# 目标收益10%所对应的权重（满仓约束下唯一确定）
w1_target = (target_return - mu[1]) / (mu[0] - mu[1])
_, frontier_vol_at_target = portfolio_stats(w1_target, mu, sig, rho_target)

# ============================
# 绘制均值‑方差前沿
# ============================
# 生成足够宽的权重范围，以展示允许卖空时的完整前沿
w1_range = np.linspace(-2.0, 3.0, 800)

fig, ax = plt.subplots(figsize=(8, 6))

for rho in rhos:
    rp, vol = portfolio_stats(w1_range, mu, sig, rho)
    # 绘制前沿曲线，横轴波动率、纵轴期望收益（转换为百分比显示）
    ax.plot(vol * 100, rp * 100, label=fr'$\rho = {rho}$')
    # 计算并标出该相关系数下的最小方差组合
    _, rp_mvp, vol_mvp = compute_mvp(mu, sig, rho)
    ax.scatter(vol_mvp * 100, rp_mvp * 100,
               marker='o', s=60, color='red', zorder=5)

# 添加MVP的图例
mvp_handle = Line2D([0], [0], marker='o', color='w',
                    markerfacecolor='red', markersize=8,
                    label='Minimum Variance Portfolio')
handles, labels = ax.get_legend_handles_labels()
handles.append(mvp_handle)
ax.legend(handles=handles)

# 图形修饰
ax.set_xlabel('Annualized Volatility (%)')
ax.set_ylabel('Expected Annual Return (%)')
ax.set_title('Mean-Variance Frontier for Two Risky Assets')
ax.grid(True, linestyle='--', alpha=0.7)

# 保存图形
figure_path = 'mean_variance_frontier.png'
fig.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close(fig)

# ============================
# 汇总结果
# ============================
result = {
    'mvp_vol_at_rho45': mvp_vol_at_rho45,
    'frontier_vol_at_target': frontier_vol_at_target,
    'figure_path': figure_path
}

# 可选：打印结果以供检查
print(result)
