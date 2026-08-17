import numpy as np
import matplotlib.pyplot as plt

# 给定参数
r1, r2 = 0.071, 0.124
sigma1, sigma2 = 0.163, 0.289
rhos = [0.15, 0.45, 0.75]

# 生成权重组合
w1 = np.linspace(0, 1, 500)
w2 = 1 - w1

# 存储结果
result = {}
fig, ax = plt.subplots(figsize=(8, 5))

for rho in rhos:
    # 组合期望收益和波动率
    ret = w1 * r1 + w2 * r2
    var = (w1**2 * sigma1**2 + w2**2 * sigma2**2 +
           2 * w1 * w2 * rho * sigma1 * sigma2)
    vol = np.sqrt(var)
    
    # 标记有效前沿（上半部分）
    # 找到最小方差组合的索引
    min_var_idx = np.argmin(var)
    min_vol = vol[min_var_idx]
    min_ret = ret[min_var_idx]
    
    # 绘制整条曲线
    ax.plot(vol, ret, label=f'ρ = {rho}')
    # 标记最小方差点
    ax.scatter(min_vol, min_ret, marker='o', s=50, zorder=5)
    ax.annotate(f'MVP ρ={rho}\n({min_vol:.4f}, {min_ret:.4f})',
                (min_vol, min_ret),
                textcoords="offset points",
                xytext=(10, -10),
                ha='center', fontsize=8,
                bbox=dict(boxstyle='round,pad=0.3', fc='yellow', alpha=0.5))
    
    # 记录 ρ=0.45 时的 MVP 波动率
    if rho == 0.45:
        result['mvp_vol_at_rho45'] = float(min_vol)
        # 目标收益 10% 的最小波动率
        # 在有效前沿上（收益高于 MVP 部分）
        # 直接通过权重计算
        # 所需组合权重满足 E = w*r1 + (1-w)*r2 = 0.10
        # 若解在 [0,1] 范围内
        w_target = (0.10 - r2) / (r1 - r2)  # 由于 r1<r2, 分母为负
        if 0 <= w_target <= 1:
            vol_target = np.sqrt(
                w_target**2 * sigma1**2 +
                (1 - w_target)**2 * sigma2**2 +
                2 * w_target * (1 - w_target) * rho * sigma1 * sigma2
            )
            result['frontier_vol_at_target'] = float(vol_target)
            # 在图中标记
            ret_target = 0.10
            ax.scatter(vol_target, ret_target, marker='*', s=100, color='red', zorder=10)
            ax.annotate(f'Target 10%\nvol={vol_target:.4f}',
                        (vol_target, ret_target),
                        textcoords="offset points",
                        xytext=(10, 10),
                        ha='center', fontsize=8,
                        bbox=dict(boxstyle='round,pad=0.3', fc='lightblue', alpha=0.7))

ax.set_xlabel('Volatility (σ)')
ax.set_ylabel('Expected Return')
ax.set_title('Efficient Frontier for Two Assets')
ax.legend()
ax.grid(True, linestyle='--', alpha=0.7)

figure_path = 'effective_frontier.png'
plt.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close()

result['figure_path'] = figure_path
result
