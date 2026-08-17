import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

# ==========================================
# 1. 参数化设置 (方便上课实时调参)
# ==========================================
rf = 0.023           # 无风险利率 2.3%
E_Rm = 0.094         # 市场期望收益 9.4%

# 题目给定的三只股票数据
stocks = {
    'X': {'beta': 0.62, 'er': 0.081},
    'Y': {'beta': 1.18, 'er': 0.131},
    'Z': {'beta': 1.51, 'er': 0.099}
}

# ==========================================
# 2. 核心计算
# ==========================================
# SML斜率即市场风险溢价: E(Rm) - rf
sml_slope = E_Rm - rf

# 计算 beta = 1.27 对应的期望收益 (SML上的理论收益)
beta_target = 1.27
er_at_beta_127 = rf + beta_target * sml_slope

# ==========================================
# 3. 绘制证券市场线 (SML)
# ==========================================
# 生成 beta 从 0 到 2 的数据
betas = np.linspace(0, 2, 200)
sml_ers = rf + betas * sml_slope

fig, ax = plt.subplots(figsize=(10, 6))

# 绘制 SML 直线
ax.plot(betas, sml_ers, label=f'SML (Slope = {sml_slope:.2%})', color='navy', linewidth=2.5)

# 标出无风险利率点和市场组合点
ax.scatter(0, rf, color='black', zorder=5, s=50)
ax.annotate(f'$r_f$ = {rf:.1%}', xy=(0, rf), xytext=(15, -15), textcoords='offset points', fontsize=11)
ax.scatter(1, E_Rm, color='black', zorder=5, s=50)
ax.annotate(f'Market = {E_Rm:.1%}', xy=(1, E_Rm), xytext=(15, -15), textcoords='offset points', fontsize=11)

# 标出三只股票，并画出它们偏离 SML 的距离 (即 Alpha)
colors = {'X': 'green', 'Y': 'darkorange', 'Z': 'crimson'}
for name, data in stocks.items():
    b = data['beta']
    e = data['er']
    sml_e = rf + b * sml_slope  # 对应的SML理论收益
    
    # 画股票点
    ax.scatter(b, e, color=colors[name], zorder=5, s=70, label=f'Stock {name} (β={b}, E(R)={e:.1%})')
    
    # 标注股票名称
    ax.annotate(f'{name}', xy=(b, e), xytext=(8, 8), textcoords='offset points', 
                fontsize=13, fontweight='bold', color=colors[name])
    
    # 画出偏离SML的垂直虚线 (Alpha的直观体现)
    ax.vlines(b, min(e, sml_e), max(e, sml_e), colors=colors[name], linestyles='dashed', linewidth=1.5)

# 坐标轴与排版格式设置
ax.yaxis.set_major_formatter(PercentFormatter(1.0, decimals=1))
ax.set_xlabel('Beta (β)', fontsize=12)
ax.set_ylabel('Expected Return E(R)', fontsize=12)
ax.set_title('Security Market Line (SML) and Stock Valuation', fontsize=14, fontweight='bold')
ax.legend(loc='upper left', fontsize=10)
ax.grid(True, linestyle='--', alpha=0.6)
ax.set_xlim(0, 2.1)
ax.set_ylim(0, 0.18)

# ==========================================
# 4. 保存图形并填充结果字典
# ==========================================
fig_path = 'sml_plot.png'
fig.savefig(fig_path, dpi=300, bbox_inches='tight')
plt.close()

result = {
    'sml_slope': sml_slope,
    'er_at_beta_127': er_at_beta_127,
    'figure_path': fig_path
}

# 控制台输出验证
print(f"SML斜率: {result['sml_slope']:.4f} ({result['sml_slope']:.2%})")
print(f"Beta=1.27时的期望收益: {result['er_at_beta_127']:.4f} ({result['er_at_beta_127']:.2%})")
print(f"图片保存路径: {result['figure_path']}")
