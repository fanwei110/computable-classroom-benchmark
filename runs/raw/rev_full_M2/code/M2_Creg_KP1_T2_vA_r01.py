import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# ====================
# 基本参数设定
# ====================
r1 = 0.071          # 资产1期望年收益
r2 = 0.124          # 资产2期望年收益
s1 = 0.163          # 资产1年化波动率
s2 = 0.289          # 资产2年化波动率
rhos = [0.15, 0.45, 0.75]   # 需要绘制的相关系数
r_target = 0.10     # 目标期望收益 10%

# ====================
# 计算所需指标
# ====================
# 1) 相关系数 0.45 时最小方差组合（MVP）的年化波动率
rho45 = 0.45
cov45 = rho45 * s1 * s2
w1_mvp_45 = (s2**2 - cov45) / (s1**2 + s2**2 - 2 * cov45)
w2_mvp_45 = 1.0 - w1_mvp_45
mvp_vol_at_rho45 = np.sqrt(
    w1_mvp_45**2 * s1**2 + w2_mvp_45**2 * s2**2 +
    2 * w1_mvp_45 * w2_mvp_45 * cov45
)

# 2) 相关系数 0.45 时，目标期望收益 10% 的最小年化波动率
# 由于仅有两只资产且允许卖空、满仓，目标收益对应的权重唯一确定
w1_target = (r_target - r2) / (r1 - r2)
w2_target = 1.0 - w1_target
frontier_vol_at_target = np.sqrt(
    w1_target**2 * s1**2 + w2_target**2 * s2**2 +
    2 * w1_target * w2_target * cov45
)

# ====================
# 绘制均值-方差前沿
# ====================
fig, ax = plt.subplots(figsize=(10, 7))
colors = ['#1f77b4', '#ff7f0e', '#2ca02c']  # 蓝、橙、绿

# 生成一系列满仓组合（允许卖空，权重可任意）
w1_vals = np.linspace(-1.5, 2.5, 600)
w2_vals = 1.0 - w1_vals

for i, rho in enumerate(rhos):
    cov = rho * s1 * s2

    # 组合收益与波动率
    rp = w1_vals * r1 + w2_vals * r2
    vp = np.sqrt(
        w1_vals**2 * s1**2 + w2_vals**2 * s2**2 +
        2 * w1_vals * w2_vals * cov
    )

    # 绘制前沿曲线
    ax.plot(vp, rp, color=colors[i], label=f'ρ = {rho}', linewidth=1.8)

    # 计算并标注该相关系数下的最小方差组合（MVP）
    w1_mvp = (s2**2 - cov) / (s1**2 + s2**2 - 2 * cov)
    w2_mvp = 1.0 - w1_mvp
    r_mvp = w1_mvp * r1 + w2_mvp * r2
    v_mvp = np.sqrt(
        w1_mvp**2 * s1**2 + w2_mvp**2 * s2**2 +
        2 * w1_mvp * w2_mvp * cov
    )

    ax.scatter(v_mvp, r_mvp, color=colors[i], s=70, zorder=5, edgecolors='k', linewidth=0.5)
    # 标注“MVP”文字，避免重叠，微调偏移
    offset = 10 if i != 1 else -15  # 中间那条可微调
    ax.annotate('MVP', (v_mvp, r_mvp), textcoords="offset points",
                xytext=(0, offset), ha='center', fontsize=9,
                color=colors[i], fontweight='bold')

# 坐标轴格式化为百分比
ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{x*100:.1f}%'))
ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: f'{y*100:.1f}%'))

ax.set_xlabel('Annualized Volatility', fontsize=12)
ax.set_ylabel('Expected Return', fontsize=12)
ax.set_title('Mean-Variance Frontier for Two Risky Assets', fontsize=14)
ax.legend(fontsize=11)
ax.grid(True, alpha=0.3)

# 保存图像
figure_path = os.path.abspath('mean_variance_frontier.png')
plt.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close()

# ====================
# 输出结果字典
# ====================
result = {
    'mvp_vol_at_rho45': mvp_vol_at_rho45,
    'frontier_vol_at_target': frontier_vol_at_target,
    'figure_path': figure_path
}

# 可选：在控制台查看结果
print(result)
