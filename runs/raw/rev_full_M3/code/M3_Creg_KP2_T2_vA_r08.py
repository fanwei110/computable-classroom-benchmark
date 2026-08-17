import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 可调参数
# ==========================================
risk_free_rate = 0.023      # 无风险利率 2.3%
market_expected_return = 0.094  # 市场期望收益 9.4%

# ==========================================
# 核心计算
# ==========================================
# SML 斜率 = 市场期望收益 - 无风险利率
sml_slope = market_expected_return - risk_free_rate

# beta = 1.27 处的 CAPM 期望收益
beta_target = 1.27
er_at_beta_127 = risk_free_rate + beta_target * sml_slope

# 股票数据
stocks = {
    'X': {'beta': 0.62, 'return': 0.081},
    'Y': {'beta': 1.18, 'return': 0.131},
    'Z': {'beta': 1.51, 'return': 0.099}
}

# ==========================================
# 绘制证券市场线 (SML)
# ==========================================
betas = np.linspace(0, 2, 200)
expected_returns = risk_free_rate + betas * sml_slope

fig, ax = plt.subplots(figsize=(10, 6))

# 绘制 SML 直线
ax.plot(betas, expected_returns, label='Security Market Line (SML)', color='blue', linewidth=2)

# 绘制并标注股票 X, Y, Z
# 设置标注偏移量以避免重叠
offsets = {
    'X': (15, -20),
    'Y': (15, 15),
    'Z': (-90, -25)
}
colors = {
    'X': 'red',
    'Y': 'green',
    'Z': 'purple'
}

for name, data in stocks.items():
    ax.scatter(data['beta'], data['return'], color=colors[name], zorder=5, label=f'Stock {name}')
    ax.annotate(
        f"{name} (β={data['beta']}, R={data['return']*100:.1f}%)",
        xy=(data['beta'], data['return']),
        xytext=offsets[name],
        textcoords='offset points',
        arrowprops=dict(arrowstyle='->', color=colors[name]),
        color=colors[name],
        fontweight='bold'
    )

# 图表格式设置
ax.set_xlabel('Beta', fontsize=12)
ax.set_ylabel('Expected Return', fontsize=12)
ax.set_title(f'Security Market Line (Rf={risk_free_rate*100:.1f}%, Rm={market_expected_return*100:.1f}%)', fontsize=14)
ax.axhline(0, color='black', linewidth=0.5)
ax.axvline(0, color='black', linewidth=0.5)
ax.legend()
ax.grid(True, linestyle='--', alpha=0.7)

# 将 Y 轴刻度格式化为百分比
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y*100:.1f}%'))

# 保存图表
figure_path = 'sml_plot.png'
fig.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close(fig)

# ==========================================
# 输出契约
# ==========================================
result = {
    'sml_slope': sml_slope,
    'er_at_beta_127': er_at_beta_127,
    'figure_path': figure_path
}
