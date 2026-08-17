import numpy as np
import matplotlib.pyplot as plt

# ============================
# 资产参数（小数表示）
# ============================
mu1 = 0.071      # 资产1期望年收益
mu2 = 0.124      # 资产2期望年收益
sigma1 = 0.163   # 资产1年化波动率
sigma2 = 0.289   # 资产2年化波动率
rhos = [0.15, 0.45, 0.75]   # 三种相关系数

# 权重扫描范围（允许卖空、满仓）
w1_range = np.linspace(-3, 4, 200000)   # 资产1权重
w2_range = 1 - w1_range

# 绘图颜色与标记风格
colors = ['tab:blue', 'tab:orange', 'tab:green']
markers = ['o', 's', 'D']

# ============================
# 结果字典
# ============================
result = {}

# 创建画布
fig, ax = plt.subplots(figsize=(10, 7))

# 逐个相关系数计算并绘图
for i, rho in enumerate(rhos):
    # ---- 构造协方差矩阵 ----
    cov = np.array([[sigma1**2, rho * sigma1 * sigma2],
                    [rho * sigma1 * sigma2, sigma2**2]])
    inv_cov = np.linalg.inv(cov)
    ones = np.ones(2)
    mu_vec = np.array([mu1, mu2])

    # ---- 解析公式所需中间量 ----
    A = mu_vec @ inv_cov @ mu_vec
    B = mu_vec @ inv_cov @ ones
    C = ones @ inv_cov @ ones
    D = A * C - B**2

    # ---- 最小方差组合 (MVP) 解析解 ----
    mu_mvp = B / C
    sigma_mvp = np.sqrt(1.0 / C)

    # ---- 权重扫描：生成所有允许的（波动率，收益）组合 ----
    mu_p = w1_range * mu1 + w2_range * mu2
    var_p = (w1_range**2) * (sigma1**2) + \
            (w2_range**2) * (sigma2**2) + \
            2 * w1_range * w2_range * rho * sigma1 * sigma2
    sigma_p = np.sqrt(var_p)

    # 按期望收益排序，使曲线连续
    sort_idx = np.argsort(mu_p)
    mu_sorted = mu_p[sort_idx]
    sigma_sorted = sigma_p[sort_idx]

    # ---- 绘制均值-方差前沿 ----
    ax.plot(sigma_sorted, mu_sorted, color=colors[i], label=f'ρ = {rho}')
    # 标出最小方差组合
    ax.scatter(sigma_mvp, mu_mvp, color=colors[i], marker=markers[i],
               edgecolors='black', zorder=5, s=80)

    # ---- 特定相关系数 0.45 的题目要求 ----
    if rho == 0.45:
        result['mvp_vol_at_rho45'] = sigma_mvp         # 最小方差组合年化波动率
        target_mu = 0.10                               # 目标期望收益 10%
        # 有效前沿方差公式
        var_target = (C * target_mu**2 - 2 * B * target_mu + A) / D
        sigma_target = np.sqrt(var_target)
        result['frontier_vol_at_target'] = sigma_target

# ============================
# 图形装饰与保存
# ============================
ax.set_xlabel('Annualized Volatility (σ)', fontsize=12)
ax.set_ylabel('Expected Return (μ)', fontsize=12)
ax.set_title('Mean–Variance Frontier (Two Risky Assets, Short-Selling Allowed)', fontsize=14)
ax.legend(fontsize=10)
ax.grid(True, linestyle='--', alpha=0.5)
ax.set_xlim(0, 0.6)
ax.set_ylim(0, 0.25)
plt.tight_layout()

figure_path = 'frontier.png'
plt.savefig(figure_path, dpi=150)
plt.close()

result['figure_path'] = figure_path

# 打印结果供课堂核对
print(result)
