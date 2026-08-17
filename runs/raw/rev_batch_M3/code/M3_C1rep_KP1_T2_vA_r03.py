import numpy as np
import matplotlib.pyplot as plt

# 资产参数
mu1, mu2 = 0.071, 0.124
sig1, sig2 = 0.163, 0.289
rhos = [0.15, 0.45, 0.75]
target_return = 0.10

# 权重范围，稍微延伸到0-1之外以展示完整的双曲线
w = np.linspace(-0.2, 1.2, 500)
mu_p = w * mu1 + (1 - w) * mu2

mvp_vol_45 = None
frontier_vol_target = None

plt.figure(figsize=(10, 6))

for i, rho in enumerate(rhos):
    cov12 = rho * sig1 * sig2
    sig_p = np.sqrt((w * sig1)**2 + ((1 - w) * sig2)**2 + 2 * w * (1 - w) * cov12)
    
    # 计算最小方差组合(MVP)
    w_mvp = (sig2**2 - cov12) / (sig1**2 + sig2**2 - 2 * cov12)
    mu_mvp = w_mvp * mu1 + (1 - w_mvp) * mu2
    sig_mvp = np.sqrt((w_mvp * sig1)**2 + ((1 - w_mvp) * sig2)**2 + 2 * w_mvp * (1 - w_mvp) * cov12)
    
    # 绘制有效前沿
    plt.plot(sig_p, mu_p, label=f'ρ = {rho}')
    
    # 标出最小方差组合
    plt.scatter(sig_mvp, mu_mvp, marker='D', s=60, zorder=5, edgecolors='black')
    plt.annotate(f'MVP(ρ={rho})\nσ={sig_mvp:.2%}', 
                 xy=(sig_mvp, mu_mvp), 
                 xytext=(10, 10 - i*20), 
                 textcoords='offset points',
                 bbox=dict(boxstyle='round,pad=0.3', fc='yellow', alpha=0.6),
                 arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))

    # 针对 rho = 0.45 计算特定指标
    if rho == 0.45:
        mvp_vol_45 = sig_mvp
        
        # 计算目标收益10%时的最小波动率
        w_target = (mu2 - target_return) / (mu2 - mu1)
        sig_target = np.sqrt((w_target * sig1)**2 + ((1 - w_target) * sig2)**2 + 2 * w_target * (1 - w_target) * cov12)
        frontier_vol_target = sig_target

# 图表美化
plt.xlabel('Volatility (Annualized)')
plt.ylabel('Expected Return (Annualized)')
plt.title('Efficient Frontier for Two Assets with Different Correlations')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)
plt.xlim(left=0)

# 保存图表
figure_path = 'efficient_frontier.png'
plt.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close()

# 按照输出契约构建result字典
result = {
    'mvp_vol_at_rho45': round(mvp_vol_45, 6),
    'frontier_vol_at_target': round(frontier_vol_target, 6),
    'figure_path': figure_path
}

print(result)
