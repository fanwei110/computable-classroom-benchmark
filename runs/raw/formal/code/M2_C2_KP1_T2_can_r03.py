import numpy as np
import matplotlib.pyplot as plt
import pandas as pd  # 允许但不强依赖，仅用于满足导入要求

# ========== 参数设定 ==========
r1 = 0.071      # 资产1期望年收益
r2 = 0.124      # 资产2期望年收益
sigma1 = 0.163  # 资产1年化波动率
sigma2 = 0.289  # 资产2年化波动率
rhos = [0.15, 0.45, 0.75]           # 相关系数列表
target_return = 0.10                # 目标期望收益 10%

# ========== 扫描权重区间 ==========
# 覆盖所有可能的MVP权重（rho=0.75时MVP权重约1.22），因此取稍宽范围
w_vals = np.linspace(-2.0, 4.0, 6000)   # 6000个点保证曲线平滑

# 准备绘图
fig, ax = plt.subplots(figsize=(10, 7))

# 存储rho=0.45所需的结果
mvp_vol_rho45 = None
frontier_vol_target = None

# ========== 对每一个相关系数处理 ==========
for rho in rhos:
    # 协方差
    cov12 = rho * sigma1 * sigma2
    cov_matrix = np.array([[sigma1**2, cov12],
                           [cov12, sigma2**2]])

    # 组合收益与方差 (向量化计算)
    # w为资产1的权重，资产2权重为 1-w
    rp = r2 + w_vals * (r1 - r2)
    var_p = (w_vals**2 * sigma1**2 +
             (1 - w_vals)**2 * sigma2**2 +
             2 * w_vals * (1 - w_vals) * cov12)
    sigma_p = np.sqrt(var_p)

    # 绘制曲线
    ax.plot(sigma_p, rp, label=f'$\\rho = {rho}$', linewidth=1.5)

    # ---- 解析计算最小方差组合 (MVP) ----
    # 两资产满仓卖空下最小方差组合权重公式
    w_mvp = (sigma2**2 - cov12) / (sigma1**2 + sigma2**2 - 2 * cov12)
    r_mvp = w_mvp * r1 + (1 - w_mvp) * r2
    var_mvp = (w_mvp**2 * sigma1**2 +
               (1 - w_mvp)**2 * sigma2**2 +
               2 * w_mvp * (1 - w_mvp) * cov12)
    sigma_mvp = np.sqrt(var_mvp)

    # 在图上标出MVP
    ax.scatter(sigma_mvp, r_mvp, s=80,
               marker='o', edgecolors='black', linewidth=0.8,
               zorder=5, label=f'MVP $\\rho={rho}$')

    # 保存rho=0.45时的MVP波动率
    if rho == 0.45:
        mvp_vol_rho45 = sigma_mvp

# ========== 计算rho=0.45下目标收益10%的最小波动率 ==========
rho_target = 0.45
cov12_45 = rho_target * sigma1 * sigma2
# 满仓约束下目标收益对应的权重
w_target = (target_return - r2) / (r1 - r2)
# 该组合的方差与波动率（唯一确定，即为该收益下的最小波动率）
var_target = (w_target**2 * sigma1**2 +
              (1 - w_target)**2 * sigma2**2 +
              2 * w_target * (1 - w_target) * cov12_45)
sigma_target = np.sqrt(var_target)
frontier_vol_target = sigma_target

# ========== 图注与格式 ==========
ax.set_xlabel('Annualized Volatility (standard deviation)', fontsize=12)
ax.set_ylabel('Expected Annual Return', fontsize=12)
ax.set_title('Mean-Variance Frontiers for Two Risky Assets\n'
             '(Full investment, short sales allowed)', fontsize=14)
ax.legend(fontsize=10, loc='upper left')
ax.grid(True, linestyle='--', alpha=0.7)
# 将坐标轴显示为百分比格式（更直观）
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x*100:.0f}%'))
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y*100:.1f}%'))
plt.tight_layout()

# 保存图片
figure_filename = 'frontier.png'
plt.savefig(figure_filename, dpi=150, bbox_inches='tight')
plt.close()

# ========== 构建结果字典 ==========
result = {
    'mvp_vol_at_rho45': round(mvp_vol_rho45, 6),   # 保留足够精度
    'frontier_vol_at_target': round(frontier_vol_target, 6),
    'figure_path': figure_filename
}

# 输出结果供检查（课堂运行时会显示）
print("===== 计算结果 =====")
print(f"相关系数0.45时最小方差组合的年化波动率: {result['mvp_vol_at_rho45']:.4%}")
print(f"目标收益10%下可达到的最小年化波动率:   {result['frontier_vol_at_target']:.4%}")
print(f"图形已保存至: {result['figure_path']}")
print("result 字典内容:", result)
