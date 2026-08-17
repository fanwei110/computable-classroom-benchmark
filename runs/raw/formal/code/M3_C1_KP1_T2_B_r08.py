import numpy as np
import matplotlib.pyplot as plt

# 资产参数
R1 = 0.071
R2 = 0.124
sig1 = 0.163
sig2 = 0.289
rhos = [0.15, 0.45, 0.75]
colors = ['blue', 'green', 'red']

# 生成资产1的权重序列
w1 = np.linspace(-0.5, 1.5, 500)

plt.figure(figsize=(10, 6))

mvp_vol_45 = None
frontier_vol_10 = None

for i, rho in enumerate(rhos):
    # 计算组合收益与波动率
    R_p = w1 * R1 + (1 - w1) * R2
    sig_p = np.sqrt(w1**2 * sig1**2 + (1 - w1)**2 * sig2**2 + 2 * w1 * (1 - w1) * rho * sig1 * sig2)
    
    # 计算最小方差组合(MVP)
    w1_mvp = (sig2**2 - rho * sig1 * sig2) / (sig1**2 + sig2**2 - 2 * rho * sig1 * sig2)
    R_mvp = w1_mvp * R1 + (1 - w1_mvp) * R2
    sig_mvp = np.sqrt(w1_mvp**2 * sig1**2 + (1 - w1_mvp)**2 * sig2**2 + 2 * w1_mvp * (1 - w1_mvp) * rho * sig1 * sig2)
    
    # 绘制前沿曲线和最小方差点
    plt.plot(sig_p, R_p, label=f'rho = {rho}', color=colors[i])
    plt.scatter(sig_mvp, R_mvp, marker='*', s=150, zorder=5, color=colors[i])
    plt.annotate(f'MVP (rho={rho})\nVol={sig_mvp:.2%}', xy=(sig_mvp, R_mvp), xytext=(5, 5), textcoords='offset points')

    # 针对rho=0.45计算所需精确值并标注10%目标收益点
    if rho == 0.45:
        mvp_vol_45 = sig_mvp
        w1_target = (0.10 - R2) / (R1 - R2)
        frontier_vol_10 = np.sqrt(w1_target**2 * sig1**2 + (1 - w1_target)**2 * sig2**2 + 2 * w1_target * (1 - w1_target) * rho * sig1 * sig2)
        
        plt.scatter(frontier_vol_10, 0.10, marker='D', s=80, zorder=5, color=colors[i])
        plt.annotate(f'Target 10%\nVol={frontier_vol_10:.2%}', xy=(frontier_vol_10, 0.10), xytext=(-80, -30), textcoords='offset points', arrowprops=dict(arrowstyle='->', connectionstyle='arc3'))

# 图表装饰
plt.xlabel('Volatility')
plt.ylabel('Return')
plt.title('Efficient Frontiers with Different Correlations')
plt.legend()
plt.grid(True)

# 保存图表
fig_path = 'efficient_frontier.png'
plt.savefig(fig_path)
plt.close()

# 封装结果字典
result = {
    'mvp_vol_at_rho45': round(mvp_vol_45, 6),
    'frontier_vol_at_target': round(frontier_vol_10, 6),
    'figure_path': fig_path
}
