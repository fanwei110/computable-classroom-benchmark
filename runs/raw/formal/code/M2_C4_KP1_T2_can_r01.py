import numpy as np
import matplotlib.pyplot as plt

# ---------- 资产参数 ----------
r1 = 0.071          # 资产1期望年收益
r2 = 0.124          # 资产2期望年收益
sigma1 = 0.163      # 资产1年化波动率
sigma2 = 0.289      # 资产2年化波动率

rhos = [0.15, 0.45, 0.75]

# ---------- 扫描权重 (允许卖空，满仓 w1+w2=1) ----------
w2 = np.linspace(-3, 5, 30000)   # 资产2的权重
w1 = 1.0 - w2                    # 资产1的权重

plt.figure(figsize=(10, 6))

# 存放相关系数0.45下的结果
mvp_vol_at_rho45 = None
frontier_vol_at_target = None

# ---------- 循环绘制每条前沿 ----------
for rho in rhos:
    cov12 = rho * sigma1 * sigma2
    # 组合方差与波动率
    var_p = (w1**2) * (sigma1**2) + (w2**2) * (sigma2**2) + 2 * w1 * w2 * cov12
    std_p = np.sqrt(var_p)
    ret_p = w1 * r1 + w2 * r2

    # 画组合曲线
    line, = plt.plot(std_p, ret_p, linewidth=1.2, label=f'ρ = {rho}')
    cur_color = line.get_color()

    # ---------- 计算最小方差组合 (解析解) ----------
    s1_sq = sigma1**2
    s2_sq = sigma2**2
    w2_mvp = (s1_sq - cov12) / (s1_sq + s2_sq - 2 * cov12)
    w1_mvp = 1.0 - w2_mvp
    ret_mvp = w1_mvp * r1 + w2_mvp * r2
    var_mvp = (w1_mvp**2) * s1_sq + (w2_mvp**2) * s2_sq + 2 * w1_mvp * w2_mvp * cov12
    std_mvp = np.sqrt(var_mvp)

    # 在曲线上标出最小方差组合
    plt.scatter(std_mvp, ret_mvp, marker='*', s=180,
                color=cur_color, edgecolors='black', linewidths=0.8, zorder=6)

    # 保存相关系数0.45所需的数据
    if rho == 0.45:
        mvp_vol_at_rho45 = std_mvp

        # 目标收益 10% 对应的组合 (满仓时权重唯一确定)
        r_target = 0.10
        w2_target = (r_target - r1) / (r2 - r1)
        w1_target = 1.0 - w2_target
        var_target = (w1_target**2) * s1_sq + (w2_target**2) * s2_sq + \
                     2 * w1_target * w2_target * cov12
        frontier_vol_at_target = np.sqrt(var_target)

# ---------- 图面设定 ----------
plt.xlabel('Annualized Volatility (Standard Deviation)')
plt.ylabel('Expected Annual Return')
plt.title('Mean-Variance Frontier for Two Risky Assets')
plt.legend(loc='upper left')
plt.grid(True, alpha=0.3)
plt.tight_layout()

# 保存图片
fig_path = 'mean_variance_frontier.png'
plt.savefig(fig_path, dpi=150)
plt.close()

# ---------- 打包结果 ----------
result = {
    'mvp_vol_at_rho45': round(mvp_vol_at_rho45, 8),
    'frontier_vol_at_target': round(frontier_vol_at_target, 8),
    'figure_path': fig_path
}

print(result)
