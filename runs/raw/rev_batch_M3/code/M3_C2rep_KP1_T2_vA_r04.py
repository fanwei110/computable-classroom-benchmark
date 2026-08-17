import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 1. 定义基本参数
# ==========================================
mu = np.array([0.071, 0.124])       # 期望年收益
sigma = np.array([0.163, 0.289])    # 年化波动率
rhos = [0.15, 0.45, 0.75]          # 相关系数列表
target_return = 0.10                # 目标期望收益 (10%)

# 初始化结果字典
result = {}

# ==========================================
# 2. 绘图准备
# ==========================================
plt.figure(figsize=(10, 7))

# 遍历不同的相关系数
for rho in rhos:
    # 构造协方差矩阵
    cov_matrix = np.array([
        [sigma[0]**2, rho * sigma[0] * sigma[1]],
        [rho * sigma[0] * sigma[1], sigma[1]**2]
    ])
    
    # 在组合权重上扫描画出前沿 (允许卖空，权重范围设为-0.5到1.5)
    w1_scan = np.linspace(-0.5, 1.5, 1000)
    w2_scan = 1 - w1_scan
    weights_scan = np.vstack([w1_scan, w2_scan])
    
    # 计算前沿上的期望收益与波动率
    port_returns = weights_scan.T @ mu
    port_variances = np.diag(weights_scan.T @ cov_matrix @ weights_scan)
    port_vols = np.sqrt(port_variances)
    
    # 绘制均值-方差前沿曲线
    plt.plot(port_vols, port_returns, label=f'ρ = {rho}', linewidth=2)
    
    # 计算并标出最小方差组合
    # 两资产满仓约束下MVP解析解：w1 = (σ2^2 - cov12) / (σ1^2 + σ2^2 - 2*cov12)
    w1_mvp = (cov_matrix[1, 1] - cov_matrix[0, 1]) / (cov_matrix[0, 0] + cov_matrix[1, 1] - 2 * cov_matrix[0, 1])
    w_mvp = np.array([w1_mvp, 1 - w1_mvp])
    
    mvp_return = w_mvp @ mu
    mvp_vol = np.sqrt(w_mvp @ cov_matrix @ w_mvp)
    
    # 在图上标出最小方差组合
    plt.scatter(mvp_vol, mvp_return, marker='*', s=300, zorder=5, edgecolors='black', linewidths=1)
    
    # ==========================================
    # 3. 针对相关系数 0.45 计算所需的两个波动率
    # ==========================================
    if rho == 0.45:
        # 记录最小方差组合的年化波动率
        result['mvp_vol_at_rho45'] = mvp_vol
        
        # 目标期望收益10%下可达到的最小年化波动率
        # 两资产满仓约束下，达到特定期望收益的权重唯一：
        # w1_target = (target_return - mu2) / (mu1 - mu2)
        w1_target = (target_return - mu[1]) / (mu[0] - mu[1])
        w_target = np.array([w1_target, 1 - w1_target])
        
        target_vol = np.sqrt(w_target @ cov_matrix @ w_target)
        result['frontier_vol_at_target'] = target_vol

# ==========================================
# 4. 图形设置与保存
# ==========================================
plt.xlabel('Annualized Volatility', fontsize=12)
plt.ylabel('Expected Annual Return', fontsize=12)
plt.title('Mean-Variance Frontier under Different Correlations', fontsize=14)
plt.legend(fontsize=11)
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()

figure_path = 'markowitz_frontier.png'
plt.savefig(figure_path, dpi=300)

# 将图片路径存入result
result['figure_path'] = figure_path

# 打印最终结果以供查验
print("Result Dictionary:")
for key, value in result.items():
    if isinstance(value, float):
        print(f"{key}: {value:.6f} ({value*100:.4f}%)")
    else:
        print(f"{key}: {value}")
