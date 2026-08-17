import numpy as np
import matplotlib.pyplot as plt

# 资产参数
mu1, mu2 = 0.071, 0.124
sig1, sig2 = 0.163, 0.289
rhos = [0.15, 0.45, 0.75]

# 权重范围（包含卖空以展示完整前沿）
w = np.linspace(-0.5, 1.5, 1000)
mu_p = w * mu1 + (1 - w) * mu2

plt.figure(figsize=(10, 7))

mvp_vol_at_rho45 = None
frontier_vol_at_target = None

for rho in rhos:
    # 计算组合波动率
    sig_p_sq = w**2 * sig1**2 + (1 - w)**2 * sig2**2 + 2 * w * (1 - w) * rho * sig1 * sig2
    sig_p = np.sqrt(sig_p_sq)
    
    # 计算最小方差组合(MVP)
    w_mvp = (sig2**2 - rho * sig1 * sig2) / (sig1**2 + sig2**2 - 2 * rho * sig1 * sig2)
    sig_mvp = np.sqrt(w_mvp**2 * sig1**2 + (1 - w_mvp)**2 * sig2**2 + 2 * w_mvp * (1 - w_mvp) * rho * sig1 * sig2)
    mu_mvp = w_mvp * mu1 + (1 - w_mvp) * mu2
    
    # 绘制前沿曲线
    plt.plot(sig_p, mu_p, label=f'ρ = {rho}')
    # 标出最小方差组合
    plt.scatter(sig_mvp, mu_mvp, marker='D', s=80, zorder=5, edgecolors='black')
    plt.text(sig_mvp + 0.003, mu_mvp, f'  MVP\n  ({sig_mvp:.2%}, {mu_mvp:.2%})', fontsize=9)
    
    # 针对 ρ=0.45 提取特定数值
    if rho == 0.45:
        mvp_vol_at_rho45 = sig_mvp
        
        # 目标收益10%时的组合权重与波动率
        mu_target = 0.10
        w_target = (mu_target - mu2) / (mu1 - mu2)
        sig_target = np.sqrt(w_target**2 * sig1**2 + (1 - w_target)**2 * sig2**2 + 2 * w_target * (1 - w_target) * rho * sig1 * sig2)
        frontier_vol_at_target = sig_target

# 绘制原始资产点
plt.scatter(sig1, mu1, color='black', marker='*', s=200, zorder=6, label='Asset 1')
plt.scatter(sig2, mu2, color='black', marker='p', s=200, zorder=6, label='Asset 2')

plt.xlabel('Annualized Volatility')
plt.ylabel('Expected Annual Return')
plt.title('Efficient Frontier for Two Assets with Different Correlations')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)
plt.xlim(0, 0.45)
plt.ylim(0, 0.20)

# 保存图片
figure_path = 'efficient_frontier.png'
plt.savefig(figure_path, dpi=150, bbox_inches='tight')

# 按照输出契约要求存入字典
result = {
    'mvp_vol_at_rho45': float(mvp_vol_at_rho45),
    'frontier_vol_at_target': float(frontier_vol_at_target),
    'figure_path': figure_path
}

print(result)
