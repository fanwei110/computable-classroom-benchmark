import matplotlib
matplotlib.use('Agg') # 使用非交互式后端，确保保存文件时不弹出窗口
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

# ==========================================
# 可调参数
# ==========================================
rf = 0.023  # 无风险利率 2.3%
rm = 0.094  # 市场期望收益 9.4%

# ==========================================
# 股票数据
# ==========================================
stocks = {
    'X': {'beta': 0.62, 'return': 0.081},
    'Y': {'beta': 1.18, 'return': 0.131},
    'Z': {'beta': 1.51, 'return': 0.099}
}

# ==========================================
# 核心计算
# ==========================================
# SML斜率即为市场风险溢价
sml_slope = rm - rf

# Beta = 1.27 处的 CAPM 期望收益
beta_target = 1.27
er_at_beta_127 = rf + beta_target * sml_slope

# ==========================================
# 绘图
# ==========================================
# 生成 Beta 从 0 到 2 的数据
betas = np.linspace(0, 2, 200)
sml_returns = rf + betas * sml_slope

plt.figure(figsize=(10, 6))
# 画出证券市场线
plt.plot(betas, sml_returns, label='Security Market Line (SML)', color='blue', linewidth=2)

# 画出无风险利率和市场组合的参考点
plt.scatter(0, rf, color='black', zorder=5)
plt.annotate(f'Rf = {rf*100:.1f}%', xy=(0, rf), xytext=(10, -10), textcoords='offset points')
plt.scatter(1, rm, color='black', zorder=5)
plt.annotate(f'Market = {rm*100:.1f}%', xy=(1, rm), xytext=(10, 5), textcoords='offset points')

# 设置股票标注的颜色和偏移量以防重叠
colors = {'X': 'red', 'Y': 'green', 'Z': 'purple'}
offsets = {'X': (15, 10), 'Y': (15, 10), 'Z': (15, -25)}

# 画出股票 X, Y, Z 并标注
for name, data in stocks.items():
    plt.scatter(data['beta'], data['return'], color=colors[name], zorder=5, s=60, label=f"Stock {name}")
    plt.annotate(
        f"Stock {name}\n(β={data['beta']}, R={data['return']*100:.1f}%)",
        xy=(data['beta'], data['return']),
        xytext=offsets[name],
        textcoords='offset points',
        arrowprops=dict(arrowstyle='->', color=colors[name], lw=1.5),
        fontsize=10,
        color=colors[name],
        bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=colors[name], alpha=0.8)
    )

# 格式化图表
plt.title('Security Market Line (SML) with Stocks X, Y, Z', fontsize=14)
plt.xlabel('Beta (β)', fontsize=12)
plt.ylabel('Expected Return', fontsize=12)
plt.gca().yaxis.set_major_formatter(PercentFormatter(1.0, decimals=1))
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend(loc='upper left')
plt.xlim(0, 2)
plt.ylim(0, 0.18)

# 保存图表
figure_path = 'sml_plot.png'
plt.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close()

# ==========================================
# 输出契约
# ==========================================
result = {
    'sml_slope': sml_slope,
    'er_at_beta_127': er_at_beta_127,
    'figure_path': figure_path
}

# 打印结果以供验证
print(result)
