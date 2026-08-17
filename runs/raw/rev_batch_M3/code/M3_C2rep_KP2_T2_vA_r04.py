import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# ==========================================
# 1. 参数化无风险利率与市场期望收益
# ==========================================
rf = 0.023      # 无风险利率 2.3%
rm = 0.094      # 市场期望收益 9.4%

# ==========================================
# 2. 计算SML斜率与 beta=1.27 处的期望收益
# ==========================================
sml_slope = rm - rf
beta_target = 1.27
er_at_beta_127 = rf + beta_target * sml_slope

# ==========================================
# 3. 定义股票数据并计算Alpha
# ==========================================
stocks = {
    'X': {'beta': 0.62, 'return': 0.081},
    'Y': {'beta': 1.18, 'return': 0.131},
    'Z': {'beta': 1.51, 'return': 0.099}
}

# 计算CAPM期望收益与Alpha
for name, data in stocks.items():
    data['er_capm'] = rf + data['beta'] * sml_slope
    data['alpha'] = data['return'] - data['er_capm']

# ==========================================
# 4. 绘制证券市场线(SML)与股票点
# ==========================================
betas = np.linspace(0, 2, 100)
er_sml = rf + betas * sml_slope

fig, ax = plt.subplots(figsize=(10, 7))

# 绘制SML
ax.plot(betas, er_sml * 100, label='Security Market Line (SML)', color='blue', linewidth=2)

# 标出无风险利率与市场组合点
ax.scatter([0], [rf * 100], color='black', zorder=5, s=60)
ax.annotate(f'Risk-free Rate\n({rf*100:.1f}%)', xy=(0, rf*100), xytext=(0.08, rf*100 + 0.4),
            arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=6))

ax.scatter([1], [rm * 100], color='darkorange', zorder=5, s=60)
ax.annotate(f'Market Portfolio\n({rm*100:.1f}%)', xy=(1, rm*100), xytext=(1.08, rm*100 + 0.4),
            arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=6))

# 标出股票 X, Y, Z 及其Alpha偏离
colors = {'X': 'green', 'Y': 'purple', 'Z': 'red'}
for name, data in stocks.items():
    b = data['beta']
    r = data['return'] * 100
    er = data['er_capm'] * 100
    a = data['alpha'] * 100
    
    # 绘制股票实际收益点
    ax.scatter([b], [r], color=colors[name], zorder=5, s=80, label=f'Stock {name}')
    
    # 绘制Alpha偏离线(虚线)
    ax.vlines(b, er, r, colors=colors[name], linestyles='dashed', linewidth=1.5)
    
    # 标注
    y_offset = 0.6 if a >= 0 else -1.2
    ax.annotate(f'{name}: β={b}, R={r:.1f}%\nα={a:.2f}%', 
                xy=(b, r), 
                xytext=(b + 0.05, r + y_offset),
                fontsize=10,
                color=colors[name])

# 标出 beta=1.27 处的期望收益
er_127_pct = er_at_beta_127 * 100
ax.scatter([beta_target], [er_127_pct], color='grey', marker='x', s=100, zorder=5, linewidths=2)
ax.annotate(f'β={beta_target}, E(R)={er_127_pct:.2f}%', 
            xy=(beta_target, er_127_pct), 
            xytext=(beta_target - 0.45, er_127_pct - 1.8),
            arrowprops=dict(facecolor='grey', shrink=0.05, width=1, headwidth=6),
            fontsize=10,
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="grey", alpha=0.8))

# 格式化图表
ax.set_xlabel('Beta (β)', fontsize=12)
ax.set_ylabel('Expected Return (%)', fontsize=12)
ax.set_title('CAPM: Security Market Line and Stock Valuation', fontsize=14)
ax.set_xlim(0, 2)
ax.set_ylim(0, 16)

# Y轴显示百分比
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda y, _: f'{y:.1f}%'))

ax.axhline(0, color='black', linewidth=0.5)
ax.grid(True, linestyle='--', alpha=0.6)
ax.legend(loc='upper left', fontsize=10)

# ==========================================
# 5. 保存图形并填充 result
# ==========================================
fig_path = 'sml_plot.png'
plt.savefig(fig_path, dpi=300, bbox_inches='tight')
plt.close()

result = {
    'sml_slope': sml_slope,
    'er_at_beta_127': er_at_beta_127,
    'figure_path': fig_path
}

# 控制台输出以供核对
print(f"SML Slope: {result['sml_slope']:.4f} ({result['sml_slope']*100:.2f}%)")
print(f"Expected Return at Beta=1.27: {result['er_at_beta_127']:.4f} ({result['er_at_beta_127']*100:.2f}%)")
print(f"Figure saved to: {result['figure_path']}")
