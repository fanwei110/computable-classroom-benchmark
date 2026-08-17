import matplotlib.pyplot as plt
import numpy as np
import os

# ==========================================
# 👨‍🏫 可调参数区（上课改这里即可）
# ==========================================
rf = 2.3    # 无风险利率 (%)
rm = 9.4    # 市场期望收益 (%)
# ==========================================

# 1. 计算 SML 斜率
sml_slope_pct = rm - rf
sml_slope = sml_slope_pct / 100  # 转换为小数形式

# 2. 计算 beta=1.27 对应的期望收益
beta_target = 1.27
er_at_beta_127_pct = rf + beta_target * sml_slope_pct
er_at_beta_127 = er_at_beta_127_pct / 100  # 转换为小数形式

# 3. 绘制证券市场线 (SML)
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS']  # 兼容中文字体
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(figsize=(10, 7))

# 生成 SML 数据
beta_range = np.linspace(0, 2, 100)
er_sml = rf + beta_range * sml_slope_pct

# 画 SML 线
ax.plot(beta_range, er_sml, label=f'SML (斜率={sml_slope_pct:.1f}%)', color='royalblue', linewidth=2.5)

# 标出三个资产点
points = {
    'X': (0.62, 8.1),
    'Y': (1.18, 13.1),
    'Z': (1.51, 9.9)
}

colors = ['red', 'green', 'purple']
for (name, (b, er)), color in zip(points.items(), colors):
    ax.scatter(b, er, color=color, zorder=5, s=80)
    # 标注文字稍微偏移以防重叠
    offset_x, offset_y = 0.05, 0.6
    if name == 'Z':
        offset_y = -1.0
    ax.annotate(f'{name}($\\beta$={b}, E(R)={er}%)', 
                xy=(b, er), 
                xytext=(b + offset_x, er + offset_y),
                fontsize=11,
                arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=5))

# 标出无风险利率和市场组合点
ax.scatter(0, rf, color='black', zorder=5, s=60)
ax.annotate(f'$r_f$={rf}%', xy=(0, rf), xytext=(0.05, rf - 1.2), fontsize=11)
ax.scatter(1, rm, color='black', zorder=5, s=60, marker='*')
ax.annotate(f'Market($\\beta$=1, E(R)={rm}%)', xy=(1, rm), xytext=(1.05, rm + 0.5), fontsize=11)

# 标出 beta=1.27 的计算点
ax.scatter(beta_target, er_at_beta_127_pct, color='orange', zorder=5, s=80, marker='D')
ax.annotate(f'$\\beta$=1.27\nE(R)={er_at_beta_127_pct:.2f}%', 
            xy=(beta_target, er_at_beta_127_pct), 
            xytext=(beta_target - 0.35, er_at_beta_127_pct + 1.5),
            fontsize=10,
            arrowprops=dict(facecolor='orange', shrink=0.05, width=1, headwidth=5))

# 格式调整
ax.set_xlabel('Beta ($\\beta$)', fontsize=13)
ax.set_ylabel('Expected Return E(R) (%)', fontsize=13)
ax.set_title('Security Market Line (SML)', fontsize=15)
ax.set_xlim(0, 2)
ax.set_ylim(0, 16)
ax.grid(True, linestyle='--', alpha=0.6)
ax.legend(fontsize=12, loc='upper left')

# 保存图表
figure_path = 'sml_plot.png'
plt.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close()

# 4. 存入结果字典 (按输出契约要求)
result = {
    'sml_slope': sml_slope,           # 0.071 (即 7.1%)
    'er_at_beta_127': er_at_beta_127, # 0.11317 (即 11.317%)
    'figure_path': os.path.abspath(figure_path)
}

# 打印验证信息
print(f"SML 斜率: {sml_slope_pct:.1f}% (小数形式: {sml_slope})")
print(f"Beta=1.27 时的期望收益: {er_at_beta_127_pct:.3f}% (小数形式: {er_at_beta_127})")
print(f"图表已保存至: {result['figure_path']}")
print(f"\n结果字典: {result}")
