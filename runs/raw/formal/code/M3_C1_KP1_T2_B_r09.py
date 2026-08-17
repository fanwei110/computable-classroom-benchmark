import numpy as np
import matplotlib.pyplot as plt
import os

# 资产参数
r1, r2 = 0.071, 0.124
s1, s2 = 0.163, 0.289
rhos = [0.15, 0.45, 0.75]
target_ret = 0.10

# 权重范围 (允许卖空以展示完整的双曲线)
w = np.linspace(-0.5, 1.5, 500)

# 初始化结果存储
mvp_vol_at_rho45 = None
frontier_vol_at_target = None

# 绘图设置
plt.figure(figsize=(10, 6))
colors = ['blue', 'green', 'red']

for i, rho in enumerate(rhos):
    # 计算投资组合的收益和波动率
    ret = w * r1 + (1 - w) * r2
    vol = np.sqrt((w * s1)**2 + ((1 - w) * s2)**2 + 2 * w * (1 - w) * rho * s1 * s2)
    
    # 计算最小方差组合 (MVP)
    w_mvp = (s2**2 - rho * s1 * s2) / (s1**2 + s2**2 - 2 * rho * s1 * s2)
    ret_mvp = w_mvp * r1 + (1 - w_mvp) * r2
    vol_mvp = np.sqrt((w_mvp * s1)**2 + ((1 - w_mvp) * s2)**2 + 2 * w_mvp * (1 - w_mvp) * rho * s1 * s2)
    
    # 绘制有效前沿曲线
    plt.plot(vol, ret, label=f'ρ = {rho}', color=colors[i])
    # 标出最小方差点
    plt.scatter(vol_mvp, ret_mvp, color=colors[i], marker='D', s=60, zorder=5)
    plt.annotate(f'MVP (ρ={rho})\n({vol_mvp:.2%}, {ret_mvp:.2%})',
                 xy=(vol_mvp, ret_mvp), xytext=(15, 15), textcoords='offset points',
                 fontsize=9, arrowprops=dict(arrowstyle='->', color=colors[i]))

    # 针对 rho = 0.45 的特定计算
    if rho == 0.45:
        mvp_vol_at_rho45 = vol_mvp
        
        # 计算目标收益10%时的最小波动率
        w_target = (target_ret - r2) / (r1 - r2)
        vol_target = np.sqrt((w_target * s1)**2 + ((1 - w_target) * s2)**2 + 2 * w_target * (1 - w_target) * rho * s1 * s2)
        frontier_vol_at_target = vol_target
        
        # 在图上标出目标收益点
        plt.scatter(vol_target, target_ret, color='black', marker='*', s=100, zorder=5)
        plt.annotate(f'Target 10% (ρ=0.45)\n({vol_target:.2%}, {target_ret:.2%})',
                     xy=(vol_target, target_ret), xytext=(-100, -40), textcoords='offset points',
                     fontsize=9, arrowprops=dict(arrowstyle='->', color='black'))

# 图表美化
plt.xlabel('Volatility (Standard Deviation)')
plt.ylabel('Expected Return')
plt.title('Efficient Frontier for Two-Asset Portfolio')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)
plt.xlim(0.10, 0.50)
plt.ylim(0.04, 0.16)

# 保存图像
figure_path = 'efficient_frontier.png'
plt.savefig(figure_path, dpi=300, bbox_inches='tight')
plt.close()

# 构建输出契约字典
result = {
    'mvp_vol_at_rho45': mvp_vol_at_rho45,
    'frontier_vol_at_target': frontier_vol_at_target,
    'figure_path': figure_path
}

print(result)
