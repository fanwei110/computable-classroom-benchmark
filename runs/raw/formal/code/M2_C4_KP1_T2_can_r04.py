import os
import numpy as np
import matplotlib.pyplot as plt

# ---------- 资产参数 ----------
mu = np.array([0.071, 0.124])          # 期望年化收益 (小数)
sigma = np.array([0.163, 0.289])       # 年化波动率 (小数)
rhos = [0.15, 0.45, 0.75]             # 要展示的相关系数
target_return = 0.10                   # 目标期望收益 10%

# ---------- 初始化结果字典 ----------
result = {}

# ---------- 准备绘图 ----------
fig, ax = plt.subplots(figsize=(10, 6))
ax.set_xlabel('Volatility (Std)', fontsize=12)
ax.set_ylabel('Expected Return', fontsize=12)
ax.set_title('Mean-Variance Frontiers for Two Risky Assets', fontsize=14)
ax.grid(True, alpha=0.3)

# 为三条曲线分配颜色，保持一致性
colors = ['#1f77b4', '#ff7f0e', '#2ca02c']

# ---------- 对每个相关系数进行计算与绘图 ----------
for rho, color in zip(rhos, colors):
    # 构建协方差矩阵
    cov = np.array([[sigma[0]**2, rho * sigma[0] * sigma[1]],
                    [rho * sigma[0] * sigma[1], sigma[1]**2]])

    # ---- 1. 扫描权重绘制前沿 ----
    w1 = np.linspace(-1, 2, 1000)      # 允许卖空，满仓：w2 = 1 - w1
    w2 = 1 - w1
    port_ret = w1 * mu[0] + w2 * mu[1]
    port_var = (w1**2 * cov[0, 0] +
                w2**2 * cov[1, 1] +
                2 * w1 * w2 * cov[0, 1])
    port_vol = np.sqrt(port_var)

    ax.plot(port_vol, port_ret, color=color, lw=2,
            label=fr'$\rho = {rho}$')

    # ---- 2. 最小方差组合 (MVP) 解析解 ----
    sigma1, sigma2 = sigma
    var1, var2 = sigma1**2, sigma2**2
    cov12 = rho * sigma1 * sigma2

    # 最小方差组合权重 (满仓，允许卖空)
    w1_mvp = (var2 - cov12) / (var1 + var2 - 2 * cov12)
    w2_mvp = 1 - w1_mvp
    mu_mvp = w1_mvp * mu[0] + w2_mvp * mu[1]
    var_mvp = (w1_mvp**2 * var1 +
               w2_mvp**2 * var2 +
               2 * w1_mvp * w2_mvp * cov12)
    vol_mvp = np.sqrt(var_mvp)

    # 在曲线上标出 MVP
    ax.scatter(vol_mvp, mu_mvp, color=color, marker='*',
               s=160, zorder=5, edgecolor='black',
               label=f'MVP (ρ={rho})' if rho == rhos[0] else None)  # 只在一个图例条目中显示 MVP 标记

    # ---- 3. 记录 rho = 0.45 时的结果 ----
    if np.isclose(rho, 0.45):
        result['mvp_vol_at_rho45'] = vol_mvp
        # 给定目标收益的前沿波动率 (由权重的唯一性直接计算)
        w1_target = (target_return - mu[1]) / (mu[0] - mu[1])
        w2_target = 1 - w1_target
        var_target = (w1_target**2 * var1 +
                      w2_target**2 * var2 +
                      2 * w1_target * w2_target * cov12)
        vol_target = np.sqrt(var_target)
        result['frontier_vol_at_target'] = vol_target

# ---------- 修饰图例 (避免重复标签) ----------
handles, labels = ax.get_legend_handles_labels()
# 去除重复的 MVP 标签，只保留一个
by_label = dict(zip(labels, handles))
ax.legend(by_label.values(), by_label.keys(), fontsize=11)

# ---------- 保存图形 ----------
figure_filename = 'mean_variance_frontier.png'
fig.savefig(figure_filename, dpi=150, bbox_inches='tight')
plt.close(fig)

# 存入绝对路径
result['figure_path'] = os.path.abspath(figure_filename)

# ---------- 输出结果 ----------
print('=== 计算结果 (小数) ===')
print(f"相关系数 0.45 时最小方差组合的年化波动率: {result['mvp_vol_at_rho45']:.6f}")
print(f"目标收益 10% 时前沿最小年化波动率:    {result['frontier_vol_at_target']:.6f}")
print(f"图形已保存至: {result['figure_path']}")
