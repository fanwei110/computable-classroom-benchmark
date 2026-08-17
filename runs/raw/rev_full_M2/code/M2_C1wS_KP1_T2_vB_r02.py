import numpy as np
import matplotlib.pyplot as plt

# ------------------ 资产参数 ------------------
r1, r2 = 0.071, 0.124      # 期望收益
s1, s2 = 0.163, 0.289      # 波动率（标准差）
rhos = [0.15, 0.45, 0.75]  # 三种相关系数

# ------------------ 全局绘图设置 ------------------
plt.figure(figsize=(8, 6))
w1_range = np.linspace(-1, 2, 3000)  # 足够覆盖所有最小方差组合

# 用于保存结果
mvp_vol_at_rho45 = None
frontier_vol_at_target = None

# ------------------ 循环每个相关系数 ------------------
for rho in rhos:
    # 协方差与方差
    cov12 = rho * s1 * s2
    var1, var2 = s1 ** 2, s2 ** 2

    # 扫描组合的风险与收益
    rets = w1_range * r1 + (1 - w1_range) * r2
    variances = (w1_range ** 2 * var1
                 + (1 - w1_range) ** 2 * var2
                 + 2 * w1_range * (1 - w1_range) * cov12)
    stds = np.sqrt(variances)

    # 画出前沿散点（点极小，连成曲线）
    plt.plot(stds, rets, '.', markersize=1, label=f'ρ = {rho}')

    # ----- 全局最小方差组合（解析解）-----
    w1_mvp = (var2 - cov12) / (var1 + var2 - 2 * cov12)
    w2_mvp = 1 - w1_mvp
    mvp_ret = w1_mvp * r1 + w2_mvp * r2
    mvp_var = (w1_mvp ** 2 * var1
               + w2_mvp ** 2 * var2
               + 2 * w1_mvp * w2_mvp * cov12)
    mvp_std = np.sqrt(mvp_var)

    # 在曲线上标出最小方差组合
    plt.scatter(mvp_std, mvp_ret, marker='*', s=150, zorder=5)

    # 针对 ρ = 0.45 保存所需结果
    if rho == 0.45:
        mvp_vol_at_rho45 = mvp_std

        # 目标收益 10% 时的最小波动率
        target_ret = 0.10
        # 满仓约束下，收益10%对应的唯一权重
        w1_target = (r2 - target_ret) / (r2 - r1)
        w2_target = 1 - w1_target
        target_var = (w1_target ** 2 * var1
                      + w2_target ** 2 * var2
                      + 2 * w1_target * w2_target * cov12)
        frontier_vol_at_target = np.sqrt(target_var)

# ------------------ 图形美化与保存 ------------------
plt.xlabel('Portfolio Standard Deviation', fontsize=12)
plt.ylabel('Portfolio Expected Return', fontsize=12)
plt.title('Efficient Frontiers with Different Correlations', fontsize=14)
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()

figure_path = 'efficient_frontier.png'
plt.savefig(figure_path, dpi=150)
plt.close()

# ------------------ 输出结果 ------------------
result = {
    'mvp_vol_at_rho45': mvp_vol_at_rho45,
    'frontier_vol_at_target': frontier_vol_at_target,
    'figure_path': figure_path
}

# 课堂演示时可打印查看
print(result)
