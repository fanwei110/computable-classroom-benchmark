import matplotlib.pyplot as plt
import os

# ==========================================
# 可调参数（上课修改这里即可）
# ==========================================
rf = 0.023      # 无风险利率 (Risk-free rate)
erm = 0.094     # 市场期望收益 (Expected market return)

# ==========================================
# 计算核心指标
# ==========================================
# SML斜率 = 市场风险溢价
sml_slope = erm - rf

# Beta = 1.27 对应的期望收益
beta_target = 1.27
er_at_beta_127 = rf + beta_target * sml_slope

# ==========================================
# 绘制证券市场线 (SML)
# ==========================================
# 设置中文字体，防止中文乱码
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(figsize=(10, 7))

# 1. 画SML直线 (Beta从0到2)
beta_line = [0, 2]
# 收益率转为百分比以便阅读
er_line = [(rf + b * sml_slope) * 100 for b in beta_line] 
ax.plot(beta_line, er_line, label='证券市场线 (SML)', color='blue', linewidth=2.5)

# 2. 标出给定的三个点 (坐标转换为百分比显示)
points = {
    'X': (0.62, 8.1),
    'Y': (1.18, 13.1),
    'Z': (1.51, 9.9)
}

for name, (b, er) in points.items():
    ax.scatter(b, er, color='red', s=60, zorder=5)
    # 判断点在SML上方还是下方以调整注释位置，避免重叠
    sml_er_at_b = (rf + b * sml_slope) * 100
    offset_y = 8 if er > sml_er_at_b else -12
    ax.annotate(f'{name} ({b}, {er}%)', 
                xy=(b, er), 
                xytext=(10, offset_y), 
                textcoords='offset points',
                fontsize=11, 
                fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.3', fc='yellow', alpha=0.6))

# 3. 标出无风险利率点和市场组合点
ax.scatter(0, rf * 100, color='green', s=80, zorder=5)
ax.annotate(f'无风险利率\n(0, {rf*100:.1f}%)', xy=(0, rf * 100), xytext=(15, -15), textcoords='offset points', fontsize=10)

ax.scatter(1, erm * 100, color='purple', s=80, zorder=5)
ax.annotate(f'市场组合\n(1, {erm*100:.1f}%)', xy=(1, erm * 100), xytext=(15, -15), textcoords='offset points', fontsize=10)

# 4. 图表格式美化
ax.set_xlabel('Beta (β)', fontsize=13)
ax.set_ylabel('期望收益率 (%)', fontsize=13)
ax.set_title(f'证券市场线 (SML)\n$r_f$ = {rf*100:.1f}%, $E(R_m)$ = {erm*100:.1f}%', fontsize=15)
ax.set_xlim(-0.05, 2.1)
ax.set_ylim(0, 18)
ax.axhline(0, color='black', linewidth=0.8, linestyle='--')
ax.grid(True, linestyle='--', alpha=0.5)
ax.legend(fontsize=12)

# 保存图片
figure_path = 'sml_plot.png'
plt.savefig(figure_path, dpi=300, bbox_inches='tight')
plt.close()

# ==========================================
# 按照输出契约打包结果
# ==========================================
result = {
    'sml_slope': sml_slope,           # 0.071
    'er_at_beta_127': er_at_beta_127, # 0.11317
    'figure_path': figure_path        # 'sml_plot.png'
}

print(result)
