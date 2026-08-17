import matplotlib.pyplot as plt
import os

# ==========================================
# 可调参数 (上课时可随时修改这里)
# ==========================================
rf = 2.3       # 无风险利率 (%)
rm = 9.4       # 市场期望收益 (%)

# 给定的三个资产点
points = {
    'X': (0.62, 8.1),
    'Y': (1.18, 13.1),
    'Z': (1.51, 9.9)
}

# ==========================================
# 核心计算
# ==========================================
# 1. 计算SML斜率 (以小数形式存储)
sml_slope = (rm - rf) / 100  # 0.071

# 2. 计算 Beta = 1.27 时的期望收益 (以小数形式存储)
beta_target = 1.27
er_at_beta_127 = (rf + beta_target * (rm - rf)) / 100  # 0.11317

# ==========================================
# 绘制证券市场线 (SML)
# ==========================================
plt.rcParams['font.sans-serif'] = ['SimHei']  # 解决中文显示问题
plt.rcParams['axes.unicode_minus'] = False    # 正常显示负号

fig, ax = plt.subplots(figsize=(10, 7))

# Beta 范围: 0 到 2
betas = [0, 2]
sml_ers = [rf, rf + 2 * (rm - rf)]

# 绘制 SML 线
ax.plot(betas, sml_ers, label='证券市场线 (SML)', color='blue', linewidth=2, marker='o', markersize=4)

# 标注无风险利率点和市场组合点
ax.scatter(0, rf, color='black', zorder=5)
ax.text(0, rf, f'  $r_f$ = {rf}%', verticalalignment='bottom', fontsize=11)

ax.scatter(1, rm, color='black', zorder=5)
ax.text(1, rm, f'  市场组合 $M$ = {rm}%', verticalalignment='bottom', fontsize=11)

# 标注三个资产点 X, Y, Z
for label, (b, er) in points.items():
    ax.scatter(b, er, color='red', zorder=5, s=60)
    # 判断点在SML上方还是下方，智能调整文本位置避免重叠
    sml_er_at_b = rf + b * (rm - rf)
    offset = 15 if er > sml_er_at_b else -18
    ax.text(b, er, f'  {label}({b}, {er}%)', verticalalignment='bottom' if er > sml_er_at_b else 'top', 
            fontsize=11, color='red', fontweight='bold',
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='none', pad=1))

# 坐标轴与网格设置
ax.set_xlabel('Beta ($\\beta$)', fontsize=13)
ax.set_ylabel('期望收益 $E(r)$ (%)', fontsize=13)
ax.set_title('证券市场线 (SML) 与资产定价偏差', fontsize=15)
ax.grid(True, linestyle='--', alpha=0.6)
ax.set_xlim(-0.1, 2.2)
ax.set_ylim(0, 18)

# 保存图片
figure_path = 'sml_plot.png'
plt.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close()

# ==========================================
# 封装输出结果
# ==========================================
result = {
    'sml_slope': sml_slope,         # 0.071
    'er_at_beta_127': er_at_beta_127, # 0.11317
    'figure_path': figure_path       # 'sml_plot.png'
}

print(result)
