import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 1. 参数化无风险利率与市场期望收益
# ==========================================
# 采用百分比数值输入，内部计算时转换为小数
rf_pct = 2.3   # 无风险利率 (%)
rm_pct = 9.4   # 市场期望收益 (%)

rf = rf_pct / 100.0
rm = rm_pct / 100.0

# ==========================================
# 2. 计算 SML 斜率与指定 Beta 处的期望收益
# ==========================================
sml_slope = rm - rf
beta_target = 1.27
er_at_beta_127 = rf + beta_target * sml_slope

# ==========================================
# 3. 定义股票数据
# ==========================================
stocks = {
    'X': {'beta': 0.62, 'return_pct': 8.1},
    'Y': {'beta': 1.18, 'return_pct': 13.1},
    'Z': {'beta': 1.51, 'return_pct': 9.9}
}

# ==========================================
# 4. 绘制图形
# ==========================================
# 设置中文字体与负号显示
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(figsize=(10, 7))

# 画出 SML (Beta 从 0 到 2)
beta_range = np.linspace(0, 2, 100)
sml_returns_pct = (rf + beta_range * sml_slope) * 100  # 转换为百分比显示

ax.plot(beta_range, sml_returns_pct, label='证券市场线 (SML)', color='blue', linewidth=2.5)

# 标出股票点并计算 alpha
for name, data in stocks.items():
    beta_i = data['beta']
    ret_i_pct = data['return_pct']
    
    # CAPM 期望收益 (%)
    er_i_pct = (rf + beta_i * sml_slope) * 100
    # Alpha (%)
    alpha_i_pct = ret_i_pct - er_i_pct
    
    ax.scatter(beta_i, ret_i_pct, color='red', s=60, zorder=5)
    # 标注内容：股票名、实际收益、Alpha
    annotate_text = f'{name}\n收益: {ret_i_pct:.1f}%\nα: {alpha_i_pct:+.2f}%'
    ax.annotate(annotate_text,
                xy=(beta_i, ret_i_pct),
                xytext=(15, 10),
                textcoords='offset points',
                fontsize=10,
                bbox=dict(boxstyle='round,pad=0.4', fc='lightyellow', ec='gray', alpha=0.9),
                arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.2', color='gray'))

# 标出关键基准点 (无风险利率与市场组合)
ax.scatter(0, rf_pct, color='green', s=60, zorder=5)
ax.annotate(f'无风险利率\n{rf_pct}%', xy=(0, rf_pct), xytext=(-15, -25), 
            textcoords='offset points', fontsize=9, color='green')

ax.scatter(1, rm_pct, color='purple', s=60, zorder=5)
ax.annotate(f'市场组合\n{rm_pct}%', xy=(1, rm_pct), xytext=(10, -25), 
            textcoords='offset points', fontsize=9, color='purple')

# 图形格式美化
ax.set_title('CAPM 与证券市场线 (SML)', fontsize=18, fontweight='bold')
ax.set_xlabel('Beta (β)', fontsize=14)
ax.set_ylabel('期望收益率 (%)', fontsize=14)
ax.set_xlim(0, 2)
ax.set_ylim(0, 20)
ax.grid(True, linestyle='--', alpha=0.6)
ax.legend(fontsize=13, loc='upper left')

# 在图表中添加报告斜率和特定点期望收益的文本框
info_text = (f'SML 斜率 (市场风险溢价): {sml_slope*100:.2f}%\n'
             f'β=1.27 处 CAPM 期望收益: {er_at_beta_127*100:.2f}%')
props = dict(boxstyle='round', facecolor='white', alpha=0.9, edgecolor='black')
ax.text(0.98, 0.05, info_text, transform=ax.transAxes, fontsize=11,
        verticalalignment='bottom', horizontalalignment='right', bbox=props)

# ==========================================
# 5. 保存图形并填充 result
# ==========================================
figure_path = 'sml_plot.png'
plt.savefig(figure_path, dpi=300, bbox_inches='tight')
plt.close()

# 将结果存入字典 (期望收益与斜率保留小数形式)
result = {
    'sml_slope': sml_slope,
    'er_at_beta_127': er_at_beta_127,
    'figure_path': figure_path
}
