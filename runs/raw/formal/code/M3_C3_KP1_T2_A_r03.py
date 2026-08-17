import numpy as np
import matplotlib.pyplot as plt

# 1. 基础参数设定（全部使用小数表示）
mu1 = 0.071      # 资产1期望年收益
mu2 = 0.124      # 资产2期望年收益
sig1 = 0.163     # 资产1年化波动率
sig2 = 0.289     # 资产2年化波动率
rhos = [0.15, 0.45, 0.75]  # 三种相关系数
target_ret = 0.10           # 目标收益 10%

# 2. 初始化结果字典
result = {}

# 3. 目标收益权重计算（两资产组合下，权重唯一，与rho无关）
w1_target = (target_ret - mu2) / (mu1 - mu2)

# 4. 绘图准备
plt.figure(figsize=(10, 7))
# 为展示rho=0.75时的MVP（需做空资产2，w1>1），权重范围适当放宽
w1_range = np.linspace(-0.4, 1.6, 1000)

for rho in rhos:
    cov = rho * sig1 * sig2
    
    # 计算组合收益与波动率序列
    port_ret = w1_range * mu1 + (1 - w1_range) * mu2
    port_vol = np.sqrt(w1_range**2 * sig1**2 + (1 - w1_range)**2 * sig2**2 + 2 * w1_range * (1 - w1_range) * cov)
    
    # 绘制均值-方差前沿曲线
    plt.plot(port_vol, port_ret, label=f'ρ = {rho:.2f}', linewidth=2)
    
    # 计算并标出最小方差组合 (MVP)
    # 无约束MVP权重公式：w1_mvp = (sig2^2 - cov) / (sig1^2 + sig2^2 - 2*cov)
    w1_mvp = (sig2**2 - cov) / (sig1**2 + sig2**2 - 2 * cov)
    ret_mvp = w1_mvp * mu1 + (1 - w1_mvp) * mu2
    vol_mvp = np.sqrt(w1_mvp**2 * sig1**2 + (1 - w1_mvp)**2 * sig2**2 + 2 * w1_mvp * (1 - w1_mvp) * cov)
    
    plt.scatter(vol_mvp, ret_mvp, marker='D', s=80, zorder=5, edgecolors='black')
    plt.annotate(f'MVP ρ={rho:.2f}\nVol={vol_mvp:.2%}', 
                 xy=(vol_mvp, ret_mvp), 
                 xytext=(15, -20), 
                 textcoords='offset points',
                 arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=-0.2'),
                 bbox=dict(boxstyle='round,pad=0.3', fc='white', alpha=0.8))

    # 5. 提取 rho=0.45 时的特定数值并存入字典
    if rho == 0.45:
        result['mvp_vol_at_rho45'] = vol_mvp
        
        # 计算目标收益10%时的最小波动率
        vol_target = np.sqrt(w1_target**2 * sig1**2 + (1 - w1_target)**2 * sig2**2 + 2 * w1_target * (1 - w1_target) * cov)
        result['frontier_vol_at_target'] = vol_target

# 标出单项资产点以便对照
plt.scatter(sig1, mu1, color='black', marker='o', s=100, zorder=5, label='Asset 1')
plt.scatter(sig2, mu2, color='black', marker='s', s=100, zorder=5, label='Asset 2')

plt.title('Efficient Frontiers with Different Correlations', fontsize=14)
plt.xlabel('Annualized Volatility', fontsize=12)
plt.ylabel('Annualized Expected Return', fontsize=12)
plt.legend(fontsize=11)
plt.grid(True, linestyle='--', alpha=0.6)
plt.xlim(0.13, 0.43)
plt.ylim(0.03, 0.16)

# 6. 保存图表并写入字典
fig_path = 'efficient_frontier.png'
plt.savefig(fig_path, dpi=300, bbox_inches='tight')
result['figure_path'] = fig_path

# 打印结果以供核对
print(result)
