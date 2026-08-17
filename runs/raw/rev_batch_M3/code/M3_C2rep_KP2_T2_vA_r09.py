import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# ==========================================
# 1. 参数化设置 (可调参数)
# ==========================================
rf = 0.023      # 无风险利率 2.3%
rm = 0.094      # 市场期望收益 9.4%

# ==========================================
# 2. 核心计算
# ==========================================
# SML 斜率
sml_slope = rm - rf

# beta = 1.27 处的 CAPM 期望收益
beta_target = 1.27
er_at_beta_127 = rf + beta_target * sml_slope

# 股票数据
stocks = {
    'X': {'beta': 0.62, 'return': 0.081},
    'Y': {'beta': 1.18, 'return': 0.131},
    'Z': {'beta': 1.51, 'return': 0.099}
}

# ==========================================
# 3. 绘图设置与绘制
# ==========================================
# 设置中文字体，防止中文乱码
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(figsize=(10, 7))

# 生成 beta 序列 (0 到 2)
betas = np.linspace(0, 2, 100)
# SML 对应的期望收益序列
er_sml = rf + betas * sml_slope

# 画出 SML
ax.plot(betas, er_sml * 100, label='证券市场线 (SML)', color='blue', linewidth=2.5)

# 画出无风险利率点和市场组合点
ax.scatter(0, rf * 100, color='green', s=80, zorder=5, label=f'无风险资产 (Rf={rf*100:.1f}%)')
ax.scatter(1, rm * 100, color='purple', s=80, zorder=5, label=f'市场组合 (Rm={rm*100:.1f}%)')

# 画出三只股票并标注 Alpha 偏离
for name, data in stocks.items():
    b = data['beta']
    r_actual = data['return']
    r_capm = rf + b * sml_slope
    
    # 画出股票点
    ax.scatter(b, r_actual * 100, color='red', s=100, zorder=5)
    
    # 标注股票名称和实际收益
    ax.annotate(f'{name}\n(β={b}, E={r_actual*100:.1f}%)',
                xy=(b, r_actual * 100),
                xytext=(15, 15 if r_actual >= r_capm else -25),
                textcoords='offset points',
                fontsize=10,
                arrowprops=dict(arrowstyle='->', color='black', lw=1.5),
                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8))
                
    # 画出表示 Alpha 的垂直虚线 (偏离SML的部分)
    ax.plot([b, b], [r_capm * 100, r_actual * 100], color='gray', linestyle='--', linewidth=1.5)
    # 在垂直线中点标明 Alpha
    alpha_val = r_actual - r_capm
    ax.text(b + 0.03, (r_actual + r_capm) / 2 * 100, f'α={alpha_val*100:.2f}%', 
            fontsize=9, color='darkred', fontweight='bold')

# 图表美化
ax.set_title('CAPM 与证券市场线 (SML)', fontsize=16, fontweight='bold')
ax.set_xlabel('Beta (β)', fontsize=13)
ax.set_ylabel('期望收益 (%)', fontsize=13)
ax.yaxis.set_major_formatter(mticker.PercentFormatter())
ax.set_xlim(-0.05, 2.05)
ax.set_ylim(0, 20)
ax.grid(True, linestyle='--', alpha=0.7)
ax.legend(loc='upper left', fontsize=11)

# ==========================================
# 4. 保存图形与输出结果
# ==========================================
figure_path = 'sml_plot.png'
plt.savefig(figure_path, dpi=300, bbox_inches='tight')
plt.close()

# 将结果存入字典
result = {
    'sml_slope': sml_slope,
    'er_at_beta_127': er_at_beta_127,
    'figure_path': figure_path
}

# 打印报告以便课堂投屏展示
print("="*50)
print("《证券投资学》课堂实时计算报告")
print("="*50)
print(f"1. 无风险利率 (Rf): {rf*100:.1f}%")
print(f"2. 市场期望收益 (Rm): {rm*100:.1f}%")
print(f"3. SML 斜率 (市场风险溢价): {sml_slope*100:.1f}% ({sml_slope:.4f})")
print(f"4. Beta=1.27 处的 CAPM 期望收益: {er_at_beta_127*100:.2f}% ({er_at_beta_127:.4f})")
print("-" * 50)
print("股票 Alpha 分析:")
for name, data in stocks.items():
    capm_e = rf + data['beta'] * sml_slope
    alpha = data['return'] - capm_e
    status = "被低估(正Alpha)" if alpha > 0 else "被高估(负Alpha)"
    print(f"  股票 {name}: 实际收益 {data['return']*100:.1f}%, CAPM收益 {capm_e*100:.2f}%, Alpha {alpha*100:.2f}% -> {status}")
print("="*50)
print(f"图形已保存至: {figure_path}")
