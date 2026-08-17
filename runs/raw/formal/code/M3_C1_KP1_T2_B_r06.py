import numpy as np
import matplotlib.pyplot as plt

# 资产参数
r1, r2 = 0.071, 0.124
v1, v2 = 0.163, 0.289
rhos = [0.15, 0.45, 0.75]
target_return = 0.10

# 权重范围（包含卖空情况以展现完整双曲线）
w1 = np.linspace(-0.5, 1.5, 1000)
w2 = 1 - w1

plt.figure(figsize=(10, 7))

mvp_vol_45 = None
frontier_vol_target = None

for rho in rhos:
    # 计算组合收益与波动率
    port_ret = w1 * r1 + w2 * r2
    port_vol = np.sqrt((w1 * v1)**2 + (w2 * v2)**2 + 2 * w1 * w2 * rho * v1 * v2)
    
    # 绘制曲线
    plt.plot(port_vol, port_ret, label=f'ρ = {rho}')
    
    # 计算最小方差组合(MVP)
    w1_mvp = (v2**2 - rho * v1 * v2) / (v1**2 + v2**2 - 2 * rho * v1 * v2)
    w2_mvp = 1 - w1_mvp
    mvp_ret = w1_mvp * r1 + w2_mvp * r2
    mvp_vol = np.sqrt((w1_mvp * v1)**2 + (w2_mvp * v2)**2 + 2 * w1_mvp * w2_mvp * rho * v1 * v2)
    
    # 标出最小方差点
    plt.scatter(mvp_vol, mvp_ret, marker='*', s=200, zorder=5)
    plt.annotate(f'MVP (ρ={rho})\nVol: {mvp_vol:.2%}', 
                 xy=(mvp_vol, mvp_ret), 
                 xytext=(mvp_vol + 0.015, mvp_ret - 0.008),
                 arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=5))
                 
    # 针对 rho=0.45 计算题目要求数值
    if rho == 0.45:
        mvp_vol_45 = mvp_vol
        
        # 计算目标收益10%时的最小波动率
        w1_target = (target_return - r2) / (r1 - r2)
        w2_target = 1 - w1_target
        frontier_vol_target = np.sqrt((w1_target * v1)**2 + (w2_target * v2)**2 + 2 * w1_target * w2_target * rho * v1 * v2)
        
        # 在图上标出目标收益点
        plt.scatter(frontier_vol_target, target_return, marker='D', s=80, color='red', zorder=5)
        plt.annotate(f'Target 10% (ρ=0.45)\nMin Vol: {frontier_vol_target:.2%}',
                     xy=(frontier_vol_target, target_return),
                     xytext=(frontier_vol_target + 0.015, target_return + 0.008),
                     arrowprops=dict(facecolor='red', shrink=0.05, width=1, headwidth=5))

# 图表美化
plt.title('两资产有效前沿 (不同相关系数)', fontsize=14)
plt.xlabel('波动率', fontsize=12)
plt.ylabel('收益率', fontsize=12)
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)
plt.xlim(0.10, 0.45)
plt.ylim(0.04, 0.16)

# 保存图片
fig_path = 'efficient_frontier.png'
plt.savefig(fig_path, dpi=300, bbox_inches='tight')
plt.close()

# 按照输出契约构建结果字典
result = {
    'mvp_vol_at_rho45': round(mvp_vol_45, 4),          # 0.45相关系数下MVP的波动率
    'frontier_vol_at_target': round(frontier_vol_target, 4), # 目标收益10%时的最小波动率
    'figure_path': fig_path
}

print(result)
