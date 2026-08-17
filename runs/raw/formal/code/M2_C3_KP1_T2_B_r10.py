import numpy as np
import matplotlib.pyplot as plt

# 给定参数
r1, r2 = 0.071, 0.124
vol1, vol2 = 0.163, 0.289
rhos = [0.15, 0.45, 0.75]
target_return = 0.10

# 用于画图的权重范围（涵盖最小方差组合）
w_range = np.linspace(-1.5, 2.5, 400)

# 准备画图
fig, ax = plt.subplots(figsize=(10, 6))

results = {}

for rho in rhos:
    # 组合方差与收益
    var = (w_range**2 * vol1**2 + (1 - w_range)**2 * vol2**2 +
           2 * w_range * (1 - w_range) * vol1 * vol2 * rho)
    std = np.sqrt(var)
    ret = w_range * r1 + (1 - w_range) * r2
    
    # 画有效前沿（限制在双曲线右半支，展示全部组合）
    ax.plot(std, ret, label=f'$\\rho={rho}$')
    
    # 最小方差组合
    # MVP权重（资产1）
    w_mvp = (vol2**2 - vol1 * vol2 * rho) / (vol1**2 + vol2**2 - 2 * vol1 * vol2 * rho)
    mvp_std = np.sqrt(w_mvp**2 * vol1**2 + (1 - w_mvp)**2 * vol2**2 +
                      2 * w_mvp * (1 - w_mvp) * vol1 * vol2 * rho)
    mvp_ret = w_mvp * r1 + (1 - w_mvp) * r2
    ax.scatter(mvp_std, mvp_ret, marker='*', s=120, zorder=5,
               label=f'MVP $\\rho={rho}$' if rho == rhos[0] else "")
    ax.annotate(f'({mvp_std:.3f}, {mvp_ret:.3f})', (mvp_std, mvp_ret),
                textcoords="offset points", xytext=(10, -10), fontsize=8)
    
    # 保存要求的结果
    if rho == 0.45:
        results['mvp_vol_at_rho45'] = mvp_std
        # 目标收益10%时的最小波动率（即有效前沿上对应点）
        w_target = (target_return - r2) / (r1 - r2)
        target_var = (w_target**2 * vol1**2 + (1 - w_target)**2 * vol2**2 +
                      2 * w_target * (1 - w_target) * vol1 * vol2 * rho)
        target_std = np.sqrt(target_var)
        results['frontier_vol_at_target'] = target_std
        ax.scatter(target_std, target_return, marker='o', color='red', s=80, zorder=5)
        ax.annotate(f'Target 10%: ({target_std:.3f}, {target_return:.2f})',
                    (target_std, target_return), textcoords="offset points",
                    xytext=(10, 10), fontsize=9, color='red')

ax.set_xlabel('Volatility (Std Dev)')
ax.set_ylabel('Expected Return')
ax.set_title('Two-Asset Efficient Frontiers for Different Correlation Coefficients')
ax.legend()
ax.grid(True)

# 保存图片
fig_path = 'efficient_frontier.png'
plt.savefig(fig_path, dpi=150, bbox_inches='tight')
plt.close()

results['figure_path'] = fig_path

# 按要求输出字典
result = results
