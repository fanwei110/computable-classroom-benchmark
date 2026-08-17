import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# ==================== 1. 基础参数设定 ====================
mu = np.array([0.071, 0.124])        # 期望年收益
sigma = np.array([0.163, 0.289])     # 年化波动率
rhos = [0.15, 0.45, 0.75]            # 给定的三种相关系数
target_mu = 0.10                     # 目标期望收益 10%

# 初始化结果字典
result = {}

# ==================== 2. 计算与绘图 ====================
plt.figure(figsize=(10, 7))

# 允许卖空，将权重扫描范围适当放大以覆盖目标收益及可能的做空情况
w1_range = np.linspace(-0.5, 1.5, 1000)
w2_range = 1 - w1_range

# 用于记录 rho=0.45 时的特定计算结果
mvp_vol_45 = None
frontier_vol_target = None

for rho in rhos:
    # 构造协方差矩阵
    cov_matrix = np.array([
        [sigma[0]**2, rho * sigma[0] * sigma[1]],
        [rho * sigma[0] * sigma[1], sigma[1]**2]
    ])
    
    # ---------- 计算最小方差组合 (MVP) ----------
    ones = np.ones(2)
    inv_cov = np.linalg.inv(cov_matrix)
    # 满仓约束下，全局最小方差组合权重公式: w_mvp = (Σ^-1 * 1) / (1' * Σ^-1 * 1)
    w_mvp = (inv_cov @ ones) / (ones @ inv_cov @ ones)
    mu_mvp = w_mvp @ mu
    var_mvp = w_mvp @ cov_matrix @ w_mvp
    sigma_mvp = np.sqrt(var_mvp)
    
    # ---------- 计算 rho=0.45 时的特定指标 ----------
    if np.isclose(rho, 0.45):
        mvp_vol_45 = sigma_mvp
        
        # 满仓约束与目标收益约束联立：w1*mu1 + w2*mu2 = target_mu, w1 + w2 = 1
        # 解得：w1 = (target_mu - mu2) / (mu1 - mu2)
        w1_target = (target_mu - mu[1]) / (mu[0] - mu[1])
        w_target = np.array([w1_target, 1 - w1_target])
        var_target = w_target @ cov_matrix @ w_target
        frontier_vol_target = np.sqrt(var_target)

    # ---------- 计算均值-方差前沿曲线 ----------
    # 使用向量化计算组合方差 w'Σw = w1^2*σ1^2 + w2^2*σ2^2 + 2*w1*w2*σ12
    var_range = (w1_range**2) * cov_matrix[0, 0] + \
                (w2_range**2) * cov_matrix[1, 1] + \
                2 * w1_range * w2_range * cov_matrix[0, 1]
    sigma_range = np.sqrt(var_range)
    mu_range = w1_range * mu[0] + w2_range * mu[1]

    # 绘制前沿曲线
    plt.plot(sigma_range, mu_range, label=f'$\\rho = {rho}$', lw=2)
    
    # 在曲线上标出最小方差组合
    plt.scatter(sigma_mvp, mu_mvp, zorder=5)
    plt.annotate(f'MVP ($\\rho$={rho})\n$\\sigma$={sigma_mvp:.2%}', 
                 xy=(sigma_mvp, mu_mvp), 
                 xytext=(15, 10), 
                 textcoords='offset points',
                 fontsize=9,
                 arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))

# ==================== 3. 图表美化与保存 ====================
plt.title('Mean-Variance Frontiers with Different Correlations', fontsize=14)
plt.xlabel('Annualized Volatility ($\\sigma$)', fontsize=12)
plt.ylabel('Expected Annual Return ($\\mu$)', fontsize=12)
plt.legend(fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)

# 坐标轴百分比格式化
plt.gca().xaxis.set_major_formatter(mticker.PercentFormatter(1.0, decimals=1))
plt.gca().yaxis.set_major_formatter(mticker.PercentFormatter(1.0, decimals=1))

# 保存图形
fig_path = 'markowitz_frontier.png'
plt.savefig(fig_path, dpi=300, bbox_inches='tight')

# ==================== 4. 填充结果字典 ====================
result['mvp_vol_at_rho45'] = mvp_vol_45
result['frontier_vol_at_target'] = frontier_vol_target
result['figure_path'] = fig_path

# 打印结果以供核验
print(f"Result Dictionary: {result}")
