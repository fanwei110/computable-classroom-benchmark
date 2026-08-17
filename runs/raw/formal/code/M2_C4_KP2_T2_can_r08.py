import numpy as np
import matplotlib.pyplot as plt

# ==================== 可调参数 ====================
rf = 0.023   # 无风险利率
rm = 0.094   # 市场期望收益
# ================================================

# 股票数据
stocks = {
    'X': {'beta': 0.62, 'return': 0.081},
    'Y': {'beta': 1.18, 'return': 0.131},
    'Z': {'beta': 1.51, 'return': 0.099},
}

# CAPM 计算
market_premium = rm - rf          # 市场风险溢价，也是 SML 斜率
sml_slope = market_premium

# 指定 beta
target_beta = 1.27
er_at_target = rf + sml_slope * target_beta

# 生成 SML 线的数据点
beta_vals = np.linspace(0, 2, 100)
sml_vals = rf + sml_slope * beta_vals

# ==================== 绘图 ====================
plt.figure(figsize=(8, 6))
plt.plot(beta_vals, sml_vals, 'b-', linewidth=2, label='SML')
plt.axhline(y=rf, color='gray', linestyle='--', alpha=0.7, label=f'Risk-free rate = {rf:.3f}')

# 标出股票点
colors = {'X': 'red', 'Y': 'green', 'Z': 'orange'}
for name, data in stocks.items():
    beta, ret = data['beta'], data['return']
    plt.scatter(beta, ret, color=colors[name], zorder=5, s=80, edgecolors='k', label=f'Stock {name}')
    plt.annotate(name, (beta, ret), textcoords="offset points", xytext=(10, 8),
                 ha='center', fontsize=11, fontweight='bold', color=colors[name])

# 标出市场组合点 (beta=1, rm)
plt.scatter(1, rm, color='darkblue', marker='^', s=100, zorder=5, edgecolors='k', label='Market (M)')
plt.annotate('M', (1, rm), textcoords="offset points", xytext=(10, -12),
             ha='center', fontsize=11, fontweight='bold', color='darkblue')

# 标出 beta=1.27 点（用于参考）
plt.scatter(target_beta, er_at_target, color='purple', marker='s', s=80, zorder=5, edgecolors='k',
            label=f'β={target_beta}, E[r]={er_at_target:.4f}')
plt.annotate(f'β={target_beta}\n{er_at_target:.4f}', (target_beta, er_at_target),
             textcoords="offset points", xytext=(-10, -20), ha='center', fontsize=9, color='purple')

plt.xlabel('Beta (β)')
plt.ylabel('Expected Return')
plt.title('Security Market Line (SML)')
plt.legend(loc='upper left', fontsize='small')
plt.grid(True, alpha=0.3)
plt.xlim(0, 2)
plt.ylim(bottom=0, top=max(sml_vals)*1.05)  # 留一点顶部空间

# 保存图形
figure_path = 'sml_plot.png'
plt.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.show()

# ==================== 输出契约 ====================
result = {
    'sml_slope': sml_slope,
    'er_at_beta_127': er_at_target,
    'figure_path': figure_path,
}

# 打印结果以便课堂展示
print("=== CAPM & SML 结果 ===")
print(f"SML 斜率 (市场风险溢价) : {sml_slope:.4f}")
print(f"β = 1.27 处的 CAPM 期望收益 : {er_at_target:.4f}")
print(f"图形已保存至 : {figure_path}")
