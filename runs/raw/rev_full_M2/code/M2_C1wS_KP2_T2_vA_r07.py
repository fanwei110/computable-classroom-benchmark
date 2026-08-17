import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 参数设定（可在此处修改）
# ==========================================
rf = 0.023        # 无风险利率 (2.3%)
market_er = 0.094 # 市场期望收益 (9.4%)
# ==========================================

# SML 斜率 = 市场风险溢价
sml_slope = market_er - rf

# beta 范围
beta_vals = np.linspace(0, 2, 100)
sml_er = rf + sml_slope * beta_vals

# 三只股票的数据
stocks = {
    'X': (0.62, 0.081),
    'Y': (1.18, 0.131),
    'Z': (1.51, 0.099)
}

# 计算 beta=1.27 处的期望收益
beta_target = 1.27
er_at_target = rf + sml_slope * beta_target

# 输出计算结果
print(f"SML 斜率 (市场风险溢价): {sml_slope:.4f} ({sml_slope*100:.2f}%)")
print(f"Beta={beta_target} 时期的望收益: {er_at_target:.4f} ({er_at_target*100:.2f}%)")

# ==========================================
# 绘图
# ==========================================
plt.figure(figsize=(10, 6))
plt.plot(beta_vals, sml_er, 'b-', linewidth=2, label='Security Market Line (SML)')

# 绘制市场组合点 (beta=1, er=market_er)
plt.scatter(1.0, market_er, color='green', s=100, zorder=5, label='Market Portfolio')
plt.text(1.0, market_er, f'  Market (1.0, {market_er*100:.1f}%)', fontsize=10, color='green')

# 绘制三只股票
colors = {'X': 'red', 'Y': 'orange', 'Z': 'purple'}
for stock, (beta, er) in stocks.items():
    plt.scatter(beta, er, color=colors[stock], s=100, zorder=5, label=f'Stock {stock}')
    plt.text(beta, er, f'  {stock} ({beta:.2f}, {er*100:.2f}%)', fontsize=10, color=colors[stock])

# 标出 beta=1.27 的点
plt.scatter(beta_target, er_at_target, color='magenta', s=80, marker='^', zorder=5, label=f'Beta={beta_target}')
plt.text(beta_target, er_at_target, f'  Beta={beta_target} ({er_at_target*100:.2f}%)', fontsize=10, color='magenta')

# 标注 alpha（与 SML 的垂直偏差）
for stock, (beta, er) in stocks.items():
    er_sml = rf + sml_slope * beta
    alpha = er - er_sml
    label = f'α={alpha*100:+.2f}%'
    plt.vlines(beta, er_sml, er, linestyles='dashed', colors=colors[stock], alpha=0.7)
    plt.annotate(label, xy=(beta, er), xytext=(beta+0.05, (er+er_sml)/2),
                 fontsize=9, color=colors[stock], ha='left')

plt.xlabel('Beta (β)', fontsize=12)
plt.ylabel('Expected Return', fontsize=12)
plt.title(f'Security Market Line (SML)\nRisk-Free Rate = {rf*100:.1f}%, Market Return = {market_er*100:.1f}%', fontsize=14)
plt.legend(loc='lower right')
plt.grid(True, alpha=0.3)
plt.xlim(0, 2)
plt.ylim(0, 0.18)
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y*100:.0f}%'))
plt.tight_layout()

# 保存图片
figure_path = 'sml_plot.png'
plt.savefig(figure_path, dpi=150)
plt.show()

# ==========================================
# 填充结果字典
# ==========================================
result = {
    'sml_slope': sml_slope,
    'er_at_beta_127': er_at_target,
    'figure_path': figure_path
}

# 验证输出
print("\n结果字典:")
for key, value in result.items():
    if isinstance(value, float):
        print(f"{key}: {value:.6f} ({value*100:.4f}%)")
    else:
        print(f"{key}: {value}")
