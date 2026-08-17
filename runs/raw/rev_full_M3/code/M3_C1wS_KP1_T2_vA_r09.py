import numpy as np
import matplotlib.pyplot as plt

# ==================== 参数设置 ====================
mu = np.array([0.071, 0.124])           # 期望年收益
sigmas = np.array([0.163, 0.289])       # 年化波动率
rhos = [0.15, 0.45, 0.75]               # 相关系数
target_ret = 0.10                       # 目标收益 10%

# ==================== 初始化结果字典 ====================
result = {}

# ==================== 绘图设置 ====================
fig, ax = plt.subplots(figsize=(10, 6))

# 满仓约束下 (w1 + w2 = 1)，通过扫描 w1 生成前沿曲线
# 允许一定程度的卖空以展示完整的双曲线前沿
w1_scan = np.linspace(-0.5, 1.5, 1000)
w2_scan = 1 - w1_scan
weights_scan = np.vstack([w1_scan, w2_scan])

mvp_vol_at_rho45 = None
frontier_vol_at_target = None

for rho in rhos:
    # 1. 构造协方差矩阵
    cov12 = rho * sigmas[0] * sigmas[1]
    cov_matrix = np.array([
        [sigmas[0]**2, cov12],
        [cov12, sigmas[1]**2]
    ])
    
    # 2. 计算扫描权重下的组合收益与波动率
    port_ret = weights_scan.T @ mu
    # 高效计算方差向量，避免构造大矩阵
    port_var = (weights_scan.T @ cov_matrix * weights_scan.T).sum(axis=1)
    port_vol = np.sqrt(np.maximum(port_var, 0))  # 防止数值误差导致负数
    
    # 3. 解析求解最小方差组合 (MVP)
    cov11 = cov_matrix[0, 0]
    cov22 = cov_matrix[1, 1]
    w1_mvp = (cov22 - cov12) / (cov11 + cov22 - 2 * cov12)
    w2_mvp = 1 - w1_mvp
    w_mvp = np.array([w1_mvp, w2_mvp])
    
    mvp_ret = w_mvp @ mu
    mvp_var = w_mvp @ cov_matrix @ w_mvp
    mvp_vol = np.sqrt(mvp_var)
    
    # 绘制前沿曲线
    ax.plot(port_vol, port_ret, label=f'ρ = {rho:.2f}')
    
    # 标出最小方差组合
    ax.scatter(mvp_vol, mvp_ret, marker='D', s=80, zorder=5)
    ax.annotate('MVP', (mvp_vol, mvp_ret), textcoords="offset points", xytext=(10, 5), ha='center')
    
    # 4. 对相关系数 0.45 计算所需的两个波动率
    if np.isclose(rho, 0.45):
        mvp_vol_at_rho45 = mvp_vol
        
        # 计算目标收益 10% 下的最小波动率
        w1_target = (target_ret - mu[1]) / (mu[0] - mu[1])
        w2_target = 1 - w1_target
        w_target = np.array([w1_target, w2_target])
        
        target_var = w_target @ cov_matrix @ w_target
        frontier_vol_at_target = np.sqrt(target_var)
        
        # 在图上标出目标收益点
        ax.scatter(frontier_vol_at_target, target_ret, marker='*', s=200, color='red', zorder=5, label='Target 10% (ρ=0.45)')
        ax.annotate('10% Target', (frontier_vol_at_target, target_ret), textcoords="offset points", xytext=(10, -10), ha='center')

# ==================== 图表美化 ====================
ax.set_xlabel('Annualized Volatility (σ)')
ax.set_ylabel('Expected Annual Return (μ)')
ax.set_title('Markowitz Mean-Variance Efficient Frontier')
ax.legend()
ax.grid(True, linestyle='--', alpha=0.7)

# ==================== 保存图形 ====================
fig_path = 'efficient_frontier.png'
plt.savefig(fig_path, dpi=150, bbox_inches='tight')

# ==================== 填充结果 ====================
result['mvp_vol_at_rho45'] = mvp_vol_at_rho45
result['frontier_vol_at_target'] = frontier_vol_at_target
result['figure_path'] = fig_path

# 打印结果供验证
print(result)
