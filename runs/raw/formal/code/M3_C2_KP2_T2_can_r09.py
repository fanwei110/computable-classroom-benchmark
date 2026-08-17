import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# =====================
# 1. 参数化假设
# =====================
rf = 0.023          # 无风险利率 2.3%
rm = 0.094          # 市场期望收益 9.4%

# =====================
# 2. 核心计算
# =====================
# SML 斜率即市场风险溢价
sml_slope = rm - rf

# Beta = 1.27 处的 CAPM 期望收益
beta_target = 1.27
er_at_beta_127 = rf + beta_target * sml_slope

# 股票数据
stocks = {
    'X': {'beta': 0.62, 'return': 0.081},
    'Y': {'beta': 1.18, 'return': 0.131},
    'Z': {'beta': 1.51, 'return': 0.099}
}

# =====================
# 3. 绘制证券市场线 (SML)
# =====================
fig, ax = plt.subplots(figsize=(10, 7))

# 生成 beta 序列及对应的 SML 期望收益
betas = np.linspace(0, 2, 100)
sml_returns = rf + betas * sml_slope

# 画出 SML
ax.plot(betas, sml_returns, label='Security Market Line (SML)', color='royalblue', linewidth=2.5)

# 标出无风险利率和市场组合点
ax.scatter(0, rf, color='forestgreen', s=80, zorder=5)
ax.annotate(f"$R_f$ ({rf:.1%})", xy=(0, rf), xytext=(15, -10), textcoords='offset points', fontsize=11, color='forestgreen')
ax.scatter(1, rm, color='forestgreen', s=80, zorder=5)
ax.annotate(f"$E(R_m)$ ({rm:.1%})", xy=(1, rm), xytext=(15, -10), textcoords='offset points', fontsize=11, color='forestgreen')

# 画出股票 X, Y, Z 的点，并标注 Alpha 偏离
for name, data in stocks.items():
    stock_beta = data['beta']
    stock_return = data['return']
    sml_er = rf + stock_beta * sml_slope
    alpha = stock_return - sml_er
    
    # 画出垂直虚线表示 Alpha 偏离
    ax.plot([stock_beta, stock_beta], [sml_er, stock_return], 
            color='gray', linestyle='--', linewidth=1.2, zorder=3)
    
    # 画出股票点
    ax.scatter(stock_beta, stock_return, color='crimson', s=100, zorder=5, edgecolors='black')
    
    # 标注文本，根据 Alpha 正负调整箭头方向防止重叠
    y_offset = 15 if alpha >= 0 else -20
    ax.annotate(f"{name} ({stock_return:.1%}, α={alpha:.1%})", 
                xy=(stock_beta, stock_return), 
                xytext=(12, y_offset), 
                textcoords='offset points',
                fontsize=11, 
                fontweight='bold',
                arrowprops=dict(arrowstyle='->', color='black', lw=1.2))

# 格式化图表
ax.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=1, decimals=1))
ax.set_xlabel('Beta ($\\beta$)', fontsize=13)
ax.set_ylabel('Expected Return $E(R)$', fontsize=13)
ax.set_title('CAPM: Security Market Line and Stock Valuation', fontsize=15, fontweight='bold')
ax.grid(True, linestyle=':', alpha=0.7)
ax.legend(fontsize=12, loc='upper left')
ax.set_xlim(-0.05, 2.05)
ax.set_ylim(0, 0.20)

# =====================
# 4. 保存图形并填充结果
# =====================
figure_path = 'sml_plot.png'
fig.savefig(figure_path, dpi=300, bbox_inches='tight')
plt.close(fig)

# 结果字典
result = {
    'sml_slope': sml_slope,
    'er_at_beta_127': er_at_beta_127,
    'figure_path': figure_path
}

# 输出结果供查验
print(f"SML Slope (Market Risk Premium): {sml_slope:.4f} ({sml_slope:.2%})")
print(f"Expected Return at Beta=1.27: {er_at_beta_127:.4f} ({er_at_beta_127:.2%})")
print(f"Figure saved to: {figure_path}")
