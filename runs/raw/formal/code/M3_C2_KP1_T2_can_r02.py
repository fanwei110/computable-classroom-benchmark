import numpy as np
import matplotlib.pyplot as plt

# ==================== 1. 参数设定 ====================
mu1, mu2 = 0.071, 0.124        # 期望年收益
sigma1, sigma2 = 0.163, 0.289 # 年化波动率
rhos = [0.15, 0.45, 0.75]     # 相关系数列表
target_return = 0.10           # 目标期望收益

# ==================== 2. 权重扫描 ====================
# 允许卖空，权重范围拓宽至 [-0.5, 1.5] 以展现双曲线完整特征
w1_arr = np.linspace(-0.5, 1.5, 2000)
w2_arr = 1 - w1_arr

# 初始化需要输出的变量
mvp_vol_at_rho45 = None
frontier_vol_at_target = None

# ==================== 3. 绘制均值-方差前沿 ====================
fig, ax = plt.subplots(figsize=(10, 7))

# 绘制基础风险资产点
ax.scatter(sigma1, mu1, marker='*', s=200, color='black', zorder=5, label='Asset 1')
ax.scatter(sigma2, mu2, marker='*', s=200, color='darkred', zorder=5, label='Asset 2')

for rho in rhos:
    # 构造协方差项
    cov12 = rho * sigma1 * sigma2
    
    # 计算组合期望收益与方差（扫描法画前沿）
    mu_p = w1_arr * mu1 + w2_arr * mu2
    var_p = w1_arr**2 * sigma1**2 + w2_arr**2 * sigma2**2 + 2 * w1_arr * w2_arr * cov12
    vol_p = np.sqrt(var_p)
    
    # 画出前沿曲线
    ax.plot(vol_p, mu_p, label=f'ρ = {rho}', lw=2)
    
    # ---------------- 解析求解最小方差组合(MVP) ----------------
    # 对 sigma_p^2 = w1^2*sigma1^2 + (1-w1)^2*sigma2^2 + 2*w1*(1-w1)*cov12 求导令其为0
    w1_mvp = (sigma2**2 - cov12) / (sigma1**2 + sigma2**2 - 2 * cov12)
    w2_mvp = 1 - w1_mvp
    mu_mvp = w1_mvp * mu1 + w2_mvp * mu2
    var_mvp = w1_mvp**2 * sigma1**2 + w2_mvp**2 * sigma2**2 + 2 * w1_mvp * w2_mvp * cov12
    vol_mvp = np.sqrt(var_mvp)
    
    # 在图上标出最小方差组合
    ax.scatter(vol_mvp, mu_mvp, marker='o', s=80, zorder=5, edgecolor='black', facecolor='white', linewidths=1.5)
    
    # 为不同 rho 的 MVP 调整标注位置，避免重叠
    offset = {0.15: (20, 15), 0.45: (-85, -25), 0.75: (20, -25)}
    ax.annotate(f'MVP (ρ={rho})\nσ={vol_mvp:.2%}, μ={mu_mvp:.2%}',
                xy=(vol_mvp, mu_mvp), xytext=offset[rho],
                textcoords='offset points', fontsize=9,
                arrowprops=dict(arrowstyle='->', color='gray', lw=1.2))
    
    # ---------------- 针对相关系数 0.45 的特定计算 ----------------
    if abs(rho - 0.45) < 1e-6:
        mvp_vol_at_rho45 = vol_mvp
        
        # 目标期望收益下的最小波动率
        # 由 mu_p = w1*mu1 + (1-w1)*mu2 = target_return 解出权重
        w1_target = (target_return - mu2) / (mu1 - mu2)
        w2_target = 1 - w1_target
        var_target = w1_target**2 * sigma1**2 + w2_target**2 * sigma2**2 + 2 * w1_target * w2_target * cov12
        frontier_vol_at_target = np.sqrt(var_target)

# ==================== 4. 图表装饰与保存 ====================
ax.set_xlabel('Annualized Volatility (σ)', fontsize=12)
ax.set_ylabel('Annualized Expected Return (μ)', fontsize=12)
ax.set_title('Markowitz Mean-Variance Frontiers (Allow Short Selling)', fontsize=14)
ax.legend(fontsize=11)
ax.grid(True, linestyle='--', alpha=0.5)
ax.set_xlim(0, 0.55)
ax.set_ylim(0.0, 0.20)

figure_path = 'markowitz_frontier.png'
fig.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close()

# ==================== 5. 封装输出 ====================
result = {
    'mvp_vol_at_rho45': mvp_vol_at_rho45,
    'frontier_vol_at_target': frontier_vol_at_target,
    'figure_path': figure_path
}

print(result)
