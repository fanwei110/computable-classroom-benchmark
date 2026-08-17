import os
import numpy as np
import matplotlib.pyplot as plt

# =============================================================================
# 可调参数 (无风险利率与市场期望收益)
# 修改这两个数值即可更新整条证券市场线 (SML) 及相关结果
# =============================================================================
RISK_FREE_RATE = 0.023      # 无风险利率 2.3%
MARKET_RETURN  = 0.094      # 市场期望收益 9.4%

# =============================================================================
# 股票数据 (不可调，仅用于绘图标注)
# =============================================================================
STOCKS = {
    'X': {'beta': 0.62, 'return': 0.081},
    'Y': {'beta': 1.18, 'return': 0.131},
    'Z': {'beta': 1.51, 'return': 0.099},
}

# =============================================================================
# 核心计算
# =============================================================================
sml_slope = MARKET_RETURN - RISK_FREE_RATE                      # SML 斜率
beta_target = 1.27                                              # 目标 beta
er_at_target = RISK_FREE_RATE + beta_target * sml_slope         # CAPM 期望收益

# =============================================================================
# 绘图
# =============================================================================
fig, ax = plt.subplots(figsize=(10, 6))

# 生成 beta 序列并绘制 SML
beta = np.linspace(0, 2, 200)
sml = RISK_FREE_RATE + beta * sml_slope
ax.plot(beta, sml, 'deepskyblue', linewidth=2, label='SML')

# 标注无风险资产与市场组合
ax.scatter(0, RISK_FREE_RATE, color='black', zorder=5)
ax.scatter(1, MARKET_RETURN, color='black', zorder=5)
ax.annotate('Risk-free\n(0, {:.1%})'.format(RISK_FREE_RATE),
            xy=(0, RISK_FREE_RATE), xytext=(10, -10),
            textcoords='offset points', fontsize=9,
            arrowprops=dict(arrowstyle='->', lw=0.8))
ax.annotate('Market\n(1, {:.1%})'.format(MARKET_RETURN),
            xy=(1, MARKET_RETURN), xytext=(10, -10),
            textcoords='offset points', fontsize=9,
            arrowprops=dict(arrowstyle='->', lw=0.8))

# 绘制股票 X, Y, Z
colors = {'X': 'crimson', 'Y': 'seagreen', 'Z': 'darkorange'}
for name, vals in STOCKS.items():
    ax.scatter(vals['beta'], vals['return'], color=colors[name],
               edgecolors='black', s=80, zorder=5)
    ax.annotate(f'{name}  (β={vals["beta"]}, E(r)={vals["return"]:.1%})',
                xy=(vals['beta'], vals['return']),
                xytext=(8, 8), textcoords='offset points',
                fontsize=9, color=colors[name],
                arrowprops=dict(arrowstyle='->', lw=0.8, color=colors[name]))

# 图表装饰
ax.set_xlim(0, 2)
ax.set_ylim(0, 0.2)
ax.set_xlabel('Beta (β)', fontsize=12)
ax.set_ylabel('Expected Return E(r)', fontsize=12)
ax.set_title('Security Market Line (SML)', fontsize=14, fontweight='bold')
ax.grid(True, linestyle='--', alpha=0.5)
ax.legend(loc='lower right')

# 在图上添加关键数值文本
textstr = (f'Risk-free rate = {RISK_FREE_RATE:.1%}\n'
           f'Market return = {MARKET_RETURN:.1%}\n'
           f'SML slope = {sml_slope:.4f}\n'
           f'E(r) at β={beta_target} = {er_at_target:.4f}')
props = dict(boxstyle='round,pad=0.4', facecolor='lightyellow', alpha=0.8)
ax.text(0.03, 0.97, textstr, transform=ax.transAxes, fontsize=10,
        verticalalignment='top', bbox=props)

plt.tight_layout()

# =============================================================================
# 保存图像并组织输出
# =============================================================================
figure_path = os.path.abspath('sml.png')
fig.savefig(figure_path, dpi=150)
plt.close(fig)   # 关闭图形以释放内存，确保无 GUI 依赖

result = {
    'sml_slope': sml_slope,
    'er_at_beta_127': er_at_target,
    'figure_path': figure_path,
}

# 输出结果供核查 (在交互环境中可直接查看字典)
print(result)
