import numpy as np
import matplotlib.pyplot as plt

# ==================== 1. 参数设定 ====================
mu1, mu2 = 0.071, 0.124       # 期望年收益
sigma1, sigma2 = 0.163, 0.289 # 年化波动率
rhos = [0.15, 0.45, 0.75]     # 相关系数
target_return = 0.10          # 目标期望收益

# 满仓且允许卖空，w1从-0.5到1.5扫描足以覆盖有效前沿及延伸
w1 = np.linspace(-0.5, 1.5, 1000)
w2 = 1 - w1

# 组合期望收益
port_returns = w1 * mu1 + w2 * mu2

# ==================== 2. 计算与绘图 ====================
plt.figure(figsize=(10, 7))

mvp_vol_at_rho45 = None
frontier_vol_at_target = None

for rho in rhos:
    # 构造协方差矩阵元素
    cov12 = rho * sigma1 * sigma2
    
    # 组合方差与波动率
    port_var = (w1**2) * (sigma1**2) + (w2**2) * (sigma2**2) + 2 * w1 * w2 * cov12
    port_vol = np.sqrt(port_var)
    
    # 画出均值-方差前沿曲线
    plt.plot(port_vol, port_returns, label=f'ρ = {rho:.2f}', linewidth=2)
    
    # ---------- 最小方差组合 (MVP) 计算 ----------
    # 对 w1 求导令其等于 0: w1_mvp = (sigma2^2 - cov12) / (sigma1^2 + sigma2^2 - 2*cov12)
    w1_mvp = (sigma2**2 - cov12) / (sigma1**2 + sigma2**2 - 2 * cov12)
    w2_mvp = 1 - w1_mvp
    
    mu_mvp = w1_mvp * mu1 + w2_mvp * mu2
    var_mvp = (w1_mvp**2) * (sigma1**2) + (w2_mvp**2) * (sigma2**2) + 2 * w1_mvp * w2_mvp * cov12
    vol_mvp = np.sqrt(var_mvp)
    
    # 在图上标出最小方差组合
    plt.scatter(vol_mvp, mu_mvp, marker='*', s=150, zorder=5, edgecolors='black', linewidths=0.5)
    
    # ---------- 针对 rho = 0.45 的特定计算 ----------
    if rho == 0.45:
        mvp_vol_at_rho45 = vol_mvp
        
        # 目标期望收益下的权重
        w1_target = (target_return - mu2) / (mu1 - mu2)
        w2_target = 1 - w1_target
        
        # 目标期望收益下的最小波动率
        var_target = (w1_target**2) * (sigma1**2) + (w2_target**2) * (sigma2**2) + 2 * w1_target * w2_target * cov12
        frontier_vol_at_target = np.sqrt(var_target)
        
        # 在图上标出目标收益点
        plt.scatter(frontier_vol_at_target, target_return, marker='D', color='red', s=80, zorder=5)
        plt.annotate(f'Target 10%\nVol={frontier_vol_at_target:.2%}', 
                     (frontier_vol_at_target, target_return), 
                     textcoords="offset points", xytext=(10,10), fontsize=9,
                     arrowprops=dict(arrowstyle='->', color='red'))

# ==================== 3. 图形修饰 ====================
plt.title('Mean-Variance Frontiers for Different Correlations', fontsize=14)
plt.xlabel('Volatility (Annualized)', fontsize=12)
plt.ylabel('Expected Return (Annualized)', fontsize=12)
plt.legend(fontsize=11)
plt.grid(True, linestyle='--', alpha=0.7)
plt.xlim(0, 0.55)
plt.ylim(0.0, 0.20)

# 保存图形
figure_path = 'mean_variance_frontier.png'
plt.savefig(figure_path, dpi=300, bbox_inches='tight')
plt.close()

# ==================== 4. 填充输出字典 ====================
result = {
    'mvp_vol_at_rho45': mvp_vol_at_rho45,
    'frontier_vol_at_target': frontier_vol_at_target,
    'figure_path': figure_path
}

# 控制台输出以便当堂验证
print("="----"== 计算结果 ==------=")
print(f"相关系数 0.45 时的最小方差组合波动率: {result['mvp_vol_at_rho45']:.6f} ({result['mvp_vol_at_rho45']:.2%})")
print(f"相关系数 0.45 时目标收益 10% 的最小波动率: {result['frontier_vol_at_target']:.6f} ({result['frontier_vol_at_target']:.2%})")
print(f"图形已保存至: {result['figure_path']}")
print("="----"===============")

print("\nResult Dictionary:")
print(result)
