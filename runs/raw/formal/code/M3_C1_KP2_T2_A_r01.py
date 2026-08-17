import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# ================= 可调参数 =================
rf = 0.023        # 无风险利率 (可修改)
rm = 0.094        # 市场期望收益 (可修改)
# ===========================================

# 1. 计算SML斜率（市场风险溢价）
sml_slope = rm - rf

# 2. 计算beta=1.27对应的期望收益
beta_target = 1.27
er_at_beta_127 = rf + beta_target * sml_slope

# 3. 绘制证券市场线(SML)
betas = [0, 2]
ers = [rf + b * sml_slope for b in betas]

fig, ax = plt.subplots(figsize=(9, 6))
ax.plot(betas, ers, label='SML', color='blue', linewidth=2, zorder=1)

# 4. 标注三个资产点
points = {
    'X': (0.62, 0.081),
    'Y': (1.18, 0.131),
    'Z': (1.51, 0.099)
}

for name, (b, e) in points.items():
    ax.scatter(b, e, color='red', s=60, zorder=2)
    # 标注文本稍微偏移以防遮挡
    ax.annotate(f'{name} ($\\beta$={b}, E(r)={e:.1%})', 
                (b, e), 
                textcoords="offset points", 
                xytext=(12, 12), 
                ha='center',
                arrowprops=dict(arrowstyle='->', color='gray', lw=1.2))

# 格式化图表外观
ax.yaxis.set_major_formatter(mticker.PercentFormatter(decimals=1))
ax.set_xlabel('Beta ($\\beta$)', fontsize=12)
ax.set_ylabel('Expected Return E(r)', fontsize=12)
ax.set_title(f'Security Market Line (SML)\n$R_f$={rf:.1%}, $E(R_M)$={rm:.1%}', fontsize=14)
ax.grid(True, linestyle='--', alpha=0.6)
ax.legend(fontsize=11)

# 设定坐标轴范围更美观
ax.set_xlim(-0.05, 2.05)
ax.set_ylim(0, max(0.155, max(p[1] for p in points.values()) + 0.03))

# 5. 保存图片
figure_path = 'sml_plot.png'
plt.savefig(figure_path, dpi=300, bbox_inches='tight')
plt.close()

# 6. 构造输出契约字典
result = {
    'sml_slope': sml_slope,
    'er_at_beta_127': er_at_beta_127,
    'figure_path': figure_path
}
