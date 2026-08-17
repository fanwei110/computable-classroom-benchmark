import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

# ============================================================
# 参数设定
# ============================================================
r1 = 0.071      # 资产1期望年收益
r2 = 0.124      # 资产2期望年收益
vol1 = 0.163    # 资产1年化波动率
vol2 = 0.289    # 资产2年化波动率
rhos = [0.15, 0.45, 0.75]   # 需要绘制的三个相关系数
target_return = 0.10        # 目标期望收益 10%

# 权重扫描范围（允许卖空、满仓 w1 + w2 = 1）
w1_range = np.linspace(-2.0, 3.0, 5000)

# ============================================================
# 准备绘图
# ============================================================
fig, ax = plt.subplots(figsize=(10, 7))

# 用于保存结果的字典
result = {}

# 颜色映射
colors = ['#1f77b4', '#ff7f0e', '#2ca02c']

# ============================================================
# 逐相关系数计算并绘制前沿
# ============================================================
for i, rho in enumerate(rhos):
    # 协方差与协方差矩阵（此处只需要协方差值 cov12）
    cov12 = rho * vol1 * vol2

    # 扫描组合权重计算期望收益与波动率
    w2_range = 1.0 - w1_range
    port_ret = w1_range * r1 + w2_range * r2
    port_vol = np.sqrt(
        w1_range**2 * vol1**2
        + w2_range**2 * vol2**2
        + 2 * w1_range * w2_range * cov12
    )

    # 绘制均值-方差前沿（整条曲线）
    ax.plot(port_vol, port_ret,
            color=colors[i], linewidth=1.5,
            label=f'ρ = {rho:.2f}')

    # --------------------------------------------------------
    # 计算该相关系数下的最小方差组合（MVP）
    # --------------------------------------------------------
    # 最小方差组合权重（解析解）
    w1_mvp = (vol2**2 - cov12) / (vol1**2 + vol2**2 - 2 * cov12)
    w2_mvp = 1.0 - w1_mvp
    mvp_ret = w1_mvp * r1 + w2_mvp * r2
    mvp_vol = np.sqrt(
        w1_mvp**2 * vol1**2
        + w2_mvp**2 * vol2**2
        + 2 * w1_mvp * w2_mvp * cov12
    )

    # 在曲线上标出MVP点（同色，稍大标记）
    ax.scatter(mvp_vol, mvp_ret,
               color=colors[i], marker='o', s=80,
               edgecolors='black', zorder=5)

    # 若相关系数为 0.45，保存MVP波动率至结果
    if rho == 0.45:
        result['mvp_vol_at_rho45'] = mvp_vol

# ============================================================
# 计算相关系数 0.45 时，目标收益 10% 下的最小年化波动率
# ============================================================
rho_target = 0.45
cov12_target = rho_target * vol1 * vol2
# 给定目标收益下的组合权重（满仓，允许卖空）
w1_target = (target_return - r2) / (r1 - r2)
w2_target = 1.0 - w1_target
frontier_vol_target = np.sqrt(
    w1_target**2 * vol1**2
    + w2_target**2 * vol2**2
    + 2 * w1_target * w2_target * cov12_target
)
result['frontier_vol_at_target'] = frontier_vol_target

# ============================================================
# 图表装饰与保存
# ============================================================
ax.set_xlabel('Annualized Volatility')
ax.set_ylabel('Expected Return')
ax.set_title('Mean-Variance Frontier for Different Correlations')
ax.legend(loc='upper left')
ax.grid(True, linestyle='--', alpha=0.7)

# 将坐标轴格式化为百分比（数据本身为小数）
ax.xaxis.set_major_formatter(PercentFormatter(1.0, decimals=0))
ax.yaxis.set_major_formatter(PercentFormatter(1.0, decimals=0))

# 适当调整坐标轴显示范围，使图形美观
ax.set_xlim(left=0.0)
ax.set_ylim(bottom=0.0)

# 保存图片
figure_filename = 'frontier_plot.png'
plt.savefig(figure_filename, dpi=150, bbox_inches='tight')
plt.close()

result['figure_path'] = figure_filename

# ============================================================
# 输出结果（教师运行时会直接看到）
# ============================================================
print("结果字典 result：")
for k, v in result.items():
    print(f"  {k}: {v}")
