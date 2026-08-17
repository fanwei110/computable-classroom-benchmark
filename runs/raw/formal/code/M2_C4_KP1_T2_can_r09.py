import numpy as np
import matplotlib.pyplot as plt
import os

# ------------------ 参数设定 ------------------
r = np.array([0.071, 0.124])          # 期望年收益
sigma = np.array([0.163, 0.289])      # 年化波动率
rhos = [0.15, 0.45, 0.75]            # 三种相关系数
mu_target = 0.10                      # 目标期望收益

# 绘图颜色
colors = ['steelblue', 'darkorange', 'seagreen']

# 存储结果
mvp_vol_at_rho45 = None
frontier_vol_at_target = None

# ------------------ 创建图形 ------------------
fig, ax = plt.subplots(figsize=(10, 6))

# ------------------ 对每个相关系数计算并画图 ------------------
for idx, rho in enumerate(rhos):
    # 1. 协方差矩阵
    cov = np.array([[sigma[0]**2, rho * sigma[0] * sigma[1]],
                    [rho * sigma[0] * sigma[1], sigma[1]**2]])

    # 2. 扫描权重 (满仓, w1 + w2 = 1, 允许卖空)
    w1 = np.linspace(-3, 4, 2000)
    w2 = 1 - w1
    mu_p = w1 * r[0] + w2 * r[1]
    var_p = (w1**2 * sigma[0]**2 +
             w2**2 * sigma[1]**2 +
             2 * w1 * w2 * rho * sigma[0] * sigma[1])
    sigma_p = np.sqrt(np.maximum(var_p, 0))  # 防止舍入负值

    # 3. 画出前沿曲线
    ax.plot(sigma_p, mu_p, color=colors[idx], label=f'ρ = {rho}')

    # 4. 计算最小方差组合 (MVP) 的解析解
    ones = np.ones(2)
    inv_cov = np.linalg.inv(cov)
    A = ones @ inv_cov @ ones
    B = ones @ inv_cov @ r
    sigma_mvp = np.sqrt(1.0 / A)
    mu_mvp = B / A

    # 5. 在曲线上标出 MVP
    ax.scatter(sigma_mvp, mu_mvp, color=colors[idx],
               edgecolor='black', s=70, zorder=5)

    # 6. 若为 ρ=0.45，记录结果并标记目标收益点
    if rho == 0.45:
        mvp_vol_at_rho45 = sigma_mvp

        # 目标收益下的最小方差
        C = r @ inv_cov @ r
        D = A * C - B**2
        sigma_target_sq = (A * mu_target**2 - 2 * B * mu_target + C) / D
        sigma_target = np.sqrt(sigma_target_sq)
        frontier_vol_at_target = sigma_target

        # 标出目标点
        ax.scatter(sigma_target, mu_target, color='crimson', marker='X',
                   s=100, zorder=6, edgecolor='black',
                   label=f'Target μ = 10% (ρ = 0.45)')

# ------------------ 图形修饰 ------------------
ax.set_xlabel('Annualized Volatility (σ)', fontsize=12)
ax.set_ylabel('Expected Return (μ)', fontsize=12)
ax.set_title('Mean–Variance Frontier for Two Risky Assets', fontsize=14)
ax.legend(loc='upper left')
ax.grid(True, linestyle='--', alpha=0.6)

# ------------------ 保存图形 ------------------
figure_path = os.path.abspath('frontier.png')
plt.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close()

# ------------------ 构造输出字典 ------------------
result = {
    'mvp_vol_at_rho45': round(mvp_vol_at_rho45, 6),
    'frontier_vol_at_target': round(frontier_vol_at_target, 6),
    'figure_path': figure_path
}

print(result)
