import numpy as np
import matplotlib.pyplot as plt

# 资产参数
E1, E2 = 0.071, 0.124
sigma1, sigma2 = 0.163, 0.289
rhos = [0.15, 0.45, 0.75]

# 权重范围（稍微扩大以展示完整的双曲线前沿）
w = np.linspace(-0.2, 1.2, 500)

# 组合收益
port_ret = w * E1 + (1 - w) * E2

plt.figure(figsize=(10, 7))

mvp_vol_45 = None
target_vol_45 = None

for rho in rhos:
    cov = rho * sigma1 * sigma2
    
    # 组合波动率
    port_vol = np.sqrt((w * sigma1)**2 + ((1 - w) * sigma2)**2 + 2 * w * (1 - w) * cov)
    
    # 画有效前沿曲线
    plt.plot(port_vol, port_ret, label=f'ρ = {rho}', linewidth=2)
    
    # 计算最小方差组合 (MVP)
    w_mvp = (sigma2**2 - cov) / (sigma1**2 + sigma2**2 - 2 * cov)
    r_mvp = w_mvp * E1 + (1 - w_mvp) * E2
    v_mvp = np.sqrt((w_mvp * sigma1)**2 + ((1 - w_mvp) * sigma2)**2 + 2 * w_mvp * (1 - w_mvp) * cov)
    
    # 在图上标出MVP
    plt.scatter(v_mvp, r_mvp, marker='*', s=300, zorder=5, edgecolors='black')
    plt.annotate(f'MVP (ρ={rho})\nVol: {v_mvp:.2%}',
                 (v_mvp, r_mvp),
                 textcoords="offset points",
                 xytext=(15, -10),
                 fontsize=9,
                 arrowprops=dict(arrowstyle='->', color='gray'))

    # 提取 ρ = 0.45 时的特定数据
    if rho == 0.45:
        mvp_vol_45 = v_mvp
        
        # 计算目标收益 10% 时的最小波动率
        target_ret = 0.10
        w_target = (target_ret - E2) / (E1 - E2)
        target_vol_45 = np.sqrt((w_target * sigma1)**2 + ((1 - w_target) * sigma2)**2 + 2 * w_target * (1 - w_target) * cov)

# 图表美化
plt.title('Efficient Frontier of Two Assets', fontsize=14)
plt.xlabel('Annualized Volatility', fontsize=12)
plt.ylabel('Expected Annual Return', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend(fontsize=11)

# 保存图表
fig_path = 'efficient_frontier.png'
plt.savefig(fig_path, dpi=300, bbox_inches='tight')
plt.close()

# 构造输出字典
result = {
    'mvp_vol_at_rho45': round(mvp_vol_45, 4),
    'frontier_vol_at_target': round(target_vol_45, 4),
    'figure_path': fig_path
}

print(result)
