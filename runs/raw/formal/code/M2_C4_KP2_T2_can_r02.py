import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# 可调参数
risk_free_rate = 0.023  # 无风险利率 2.3%
market_return = 0.094   # 市场期望收益 9.4%

# 计算证券市场线(SML)的斜率
sml_slope = market_return - risk_free_rate
print(f"SML斜率: {sml_slope:.4f} ({sml_slope*100:.2f}%)")

# 市场贝塔和期望收益的关系
# E(R) = Rf + beta * (Rm - Rf)
# 当 beta = 0 时，E(R) = Rf
# 当 beta = 1 时，E(R) = Rm

# 计算三只股票的期望收益
stocks = {
    'X': {'beta': 0.62, 'return': 0.081, 'label': 'X'},
    'Y': {'beta': 1.18, 'return': 0.131, 'label': 'Y'},
    'Z': {'beta': 1.51, 'return': 0.099, 'label': 'Z'}
}

# 计算每只股票根据CAPM的期望收益和alpha值
for symbol, stock in stocks.items():
    capm_er = risk_free_rate + stock['beta'] * sml_slope
    alpha = stock['return'] - capm_er
    print(f"股票{symbol}(beta={stock['beta']}): 实际收益={stock['return']*100:.2f}%, CAPM期望收益={capm_er*100:.2f}%, alpha={alpha*100:.2f}%")

# 计算beta=1.27时的CAPM期望收益
beta_127 = 1.27
er_at_beta_127 = risk_free_rate + beta_127 * sml_slope
print(f"Beta=1.27时的CAPM期望收益: {er_at_beta_127:.4f} ({er_at_beta_127*100:.2f}%)")

# 绘制证券市场线
plt.figure(figsize=(10, 6))

# 生成beta值范围
beta_range = np.linspace(0, 2, 100)
# 计算对应的期望收益
er_range = risk_free_rate + beta_range * sml_slope

# 绘制SML线
plt.plot(beta_range, er_range, 'b-', linewidth=2, label=f'SML (Rf={risk_free_rate*100:.1f}%, Rm={market_return*100:.1f}%)')

# 标记特殊点
# 无风险利率点 (beta=0)
plt.plot(0, risk_free_rate, 'go', markersize=8, label=f'无风险利率点 (β=0, E(R)={risk_free_rate*100:.2f}%)')
plt.text(0, risk_free_rate, f'Rf={risk_free_rate*100:.1f}%', fontsize=9, ha='right')

# 市场组合点 (beta=1)
plt.plot(1, market_return, 'mo', markersize=8, label=f'市场组合 (β=1, E(R)={market_return*100:.2f}%)')
plt.text(1, market_return, f'市场组合', fontsize=9, ha='left')

# 标记三只股票
colors = ['red', 'orange', 'purple']
for (symbol, stock), color in zip(stocks.items(), colors):
    # 实际收益点
    plt.scatter(stock['beta'], stock['return'], c=color, s=80, zorder=5)
    # 标注
    plt.annotate(f'{symbol}\nβ={stock["beta"]}\nE(R)={stock["return"]*100:.1f}%', 
                 xy=(stock['beta'], stock['return']),
                 xytext=(10, 10), textcoords='offset points',
                 fontsize=9, color=color)
    
    # 计算对应的SML上的点
    capm_er = risk_free_rate + stock['beta'] * sml_slope
    
    # 绘制从实际点到SML线的连线（表示alpha）
    plt.plot([stock['beta'], stock['beta']], [stock['return'], capm_er], 
             '--', color=color, alpha=0.5)
    
    # 如果需要突出显示CAPM期望收益点
    plt.scatter(stock['beta'], capm_er, c=color, alpha=0.3, s=50, marker='s')

# 标记beta=1.27的点
plt.axvline(x=beta_127, color='green', linestyle='--', alpha=0.7)
plt.scatter(beta_127, er_at_beta_127, c='green', s=100, zorder=5)
plt.annotate(f'β={beta_127}\nE(R)={er_at_beta_127*100:.2f}%', 
             xy=(beta_127, er_at_beta_127),
             xytext=(15, -15), textcoords='offset points',
             fontsize=9, color='green',
             arrowprops=dict(arrowstyle='->', color='green'))

plt.xlabel('Beta (β)', fontsize=12, fontweight='bold')
plt.ylabel('期望收益 E(R)', fontsize=12, fontweight='bold')
plt.title('证券市场线 (SML) - CAPM\n股票X, Y, Z分析', fontsize=14, fontweight='bold')
plt.legend(loc='lower right')
plt.grid(True, alpha=0.3)
plt.xlim(-0.1, 2.1)
plt.ylim(0, 0.16)  # 设置合理的y轴范围

# 调整显示格式
plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:.2f}'))
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda y, p: f'{y*100:.1f}%'))

plt.tight_layout()

# 保存图像
figure_path = '/tmp/capm_sml_analysis.png'
plt.savefig(figure_path, dpi=300, bbox_inches='tight')
plt.show()

# 输出结果字典
result = {
    'sml_slope': sml_slope,
    'er_at_beta_127': er_at_beta_127,
    'figure_path': figure_path
}

print(f"\nSML斜率: {result['sml_slope']:.6f}")
print(f"Beta=1.27时的CAPM期望收益: {result['er_at_beta_127']:.6f}")
print(f"图像保存路径: {result['figure_path']}")
