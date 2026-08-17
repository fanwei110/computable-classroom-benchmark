import numpy as np
import matplotlib.pyplot as plt

# ==================== 1. 参数设定 ====================
mu1 = 0.071      # 资产1期望收益
mu2 = 0.124      # 资产2期望收益
sig1 = 0.163     # 资产1波动率
sig2 = 0.289     # 资产2波动率

rhos = [0.15, 0.45, 0.75]  # 相关系数
target_return = 0.10       # 目标期望收益

# 权重扫描范围（允许卖空，满仓约束 w1 + w2 = 1）
w1_range = np.linspace(-0.5, 1.5, 1000)
w2_range = 1 - w1_range

# ==================== 2. 绘图与计算 ====================
plt.figure(figsize=(10, 7))

# 记录特定条件下的结果
mvp_vol_at_rho45 = None
frontier_vol_at_target = None

for rho in rhos:
    # 构造协方差矩阵
    cov12 = rho * sig1 * sig2
    Sigma = np.array([[sig1**2, cov12], 
                      [cov12, sig2**2]])
    
    # 在组合权重上扫描计算前沿
    mu_p = w1_range * mu1 + w2_range * mu2
    var_p = (w1_range**2 * Sigma[0, 0] + 
             w2_range**2 * Sigma[1, 1] + 
             2 * w1_range * w2_range * Sigma[0, 1])
    sig_p = np.sqrt(var_p)
    
    # 绘制前沿曲线
    plt.plot(sig_p, mu_p, label=f'ρ = {rho:.2f}', lw=2)
    
    # ---- 解析求解最小方差组合(MVP) ----
    # 对 w1 求导令其等于0：w1_mvp = (sig2^2 - cov12) / (sig1^2 + sig2^2 - 2*cov12)
    w1_mvp = (Sigma[1, 1] - Sigma[0, 1]) / (Sigma[0, 0] + Sigma[1, 1] - 2 * Sigma[0, 1])
    w2_mvp = 1 - w1_mvp
    
    mu_mvp = w1_mvp * mu1 + w2_mvp * mu2
    var_mvp = (w1_mvp**2 * Sigma[0, 0] + 
               w2_mvp**2 * Sigma[1, 1] + 
               2 * w1_mvp * w2_mvp * Sigma[0, 1])
    sig_mvp = np.sqrt(var_mvp)
    
    # 在曲线上标出最小方差组合
    plt.scatter(sig_mvp, mu_mvp, marker='*', s=200, zorder=5, edgecolors='black', linewidths=0.8)
    plt.text(sig_mvp + 0.008, mu_mvp - 0.006, f'MVP(ρ={rho:.2f})', fontsize=9)
    
    # ---- 针对 rho=0.45 的专项计算 ----
    if rho == 0.45:
        # 1. 最小方差组合的年化波动率
        mvp_vol_at_rho45 = float(sig_mvp)
        
        # 2. 目标期望收益 10% 下可达到的最小年化波动率
        # 由 mu_p = w1*mu1 + (1-w1)*mu2 = target_return，解出 w1
        w1_target = (target_return - mu2) / (mu1 - mu2)
        w2_target = 1 - w1_target
        
        var_target = (w1_target**2 * Sigma[0, 0] + 
                      w2_target**2 * Sigma[1, 1] + 
                      2 * w1_target * w2_target * Sigma[0, 1])
        sig_target = np.sqrt(var_target)
        frontier_vol_at_target = float(sig_target)

# ==================== 3. 图表修饰 ====================
plt.xlabel('Volatility (σ)', fontsize=12)
plt.ylabel('Expected Return (μ)', fontsize=12)
plt.title('Mean-Variance Frontiers under Different Correlations', fontsize=14)
plt.legend(fontsize=11)
plt.grid(True, linestyle='--', alpha=0.6)
plt.xlim(0, 0.65)
plt.ylim(0, 0.20)

# 保存图形
fig_path = 'markowitz_frontier.png'
plt.savefig(fig_path, dpi=300, bbox_inches='tight')
plt.close()

# ==================== 4. 填充输出契约 ====================
result = {
    'mvp_vol_at_rho45': mvp_vol_at_rho45,
    'frontier_vol_at_target': frontier_vol_at_target,
    'figure_path': fig_path
}

# 控制台打印结果供教师核对
print(f"rho=0.45 时最小方差组合的年化波动率: {mvp_vol_at_rho45:.6f}")
print(f"rho=0.45 时目标期望收益10%的最小年化波动率: {frontier_vol_at_target:.6f}")
print(f"图形已保存至: {fig_path}")
