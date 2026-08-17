import numpy as np
import matplotlib.pyplot as plt

# ==================== 参数设置 ====================
mu = np.array([0.071, 0.124])           # 期望年收益
sigma = np.array([0.163, 0.289])        # 年化波动率
rho_values = [0.15, 0.45, 0.75]         # 需要考察的相关系数
target_return = 0.10                    # 目标期望收益
w1_range = np.linspace(-2, 3, 5001)     # 资产1权重范围，足够覆盖完整前沿

# ==================== 初始化结果与画图 ====================
result = {}
plt.figure(figsize=(10, 6))

# ==================== 计算并绘制每个相关系数 ====================
for rho in rho_values:
    # 协方差矩阵及其逆
    cov12 = rho * sigma[0] * sigma[1]
    cov = np.array([[sigma[0]**2, cov12],
                    [cov12, sigma[1]**2]])
    inv_cov = np.linalg.inv(cov)
    ones = np.ones(2)

    # ----- 最小方差组合 (MVP) -----
    w_mvp = inv_cov @ ones / (ones @ inv_cov @ ones)
    mu_mvp = w_mvp @ mu
    vol_mvp = np.sqrt(w_mvp @ cov @ w_mvp)

    # 存储 rho=0.45 的结果
    if rho == 0.45:
        result['mvp_vol_at_rho45'] = vol_mvp

        # 用于目标收益计算的两基金分离参数
        A = ones @ inv_cov @ ones
        B = mu @ inv_cov @ ones
        C = mu @ inv_cov @ mu
        D = A * C - B**2
        var_target = (A * target_return**2 - 2 * B * target_return + C) / D
        vol_target = np.sqrt(var_target)
        result['frontier_vol_at_target'] = vol_target

    # ----- 生成均值-方差前沿曲线 -----
    # 权重：w1 为资产1比例，资产2比例为 1-w1
    ret = mu[1] + w1_range * (mu[0] - mu[1])   # 组合期望收益
    var = (w1_range**2 * sigma[0]**2 +
           (1 - w1_range)**2 * sigma[1]**2 +
           2 * w1_range * (1 - w1_range) * cov12)
    vol = np.sqrt(var)                         # 组合波动率

    # 绘制前沿线
    plt.plot(vol, ret, label=f'ρ = {rho}')

    # 在曲线上标出最小方差组合
    plt.scatter(vol_mvp, mu_mvp, marker='*', s=120,
                edgecolors='black', linewidths=0.6, zorder=5)

# ==================== 图形美化与保存 ====================
plt.xlabel('Annualized Volatility')
plt.ylabel('Expected Annual Return')
plt.title('Mean-Variance Frontier for Two Risky Assets')
plt.legend()
plt.grid(True, alpha=0.3)

figure_path = 'mean_variance_frontier.png'
plt.savefig(figure_path, dpi=150, bbox_inches='tight')
result['figure_path'] = figure_path

# ==================== 输出结果 ====================
print(result)
