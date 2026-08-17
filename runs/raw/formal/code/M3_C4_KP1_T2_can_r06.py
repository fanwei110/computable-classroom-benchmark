import numpy as np
import matplotlib.pyplot as plt

# ==================== 1. 参数设置 ====================
mu1, mu2 = 0.071, 0.124       # 期望年收益
sig1, sig2 = 0.163, 0.289     # 年化波动率
rhos = [0.15, 0.45, 0.75]     # 相关系数

# ==================== 2. 扫描权重并画图 ====================
# 允许卖空，权重范围设置大一些以完整展示双曲线前沿
w1_arr = np.linspace(-1.0, 2.0, 500)

plt.figure(figsize=(10, 6))

mvp_vol_45 = None
frontier_vol_target = None

for rho in rhos:
    # 构造协方差项
    cov12 = rho * sig1 * sig2
    
    # 组合期望收益与方差
    w2_arr = 1 - w1_arr
    mu_p = w1_arr * mu1 + w2_arr * mu2
    var_p = (w1_arr**2 * sig1**2 + w2_arr**2 * sig2**2 + 2 * w1_arr * w2_arr * cov12)
    sig_p = np.sqrt(var_p)
    
    # 画出前沿曲线
    line, = plt.plot(sig_p, mu_p, label=f'ρ = {rho:.2f}')
    color = line.get_color()
    
    # ==================== 3. 寻找并标出最小方差组合(MVP) ====================
    # 解析求解两资产满仓约束下MVP的权重
    w1_mvp = (sig2**2 - cov12) / (sig1**2 + sig2**2 - 2 * cov12)
    w2_mvp = 1 - w1_mvp
    
    # 计算MVP的收益与波动率
    mu_mvp = w1_mvp * mu1 + w2_mvp * mu2
    var_mvp = w1_mvp**2 * sig1**2 + w2_mvp**2 * sig2**2 + 2 * w1_mvp * w2_mvp * cov12
    sig_mvp = np.sqrt(var_mvp)
    
    # 在图上标出MVP点
    plt.scatter(sig_mvp, mu_mvp, marker='o', s=80, color=color, edgecolors='black', zorder=5)
    plt.annotate('MVP', (sig_mvp, mu_mvp), textcoords="offset points", xytext=(-15, 10), ha='right', fontsize=9, color=color, fontweight='bold')
    
    # ==================== 4. 针对rho=0.45计算特定指标 ====================
    if rho == 0.45:
        # 记录MVP波动率
        mvp_vol_45 = float(sig_mvp)
        
        # 目标期望收益 10% 下，两资产唯一确定了组合权重，此即该收益下的最小方差组合
        mu_target = 0.10
        w1_target = (mu_target - mu2) / (mu1 - mu2)
        w2_target = 1 - w1_target
        
        var_target = w1_target**2 * sig1**2 + w2_target**2 * sig2**2 + 2 * w1_target * w2_target * cov12
        sig_target = np.sqrt(var_target)
        frontier_vol_target = float(sig_target)
        
        # 在图上标出目标收益点
        plt.scatter(sig_target, mu_target, marker='*', s=150, color=color, edgecolors='black', zorder=5)
        plt.annotate('Target 10%', (sig_target, mu_target), textcoords="offset points", xytext=(-15, 10), ha='right', fontsize=9, color=color, fontweight='bold')

# ==================== 5. 图表美化与保存 ====================
plt.xlabel('Annualized Volatility (σ)')
plt.ylabel('Expected Annual Return (μ)')
plt.title('Mean-Variance Frontiers for Different Correlations')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)
plt.xlim(0, 0.45)
plt.ylim(0.04, 0.18)
plt.tight_layout()

fig_path = 'markowitz_frontier.png'
plt.savefig(fig_path)

# ==================== 6. 输出结果 ====================
result = {
    'mvp_vol_at_rho45': mvp_vol_45,
    'frontier_vol_at_target': frontier_vol_target,
    'figure_path': fig_path
}

# 打印结果以供核验
print(result)
