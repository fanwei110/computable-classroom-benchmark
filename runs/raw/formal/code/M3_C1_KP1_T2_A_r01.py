import numpy as np
import matplotlib.pyplot as plt
import os

# 解决中文显示问题
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# 资产参数
E1, E2 = 0.071, 0.124
S1, S2 = 0.163, 0.289
rhos = [0.15, 0.45, 0.75]

# 生成权重范围 (允许卖空，范围设为-0.2到1.2以便观察完整前沿)
w1 = np.linspace(-0.2, 1.2, 500)
w2 = 1 - w1

port_returns = w1 * E1 + w2 * E2

plt.figure(figsize=(10, 7))

mvp_vol_45 = None
frontier_vol_10_45 = None

for rho in rhos:
    # 计算组合波动率
    port_vols = np.sqrt(w1**2 * S1**2 + w2**2 * S2**2 + 2 * w1 * w2 * rho * S1 * S2)
    
    # 寻找最小方差组合 (MVP)
    w1_mvp = (S2**2 - rho * S1 * S2) / (S1**2 + S2**2 - 2 * rho * S1 * S2)
    w2_mvp = 1 - w1_mvp
    ret_mvp = w1_mvp * E1 + w2_mvp * E2
    vol_mvp = np.sqrt(w1_mvp**2 * S1**2 + w2_mvp**2 * S2**2 + 2 * w1_mvp * w2_mvp * rho * S1 * S2)
    
    # 绘制前沿曲线
    plt.plot(port_vols, port_returns, label=f'相关系数 ρ = {rho}')
    
    # 标出最小方差组合
    plt.scatter(vol_mvp, ret_mvp, marker='*', s=200, zorder=5)
    plt.annotate(f'MVP (ρ={rho})\n({vol_mvp:.2%}, {ret_mvp:.2%})', 
                 xy=(vol_mvp, ret_mvp), xytext=(15, -10), textcoords='offset points',
                 arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=-0.2'))

    # 提取 rho=0.45 时的特定数值
    if rho == 0.45:
        mvp_vol_45 = vol_mvp
        
        # 计算目标收益为10%时的最小波动率
        w1_target = (E2 - 0.10) / (E2 - E1)
        w2_target = 1 - w1_target
        frontier_vol_10_45 = np.sqrt(w1_target**2 * S1**2 + w2_target**2 * S2**2 + 2 * w1_target * w2_target * rho * S1 * S2)

# 图表美化
plt.title('两只资产的有效前沿 (不同相关系数)')
plt.xlabel('年化波动率')
plt.ylabel('期望年收益')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)
plt.xlim(0.10, 0.40)
plt.ylim(0.04, 0.16)

# 保存图片
fig_path = 'efficient_frontier.png'
plt.savefig(fig_path, dpi=300, bbox_inches='tight')
plt.close()

# 按照输出契约构建结果字典
result = {
    'mvp_vol_at_rho45': round(mvp_vol_45, 6),
    'frontier_vol_at_target': round(frontier_vol_10_45, 6),
    'figure_path': fig_path
}

print(result)
