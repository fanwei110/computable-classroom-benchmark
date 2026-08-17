import matplotlib.pyplot as plt
import numpy as np
import json
import os

# 参数设定
rf = 2.3
market_return = 9.4
beta_range = np.linspace(0, 2, 100)

# SML 方程: E(R) = rf + beta * (market_return - rf)
market_premium = market_return - rf
sml_slope = market_premium  # 7.1%
sml_line = rf + beta_range * sml_slope

# 给定的三个点
points = {
    'X': (0.62, 8.1),
    'Y': (1.18, 13.1),
    'Z': (1.51, 9.9)
}

# 计算 beta=1.27 对应的期望收益
beta_target = 1.27
er_at_beta_127 = rf + beta_target * sml_slope

# 绘图
fig, ax = plt.subplots(figsize=(10, 6))

# 绘制 SML 线
ax.plot(beta_range, sml_line, 'b-', linewidth=2, label='Security Market Line (SML)')
ax.axhline(y=rf, color='gray', linestyle='--', linewidth=0.8)
ax.axvline(x=1, color='gray', linestyle='--', linewidth=0.8)

# 标记 rf 和市场组合点，并使其可拖动（此处仅为可视化，不实现交互拖动代码）
rf_point, = ax.plot(0, rf, 'ko', markersize=10, label=f'Risk-free rate (β=0, {rf}%)')
mkt_point, = ax.plot(1, market_return, 'ko', markersize=10, label=f'Market portfolio (β=1, {market_return}%)')

# 标注三个点
colors = ['red', 'green', 'purple']
for color, (name, (beta, er)) in zip(colors, points.items()):
    ax.plot(beta, er, 'o', color=color, markersize=8)
    ax.annotate(f'{name} (β={beta}, {er}%)', xy=(beta, er),
                xytext=(5, 5), textcoords='offset points',
                fontsize=10, fontweight='bold', color=color)

# 标注 beta=1.27 对应点
ax.plot(beta_target, er_at_beta_127, 'r*', markersize=12, label=f'β=1.27, E(R)={er_at_beta_127:.2f}%')
ax.axvline(x=beta_target, color='red', linestyle=':', alpha=0.6)
ax.axhline(y=er_at_beta_127, color='red', linestyle=':', alpha=0.6)

# 图形设置
ax.set_xlabel('Beta (β)', fontsize=12)
ax.set_ylabel('Expected Return (%)', fontsize=12)
ax.set_title('Security Market Line (SML)', fontsize=14)
ax.set_xlim(0, 2)
ax.set_ylim(0, 18)
ax.legend(loc='lower right')
ax.grid(True, alpha=0.3)

# 保存图形
figure_path = 'sml_plot.png'
plt.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close()

# 构建结果字典
result = {
    'sml_slope': sml_slope,
    'er_at_beta_127': er_at_beta_127,
    'figure_path': os.path.abspath(figure_path)
}

# 打印结果以验证
print(json.dumps(result, indent=2))
