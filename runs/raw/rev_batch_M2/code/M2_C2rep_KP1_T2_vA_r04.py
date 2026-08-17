import numpy as np
import matplotlib.pyplot as plt

# 参数设定
r = np.array([0.071, 0.124])            # 期望年收益
sigma = np.array([0.163, 0.289])        # 年化波动率
rhos = [0.15, 0.45, 0.75]               # 三个相关系数
colors = ['#1f77b4', '#ff7f0e', '#2ca02c']  # 曲线颜色（蓝、橙、绿）

# 扫描权重（允许卖空，w1 + w2 = 1）
w1_vals = np.linspace(-2.0, 3.0, 5000)  # 足够稠密以画出光滑曲线

# 结果字典
result = {}

# 绘图
plt.figure(figsize=(10, 6))
for i, rho in enumerate(rhos):
    color = colors[i]
    # 协方差矩阵
    cov12 = rho * sigma[0] * sigma[1]
    # 扫描组合的收益与波动率
    w2_vals = 1.0 - w1_vals
    port_ret = w1_vals * r[0] + w2_vals * r[1]
    port_var = (w1_vals**2 * sigma[0]**2 + w2_vals**2 * sigma[1]**2 +
                2 * w1_vals * w2_vals * cov12)
    port_vol = np.sqrt(port_var)
    # 画前沿曲线
    plt.plot(port_vol * 100, port_ret * 100, color=color, label=f'ρ = {rho}')

    # 最小方差组合 (MVP)
    w1_mvp = (sigma[1]**2 - cov12) / (sigma[0]**2 + sigma[1]**2 - 2 * cov12)
    w2_mvp = 1.0 - w1_mvp
    ret_mvp = w1_mvp * r[0] + w2_mvp * r[1]
    var_mvp = (w1_mvp**2 * sigma[0]**2 + w2_mvp**2 * sigma[1]**2 +
               2 * w1_mvp * w2_mvp * cov12)
    vol_mvp = np.sqrt(var_mvp)
    # 标记 MVP
    plt.scatter(vol_mvp * 100, ret_mvp * 100, color=color,
                marker='o', s=60, zorder=5, edgecolors='k', linewidth=0.5)

    # 对 ρ=0.45 保存所需数据
    if rho == 0.45:
        result['mvp_vol_at_rho45'] = vol_mvp            # 年化波动率（小数）
        # 目标期望收益 10% 下的最小波动率
        w1_target = (0.10 - r[1]) / (r[0] - r[1])       # 解满仓约束
        w2_target = 1.0 - w1_target
        var_target = (w1_target**2 * sigma[0]**2 + w2_target**2 * sigma[1]**2 +
                      2 * w1_target * w2_target * cov12)
        vol_target = np.sqrt(var_target)
        result['frontier_vol_at_target'] = vol_target   # 年化波动率（小数）

# 图形美化
plt.xlabel('Annualized Volatility (%)')
plt.ylabel('Expected Annual Return (%)')
plt.title('Mean-Variance Frontier under Different Correlations')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()

# 保存图形
fig_path = 'mean_variance_frontier.png'
plt.savefig(fig_path, dpi=150)
result['figure_path'] = fig_path

# 输出结果（供教师检查）
print(result)
plt.show()
