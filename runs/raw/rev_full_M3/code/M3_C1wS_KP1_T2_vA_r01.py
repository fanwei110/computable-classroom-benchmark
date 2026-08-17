import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 1. 参数设定
# ==========================================
mu = np.array([0.071, 0.124])        # 期望年收益 (7.1%, 12.4%)
sigma = np.array([0.163, 0.289])     # 年化波动率 (16.3%, 28.9%)
rhos = [0.15, 0.45, 0.75]           # 需要绘制的前沿相关系数

# 用于扫描的权重网格 (w1从-0.5到1.5，w2 = 1 - w1)
w1_grid = np.linspace(-0.5, 1.5, 1000)

# ==========================================
# 2. 初始化结果字典
# ==========================================
result = {
    'mvp_vol_at_rho45': None,
    'frontier_vol_at_target': None,
    'figure_path': None
}

plt.figure(figsize=(10, 7))
first_mvp_plot = True

# ==========================================
# 3. 遍历相关系数，计算并绘图
# ==========================================
for rho in rhos:
    # 构造协方差矩阵
    cov12 = rho * sigma[0] * sigma[1]
    cov_matrix = np.array([[sigma[0]**2, cov12],
                           [cov12, sigma[1]**2]])
    
    # 在组合权重上扫描计算前沿
    w2_grid = 1 - w1_grid
    mu_p = w1_grid * mu[0] + w2_grid * mu[1]
    var_p = (w1_grid**2 * cov_matrix[0, 0] + 
             w2_grid**2 * cov_matrix[1, 1] + 
             2 * w1_grid * w2_grid * cov_matrix[0, 1])
    sig_p = np.sqrt(var_p)
    
    # 绘制前沿曲线
    plt.plot(sig_p, mu_p, label=f'ρ = {rho}')
    
    # 解析求解最小方差组合
    # 满仓约束(w1+w2=1)下，对w1求导令其为0可得：w1_mvp = (sig2^2 - cov12) / (sig1^2 + sig2^2 - 2*cov12)
    w1_mvp = (cov_matrix[1, 1] - cov_matrix[0, 1]) / (cov_matrix[0, 0] + cov_matrix[1, 1] - 2 * cov_matrix[0, 1])
    w2_mvp = 1 - w1_mvp
    mu_mvp = w1_mvp * mu[0] + w2_mvp * mu[1]
    var_mvp = (w1_mvp**2 * cov_matrix[0, 0] + 
               w2_mvp**2 * cov_matrix[1, 1] + 
               2 * w1_mvp * w2_mvp * cov_matrix[0, 1])
    sig_mvp = np.sqrt(var_mvp)
    
    # 在图上标出最小方差组合
    mvp_label = 'Minimum Variance Portfolio' if first_mvp_plot else None
    plt.scatter(sig_mvp, mu_mvp, marker='o', color='black', s=60, zorder=5, label=mvp_label)
    first_mvp_plot = False
    
    # 如果是 rho = 0.45，计算需要的两个波动率
    if np.isclose(rho, 0.45):
        # 1) rho=0.45时的最小方差组合波动率
        result['mvp_vol_at_rho45'] = sig_mvp
        
        # 2) 目标收益10%时的最小波动率
        # 两资产满仓约束下，目标收益唯一确定了权重配置，因此该权重下的波动率即为该目标下的最小波动率
        target_ret = 0.10
        w1_target = (target_ret - mu[1]) / (mu[0] - mu[1])
        w2_target = 1 - w1_target
        var_target = (w1_target**2 * cov_matrix[0, 0] + 
                      w2_target**2 * cov_matrix[1, 1] + 
                      2 * w1_target * w2_target * cov_matrix[0, 1])
        sig_target = np.sqrt(var_target)
        result['frontier_vol_at_target'] = sig_target

# ==========================================
# 4. 图形美化与保存
# ==========================================
plt.title('Markowitz Mean-Variance Frontier (Two Assets)')
plt.xlabel('Annualized Volatility')
plt.ylabel('Expected Annual Return')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)

# 保存图形
fig_path = 'markowitz_frontier.png'
plt.savefig(fig_path, dpi=150, bbox_inches='tight')
plt.close()

result['figure_path'] = fig_path

# 打印结果以供核对
print(result)
