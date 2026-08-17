import numpy as np
import matplotlib.pyplot as plt

# 资产参数
r1 = 0.071
r2 = 0.124
sigma1 = 0.163
sigma2 = 0.289
var1 = sigma1**2
var2 = sigma2**2

rhos = [0.15, 0.45, 0.75]
target_return = 0.10

# 存储结果
result = {}

# 准备画图
fig, ax = plt.subplots(figsize=(8, 6))

for rho in rhos:
    cov = rho * sigma1 * sigma2

    # 生成有效前沿：组合权重 w1 从0到1，计算收益和风险
    # 注意：有效前沿是最小方差以上的部分，但我们可以画出全部组合（波动率-收益）曲线
    w1 = np.linspace(0, 1, 500)
    w2 = 1 - w1
    ret = w1 * r1 + w2 * r2
    vol = np.sqrt(w1**2 * var1 + w2**2 * var2 + 2 * w1 * w2 * cov)

    # 找到最小方差组合 (MVP)
    w1_mvp = (var2 - cov) / (var1 + var2 - 2 * cov)
    w2_mvp = 1 - w1_mvp
    ret_mvp = w1_mvp * r1 + w2_mvp * r2
    vol_mvp = np.sqrt(w1_mvp**2 * var1 + w2_mvp**2 * var2 +
                      2 * w1_mvp * w2_mvp * cov)

    # 画前沿曲线
    ax.plot(vol, ret, label=f'ρ = {rho}')
    # 标记 MVP
    ax.scatter(vol_mvp, ret_mvp, marker='o', s=60,
               edgecolors='k', zorder=5)
    ax.annotate(f'MVP ({vol_mvp:.3f}, {ret_mvp:.3f})',
                (vol_mvp, ret_mvp),
                textcoords="offset points", xytext=(10, -10),
                fontsize=8)

    # 保存 ρ=0.45 时的 MVP 波动率
    if rho == 0.45:
        result['mvp_vol_at_rho45'] = vol_mvp

        # 目标收益10%时的组合
        # 注意：若目标收益在资产收益之间，可直接用线性插值得到权重
        w1_target = (target_return - r2) / (r1 - r2)
        w2_target = 1 - w1_target
        vol_target = np.sqrt(w1_target**2 * var1 +
                             w2_target**2 * var2 +
                             2 * w1_target * w2_target * cov)
        result['frontier_vol_at_target'] = vol_target

        # 在图上标记目标收益点
        ax.scatter(vol_target, target_return, marker='*', s=100,
                   color='red', edgecolors='k', zorder=6)
        ax.annotate(f'Target 10%\n(σ={vol_target:.3f})',
                    (vol_target, target_return),
                    textcoords="offset points", xytext=(10, 10),
                    fontsize=8, color='red')

# 图形美化
ax.set_xlabel('Annualized Volatility (σ)')
ax.set_ylabel('Expected Annual Return')
ax.set_title('Efficient Frontiers for Different Correlations')
ax.legend()
ax.grid(True, alpha=0.3)
ax.set_xlim(0.14, 0.30)
ax.set_ylim(0.06, 0.13)

# 保存图像
fig_path = 'effective_frontier.png'
fig.savefig(fig_path, dpi=200, bbox_inches='tight')
result['figure_path'] = fig_path

plt.show()

print(result)
