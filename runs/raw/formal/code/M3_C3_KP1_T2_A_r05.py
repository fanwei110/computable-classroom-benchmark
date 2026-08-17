import numpy as np
import matplotlib.pyplot as plt
import os

# 资产参数 (小数表示)
mu1, mu2 = 0.071, 0.124
sig1, sig2 = 0.163, 0.289

# 相关系数列表
rhos = [0.15, 0.45, 0.75]

# 生成投资组合权重 (允许卖空，范围稍大以展示完整前沿)
w1 = np.linspace(-0.5, 1.5, 500)
w2 = 1 - w1

plt.figure(figsize=(10, 7))

# 计算特定要求并保存
mvp_vol_at_rho45 = None
frontier_vol_at_target = None

# 目标收益率
target_ret = 0.10

for rho in rhos:
    cov = rho * sig1 * sig2
    
    # 组合收益率与波动率
    port_ret = w1 * mu1 + w2 * mu2
    port_vol = np.sqrt((w1 * sig1)**2 + (w2 * sig2)**2 + 2 * w1 * w2 * cov)
    
    # 画前沿曲线
    plt.plot(port_vol, port_ret, label=f'ρ = {rho}', linewidth=2)
    
    # 计算并标出最小方差组合 (MVP)
    w1_mvp = (sig2**2 - cov) / (sig1**2 + sig2**2 - 2 * cov)
    w2_mvp = 1 - w1_mvp
    mvp_ret = w1_mvp * mu1 + w2_mvp * mu2
    mvp_vol = np.sqrt((w1_mvp * sig1)**2 + (w2_mvp * sig2)**2 + 2 * w1_mvp * w2_mvp * cov)
    
    plt.scatter(mvp_vol, mvp_ret, marker='*', s=200, zorder=5, edgecolors='black')
    plt.annotate(f'MVP (ρ={rho})\nVol={mvp_vol:.2%}', 
                 xy=(mvp_vol, mvp_ret), 
                 xytext=(10, 10), 
                 textcoords='offset points',
                 bbox=dict(boxstyle='round,pad=0.3', fc='white', alpha=0.7))

    # 提取特定 rho=0.45 时的数据
    if rho == 0.45:
        mvp_vol_at_rho45 = mvp_vol
        
        # 计算目标收益率 10% 下的最小波动率
        w1_target = (target_ret - mu2) / (mu1 - mu2)
        w2_target = 1 - w1_target
        frontier_vol_at_target = np.sqrt((w1_target * sig1)**2 + (w2_target * sig2)**2 + 2 * w1_target * w2_target * cov)

# 图表美化
plt.title('Two-Asset Efficient Frontier under Different Correlations', fontsize=14)
plt.xlabel('Annualized Volatility', fontsize=12)
plt.ylabel('Annualized Expected Return', fontsize=12)
plt.legend(fontsize=11)
plt.grid(True, linestyle='--', alpha=0.6)
plt.xlim(0, 0.45)
plt.ylim(0.04, 0.15)

# 保存图表
figure_path = 'efficient_frontier.png'
plt.savefig(figure_path, dpi=300, bbox_inches='tight')
plt.close()

# 按照输出契约存入字典
result = {
    'mvp_vol_at_rho45': mvp_vol_at_rho45,
    'frontier_vol_at_target': frontier_vol_at_target,
    'figure_path': figure_path
}

# 打印结果验证
print(result)
