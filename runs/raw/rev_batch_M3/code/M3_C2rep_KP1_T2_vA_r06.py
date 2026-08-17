import numpy as np
import matplotlib.pyplot as plt

# ==================== 1. 参数设定 ====================
# 期望年收益
mu = np.array([0.071, 0.124])
# 年化波动率
sigma = np.array([0.163, 0.289])
# 相关系数列表
rhos = [0.15, 0.45, 0.75]

# 目标期望收益
target_return = 0.10

# 在满仓约束下，对资产1的权重进行扫描（允许卖空，故范围放宽至[-0.5, 1.5]以展示完整双曲线）
w1_vals = np.linspace(-0.5, 1.5, 1000)

# 存储结果的字典
result = {}

# ==================== 2. 绘图与计算 ====================
fig, ax = plt.subplots(figsize=(10, 7))

colors = ['blue', 'green', 'red']

for i, rho in enumerate(rhos):
    # 构造协方差矩阵
    cov = np.array([
        [sigma[0]**2, rho * sigma[0] * sigma[1]],
        [rho * sigma[0] * sigma[1], sigma[1]**2]
    ])
    
    # 满仓约束下 w2 = 1 - w1
    w2_vals = 1 - w1_vals
    
    # 计算组合的期望收益与波动率
    port_returns = w1_vals * mu[0] + w2_vals * mu[1]
    port_vars = w1_vals**2 * cov[0,0] + w2_vals**2 * cov[1,1] + 2 * w1_vals * w2_vals * cov[0,1]
    port_vols = np.sqrt(port_vars)
    
    # 画出均值-方差前沿
    ax.plot(port_vols, port_returns, label=f'rho = {rho}', color=colors[i], linestyle='-', linewidth=2)
    
    # ---------------- 求解最小方差组合(MVP) ----------------
    # 利用解析解求解MVP权重 w1_mvp
    w1_mvp = (cov[1,1] - cov[0,1]) / (cov[0,0] + cov[1,1] - 2 * cov[0,1])
    w2_mvp = 1 - w1_mvp
    
    mvp_return = w1_mvp * mu[0] + w2_mvp * mu[1]
    mvp_var = w1_mvp**2 * cov[0,0] + w2_mvp**2 * cov[1,1] + 2 * w1_mvp * w2_mvp * cov[0,1]
    mvp_vol = np.sqrt(mvp_var)
    
    # 在每条曲线上标出最小方差组合
    ax.scatter(mvp_vol, mvp_return, color=colors[i], marker='*', s=300, zorder=5, edgecolors='black')
    ax.annotate(f'MVP (rho={rho})', xy=(mvp_vol, mvp_return), xytext=(10, 5), 
                textcoords='offset points', fontsize=10, color=colors[i])
    
    # ---------------- 针对 rho=0.45 的特定计算 ----------------
    if rho == 0.45:
        # 记录最小方差组合的年化波动率
        result['mvp_vol_at_rho45'] = mvp_vol
        
        # 求解目标期望收益 10% 下的权重
        w1_target = (target_return - mu[1]) / (mu[0] - mu[1])
        w2_target = 1 - w1_target
        
        # 计算该目标收益下的最小年化波动率
        target_var = w1_target**2 * cov[0,0] + w2_target**2 * cov[1,1] + 2 * w1_target * w2_target * cov[0,1]
        target_vol = np.sqrt(target_var)
        result['frontier_vol_at_target'] = target_vol

# ==================== 3. 图形格式设定与保存 ====================
ax.set_xlabel('Volatility (Annualized)', fontsize=12)
ax.set_ylabel('Expected Return (Annualized)', fontsize=12)
ax.set_title('Mean-Variance Frontier for Different Correlations', fontsize=14)
ax.legend(fontsize=11)
ax.grid(True, linestyle='--', alpha=0.6)

# 保存图形
fig_path = 'mean_variance_frontier.png'
plt.savefig(fig_path, dpi=300, bbox_inches='tight')
plt.close()

result['figure_path'] = fig_path

# 输出结果确认
print(result)
