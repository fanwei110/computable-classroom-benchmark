import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as mtick

# ==========================================
# 上课调参区域：修改这里的数值即可
# ==========================================
rf = 0.023      # 无风险利率
rm = 0.094      # 市场期望收益 (E(Rm))

# ==========================================
# 计算核心指标
# ==========================================
sml_slope = rm - rf
beta_target = 1.27
er_at_beta_127 = rf + beta_target * sml_slope

# ==========================================
# 绘制证券市场线 (SML)
# ==========================================
# 生成Beta从0到2的序列
betas = np.linspace(0, 2, 100)
# SML公式: E(R) = rf + β * (rm - rf)
er_sml = rf + betas * sml_slope

plt.figure(figsize=(10, 7))

# 绘制SML直线
plt.plot(betas, er_sml, color='blue', linewidth=2, label='SML (Security Market Line)')

# 标出市场组合点 M (Beta=1, E(R)=rm)
plt.scatter(1, rm, color='blue', s=80, zorder=5)
plt.annotate('M (Market)\n(1.00, 9.4%)', (1, rm), textcoords="offset points", xytext=(10, -15), fontsize=10)

# 标出无风险利率点 F (Beta=0, E(R)=rf)
plt.scatter(0, rf, color='blue', s=80, zorder=5)
plt.annotate(f'rf (Risk-free)\n(0, {rf*100:.1f}%)', (0, rf), textcoords="offset points", xytext=(10, 5), fontsize=10)

# 绘制题目要求的三个点 X, Y, Z
points = {
    'X': (0.62, 0.081),
    'Y': (1.18, 0.131),
    'Z': (1.51, 0.099)
}

colors = {'X': 'red', 'Y': 'green', 'Z': 'purple'}
for name, (b, r) in points.items():
    plt.scatter(b, r, color=colors[name], s=100, zorder=5, marker='o')
    # 标注点，稍微偏移避免遮挡
    plt.annotate(f'{name} ({b}, {r*100:.1f}%)', (b, r), textcoords="offset points", 
                 xytext=(10, 10 if r > rf + b*sml_slope else -20), 
                 fontsize=11, fontweight='bold', color=colors[name])

# 绘制辅助虚线（从X轴到M点，以及Y轴的rf）
plt.axhline(y=rf, color='grey', linestyle='--', linewidth=0.8)
plt.axvline(x=1, color='grey', linestyle='--', linewidth=0.8)

# 设置图表格式
plt.title('Security Market Line (SML)', fontsize=16)
plt.xlabel('Beta (β)', fontsize=13)
plt.ylabel('Expected Return E(R)', fontsize=13)
plt.xlim(0, 2)
plt.ylim(0, 0.18) # 留出足够空间显示Y点

# Y轴显示为百分比
plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(1.0))

plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(fontsize=12)
plt.tight_layout()

# 保存图片
figure_path = 'sml_plot.png'
plt.savefig(figure_path, dpi=300)
plt.close()

# ==========================================
# 按照输出契约生成结果字典
# ==========================================
result = {
    'sml_slope': sml_slope,           # 0.071
    'er_at_beta_127': er_at_beta_127, # 0.11317
    'figure_path': figure_path
}

# 打印结果供查看
print(f"SML斜率: {sml_slope:.4f} (即 {sml_slope*100:.1f}%)")
print(f"Beta=1.27时的期望收益: {er_at_beta_127:.5f} (即 {er_at_beta_127*100:.3f}%)")
print(f"结果字典: {result}")
