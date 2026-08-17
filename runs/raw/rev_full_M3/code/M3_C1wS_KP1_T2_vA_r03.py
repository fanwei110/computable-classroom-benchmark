import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 马科维茨均值-方差组合理论 - 课堂演示代码
# ==========================================

# 1. 基础参数设定
mu = np.array([0.071, 0.124])      # 期望年收益
sigma = np.array([0.163, 0.289])   # 年化波动率
rhos = [0.15, 0.45, 0.75]         # 相关系数列表

# 2. 辅助函数定义
def get_cov_matrix(rho):
    """根据相关系数构造协方差矩阵"""
    return np.array([[sigma[0]**2, rho * sigma[0] * sigma[1]],
                     [rho * sigma[0] * sigma[1], sigma[1]**2]])

def port_ret(w1):
    """计算组合期望收益（w1为资产1的权重，满仓约束下w2=1-w1）"""
    return w1 * mu[0] + (1 - w1) * mu[1]

def port_vol(w1, cov):
    """计算组合波动率（标量输入，用于解析精确求解）"""
    w = np.array([w1, 1 - w1])
    return np.sqrt(w.T @ cov @ w)

# 3. 权重扫描与前沿绘制
# 假设允许卖空，扫描范围设为[-0.5, 1.5]以展现完整的双曲线
w1_scan = np.linspace(-0.5, 1.5, 1000)

fig, ax = plt.subplots(figsize=(10, 7))
colors = ['tab:blue', 'tab:orange', 'tab:green']

for i, rho in enumerate(rhos):
    cov = get_cov_matrix(rho)
    
    # 向量化计算扫描权重下的收益与波动率
    w_vec = np.array([w1_scan, 1 - w1_scan])
    vols = np.sqrt(np.sum(w_vec * (cov @ w_vec), axis=0))
    rets = port_ret(w1_scan)
    
    # 计算解析的最小方差组合(MVP)
    # 对 w'Σw 求导令其等于0，解得两资产下MVP权重w1的解析解
    w1_mvp = (sigma[1]**2 - rho * sigma[0] * sigma[1]) / \
             (sigma[0]**2 + sigma[1]**2 - 2 * rho * sigma[0] * sigma[1])
    mvp_ret = port_ret(w1_mvp)
    mvp_vol = port_vol(w1_mvp, cov)
    
    # 区分有效前沿（上半支，实线）与无效前沿（下半支，虚线）
    eff_mask = rets >= mvp_ret
    ineff_mask = rets < mvp_ret
    
    ax.plot(vols[eff_mask], rets[eff_mask], color=colors[i], lw=2, 
            label=r'$\rho = {:.2f}$'.format(rho))
    ax.plot(vols[ineff_mask], rets[ineff_mask], color=colors[i], lw=2, 
            ls='--', alpha=0.5)
    
    # 在每条曲线上标出最小方差组合点
    ax.scatter(mvp_vol, mvp_ret, marker='*', s=300, zorder=5, 
               color=colors[i], edgecolors='black', linewidths=0.5)

# 增加MVP图例说明
ax.scatter([], [], marker='*', color='grey', s=150, label='Minimum Variance Portfolio')

# 4. 特定问题计算 (rho = 0.45)
rho_45 = 0.45
cov_45 = get_cov_matrix(rho_45)

# 计算 rho=0.45 时的最小方差组合
w1_mvp_45 = (sigma[1]**2 - rho_45 * sigma[0] * sigma[1]) / \
            (sigma[0]**2 + sigma[1]**2 - 2 * rho_45 * sigma[0] * sigma[1])
mvp_vol_45 = port_vol(w1_mvp_45, cov_45)

# 计算 rho=0.45 时目标收益10%的最小波动率
# 两资产下，实现目标收益的权重是唯一确定的
target_ret = 0.10
w1_target = (mu[1] - target_ret) / (mu[1] - mu[0])
target_vol = port_vol(w1_target, cov_45)

# 5. 图形美化与保存
ax.set_xlabel('Annualized Volatility', fontsize=12)
ax.set_ylabel('Annualized Expected Return', fontsize=12)
ax.set_title('Markowitz Mean-Variance Frontier', fontsize=14)
ax.legend(fontsize=11)
ax.grid(True, linestyle='--', alpha=0.6)

fig_path = 'efficient_frontier.png'
fig.savefig(fig_path, dpi=150, bbox_inches='tight')
plt.close(fig)

# 6. 填充输出契约
result = {
    'mvp_vol_at_rho45': mvp_vol_45,
    'frontier_vol_at_target': target_vol,
    'figure_path': fig_path
}

# 课堂输出互动打印
print(f"ρ=0.45 时最小方差组合的波动率: {mvp_vol_45:.4f} (即 {mvp_vol_45*100:.2f}%)")
print(f"ρ=0.45 时目标收益10%的最小波动率: {target_vol:.4f} (即 {target_vol*100:.2f}%)")
print("计算结果字典 result:", result)
