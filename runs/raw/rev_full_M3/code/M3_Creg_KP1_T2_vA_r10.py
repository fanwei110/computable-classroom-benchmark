import numpy as np
import matplotlib.pyplot as plt

# =========================================================
# 输入数据
# =========================================================
mu1 = 0.071       # 资产1期望年收益
mu2 = 0.124       # 资产2期望年收益
sig1 = 0.163      # 资产1年化波动率
sig2 = 0.289      # 资产2年化波动率
rhos = [0.15, 0.45, 0.75]  # 给定的相关系数
mu_target = 0.10  # 目标期望收益

# =========================================================
# 均值-方差前沿计算与绘图
# =========================================================
# 资产1的权重范围，允许卖空所以范围扩展到 [-0.5, 1.5]
w1_range = np.linspace(-0.5, 1.5, 500)

fig, ax = plt.subplots(figsize=(10, 7))

# 为防止标注重叠，预设不同相关系数的标注偏移量
annotation_offsets = {
    0.15: (10, 5),
    0.45: (10, -20),
    0.75: (-80, -20)
}

# 存储特定结果
mvp_vol_at_rho45 = None
frontier_vol_at_target = None

for rho in rhos:
    # --- 1. 计算均值-方差前沿曲线 ---
    # 资产2的权重
    w2_range = 1 - w1_range
    
    # 组合期望收益
    mu_p = w1_range * mu1 + w2_range * mu2
    
    # 组合方差与波动率
    var_p = (w1_range**2 * sig1**2 + 
             w2_range**2 * sig2**2 + 
             2 * w1_range * w2_range * rho * sig1 * sig2)
    sig_p = np.sqrt(np.maximum(var_p, 0))
    
    # 绘制前沿曲线
    ax.plot(sig_p, mu_p, label=f'$\\rho = {rho}$')
    
    # --- 2. 计算最小方差组合 (MVP) ---
    # 求解使方差最小的资产1权重
    w1_mvp = (sig2**2 - rho * sig1 * sig2) / (sig1**2 + sig2**2 - 2 * rho * sig1 * sig2)
    w2_mvp = 1 - w1_mvp
    
    # MVP的收益与波动率
    mu_mvp = w1_mvp * mu1 + w2_mvp * mu2
    var_mvp = (w1_mvp**2 * sig1**2 + 
               w2_mvp**2 * sig2**2 + 
               2 * w1_mvp * w2_mvp * rho * sig1 * sig2)
    sig_mvp = np.sqrt(var_mvp)
    
    # 在图中标注MVP点
    ax.scatter(sig_mvp, mu_mvp, zorder=5)
    offset = annotation_offsets.get(rho, (10, 10))
    ax.annotate(f'MVP ($\\rho={rho}$)\n$\\sigma={sig_mvp:.4f}$', 
                xy=(sig_mvp, mu_mvp), 
                xytext=offset, textcoords='offset points', fontsize=9,
                arrowprops=dict(arrowstyle='->', connectionstyle='arc3'))
    
    # --- 3. 针对相关系数 0.45 的特定计算 ---
    if np.isclose(rho, 0.45):
        mvp_vol_at_rho45 = sig_mvp
        
        # 目标期望收益下的组合权重
        w1_target = (mu_target - mu2) / (mu1 - mu2)
        w2_target = 1 - w1_target
        
        # 目标期望收益下的最小波动率
        var_target = (w1_target**2 * sig1**2 + 
                      w2_target**2 * sig2**2 + 
                      2 * w1_target * w2_target * rho * sig1 * sig2)
        frontier_vol_at_target = np.sqrt(var_target)

# =========================================================
# 图表格式修饰
# =========================================================
# 标出单项风险资产
ax.scatter([sig1, sig2], [mu1, mu2], color='black', zorder=6, label='Individual Assets')
ax.annotate('Asset 1', xy=(sig1, mu1), xytext=(-50, -20), textcoords='offset points', fontsize=10)
ax.annotate('Asset 2', xy=(sig2, mu2), xytext=(10, -10), textcoords='offset points', fontsize=10)

# 标出目标期望收益线
ax.axhline(y=mu_target, color='gray', linestyle='--', linewidth=1, label=f'Target Return ({mu_target:.0%})')

ax.set_xlabel('Volatility (Annualized)', fontsize=12)
ax.set_ylabel('Expected Return (Annualized)', fontsize=12)
ax.set_title('Mean-Variance Frontiers for Different Correlations', fontsize=14)
ax.legend()
ax.grid(True, linestyle='--', alpha=0.7)

# 保存图表
fig_path = 'mean_variance_frontier.png'
plt.savefig(fig_path, dpi=150, bbox_inches='tight')
plt.close()

# =========================================================
# 输出契约组装
# =========================================================
result = {
    'mvp_vol_at_rho45': mvp_vol_at_rho45,
    'frontier_vol_at_target': frontier_vol_at_target,
    'figure_path': fig_path
}

print(result)
