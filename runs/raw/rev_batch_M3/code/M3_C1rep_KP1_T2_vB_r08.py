import numpy as np
import matplotlib.pyplot as plt

# 1. 设置参数
r1, r2 = 0.071, 0.124
s1, s2 = 0.163, 0.289
rhos = [0.15, 0.45, 0.75]
target_ret = 0.10

# 2. 生成权重网格并计算前沿
w1 = np.linspace(-0.5, 1.5, 1000)
w2 = 1 - w1
rp = w1 * r1 + w2 * r2

plt.figure(figsize=(10, 6))
mvp_vols = {}

for rho in rhos:
    sp = np.sqrt((w1 * s1)**2 + (w2 * s2)**2 + 2 * w1 * w2 * rho * s1 * s2)
    plt.plot(sp, rp, label=f'ρ = {rho}')

    # 计算并标记最小方差点 (MVP)
    w1_mvp = (s2**2 - rho * s1 * s2) / (s1**2 + s2**2 - 2 * rho * s1 * s2)
    w2_mvp = 1 - w1_mvp
    r_mvp = w1_mvp * r1 + w2_mvp * r2
    s_mvp = np.sqrt(w1_mvp**2 * s1**2 + w2_mvp**2 * s2**2 + 2 * w1_mvp * w2_mvp * rho * s1 * s2)
    
    plt.scatter(s_mvp, r_mvp, marker='D', s=40, zorder=5)
    plt.annotate(f'MVP (ρ={rho})\n{s_mvp:.2%}, {r_mvp:.2%}', 
                 xy=(s_mvp, r_mvp), xytext=(5, 5), textcoords='offset points', fontsize=8)
    
    mvp_vols[rho] = s_mvp

# 3. 计算 rho=0.45 时的目标收益10%的波动率
w1_target = (target_ret - r2) / (r1 - r2)
w2_target = 1 - w1_target
s_target = np.sqrt(w1_target**2 * s1**2 + w2_target**2 * s2**2 + 2 * w1_target * w2_target * 0.45 * s1 * s2)

# 在图上标记目标收益点
plt.scatter(s_target, target_ret, marker='*', color='red', s=150, zorder=5)
plt.annotate(f'Target 10% (ρ=0.45)\n{s_target:.2%}', 
             xy=(s_target, target_ret), xytext=(-80, -20), textcoords='offset points', 
             fontsize=9, color='red', arrowprops=dict(arrowstyle='->', color='red'))

# 图表美化
plt.xlabel('Volatility (Standard Deviation)')
plt.ylabel('Expected Return')
plt.title('Two-Asset Efficient Frontier')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)
plt.xlim(0.10, 0.45)
plt.ylim(0.04, 0.16)

# 保存图表
figure_path = 'efficient_frontier.png'
plt.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close()

# 4. 按照输出契约存入字典
result = {
    'mvp_vol_at_rho45': mvp_vols[0.45],       # 0.1617123...
    'frontier_vol_at_target': s_target,        # 0.2024013...
    'figure_path': figure_path
}

print(result)
