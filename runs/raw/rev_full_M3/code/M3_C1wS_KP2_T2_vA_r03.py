import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# ==========================================
# 1. 参数化设置 (教师可在此处直接调参)
# ==========================================
rf = 0.023   # 无风险利率 2.3%
rm = 0.094   # 市场期望收益 9.4%

# ==========================================
# 2. 计算核心指标
# ==========================================
# SML斜率即为市场风险溢价
sml_slope = rm - rf

# 计算beta=1.27时的期望收益
beta_target = 1.27
er_at_beta_127 = rf + beta_target * sml_slope

# ==========================================
# 3. 绘制证券市场线 (SML)
# ==========================================
# 生成SML线条数据
beta_range = np.linspace(0, 2, 100)
sml_er_range = rf + beta_range * sml_slope

# 三只股票的给定数据
stocks = {
    'X': (0.62, 0.081),
    'Y': (1.18, 0.131),
    'Z': (1.51, 0.099)
}

# 创建画布
fig, ax = plt.subplots(figsize=(10, 6))

# 画SML线
ax.plot(beta_range, sml_er_range, label='Security Market Line (SML)', 
        color='blue', linewidth=2.5, zorder=2)

# 标出三只股票的点并标注 (偏离SML的部分即为Alpha)
colors = {'X': 'green', 'Y': 'orange', 'Z': 'red'}
# 调整标注位置以防重叠，确保课堂投屏清晰
offsets = {'X': (10, 15), 'Y': (-100, 15), 'Z': (-100, -25)}

for label, (b, e) in stocks.items():
    ax.scatter(b, e, color=colors[label], zorder=5, s=80, label=f'Stock {label}')
    ax.annotate(f'{label} ($\\beta$={b}, E={e:.1%})',
                xy=(b, e),
                xytext=offsets[label],
                textcoords='offset points',
                fontsize=11,
                arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=5))

# 格式化图表
ax.set_title(f'Security Market Line (SML)\n$R_f$={rf:.1%}, $E(R_m)$={rm:.1%}, Slope={sml_slope:.2%}', fontsize=14)
ax.set_xlabel('Beta ($\\beta$)', fontsize=12)
ax.set_ylabel('Expected Return ($E(R)$)', fontsize=12)

# Y轴显示为百分比
ax.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=1, decimals=1))
# X轴刻度
ax.xaxis.set_major_locator(mticker.MultipleLocator(0.2))

ax.set_xlim(0, 2)
ax.set_ylim(0, 0.18) # 0% 到 18%，留足视觉空间
ax.grid(True, linestyle='--', alpha=0.6)
ax.legend(loc='upper left', fontsize=10)

# ==========================================
# 4. 保存图形并输出结果
# ==========================================
figure_path = 'sml_plot.png'
fig.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close()

# 将结果存入字典
result = {
    'sml_slope': sml_slope,
    'er_at_beta_127': er_at_beta_127,
    'figure_path': figure_path
}

# 课堂投屏打印展示
print(f"--- 课堂计算结果 ---")
print(f"SML 斜率 (市场风险溢价): {sml_slope:.4f} ({sml_slope:.2%})")
print(f"Beta = 1.27 时的期望收益 : {er_at_beta_127:.4f} ({er_at_beta_127:.2%})")
print(f"图形已保存至: {figure_path}")
print(f"\nresult 字典内容: {result}")
