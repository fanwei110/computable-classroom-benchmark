import matplotlib.pyplot as plt
import numpy as np
import os

# 参数设置
rf = 2.3  # 无风险利率 (%)
market_return = 9.4  # 市场收益率 (%)
market_beta = 1.0

# 三个点
X = (0.62, 8.1)
Y = (1.18, 13.1)
Z = (1.51, 9.9)

# 计算SML斜率
sml_slope = market_return - rf  # 市场风险溢价

# 计算beta=1.27时的期望收益
beta_target = 1.27
er_at_beta_127 = rf + sml_slope * beta_target

print(f"SML斜率 (市场风险溢价): {sml_slope:.2f}%")
print(f"Beta=1.27时的期望收益率: {er_at_beta_127:.2f}%")

# 创建图形
fig, ax = plt.subplots(figsize=(10, 8))

# 绘制SML线
beta_range = np.linspace(0, 2, 100)
sml_returns = rf + sml_slope * beta_range
ax.plot(beta_range, sml_returns, 'b-', linewidth=2.5, label='SML', zorder=1)

# 标注rf点
ax.scatter(0, rf, color='red', s=150, zorder=5, label='rf')
ax.annotate(f'rf ({rf}%)', (0, rf), xytext=(0.1, rf-1), 
            fontsize=10, fontweight='bold', color='red')

# 标注市场组合点
ax.scatter(market_beta, market_return, color='green', s=150, zorder=5, label='Market')
ax.annotate(f'Market (β=1.0, {market_return}%)', (market_beta, market_return), 
            xytext=(1.05, market_return+0.5), fontsize=10, fontweight='bold', color='green')

# 标注X点
ax.scatter(X[0], X[1], color='orange', s=120, zorder=5, label='X')
ax.annotate(f'X (β={X[0]}, {X[1]}%)', (X[0], X[1]), 
            xytext=(X[0]+0.1, X[1]-1), fontsize=10, color='orange',
            arrowprops=dict(arrowstyle='->', color='orange', lw=1))

# 标注Y点
ax.scatter(Y[0], Y[1], color='purple', s=120, zorder=5, label='Y')
ax.annotate(f'Y (β={Y[0]}, {Y[1]}%)', (Y[0], Y[1]), 
            xytext=(Y[0]+0.1, Y[1]+1), fontsize=10, color='purple',
            arrowprops=dict(arrowstyle='->', color='purple', lw=1))

# 标注Z点
ax.scatter(Z[0], Z[1], color='brown', s=120, zorder=5, label='Z')
ax.annotate(f'Z (β={Z[0]}, {Z[1]}%)', (Z[0], Z[1]), 
            xytext=(Z[0]-0.3, Z[1]-2), fontsize=10, color='brown',
            arrowprops=dict(arrowstyle='->', color='brown', lw=1))

# 标注beta=1.27的期望收益
ax.scatter(beta_target, er_at_beta_127, color='darkblue', s=150, zorder=5, marker='D')
ax.axhline(y=er_at_beta_127, xmin=0, xmax=beta_target/2, color='gray', 
           linestyle='--', alpha=0.7)
ax.axvline(x=beta_target, ymin=0, ymax=er_at_beta_127/15, color='gray', 
           linestyle='--', alpha=0.7)
ax.annotate(f'β={beta_target}\nE(r)={er_at_beta_127:.2f}%', 
            (beta_target, er_at_beta_127), 
            xytext=(beta_target+0.15, er_at_beta_127-1.5), 
            fontsize=10, fontweight='bold', color='darkblue',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='lightblue', alpha=0.7))

# 设置坐标轴
ax.set_xlabel('Beta (β)', fontsize=12, fontweight='bold')
ax.set_ylabel('Expected Return (%)', fontsize=12, fontweight='bold')
ax.set_title('Security Market Line (SML)\nrf = 2.3%, Market Return = 9.4%', 
             fontsize=14, fontweight='bold')

# 设置坐标轴范围
ax.set_xlim(-0.1, 2.1)
ax.set_ylim(0, max(max(sml_returns), 14))

# 添加网格和图例
ax.grid(True, alpha=0.3, linestyle='--')
ax.legend(loc='lower right', fontsize=10)

# 添加文本信息
ax.text(0.2, 13, f'SML Equation: E(r) = {rf}% + {sml_slope:.2f}% × β', 
        fontsize=10, bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

# 保存图形
figure_path = 'sml_chart.png'
plt.savefig(figure_path, dpi=300, bbox_inches='tight')
print(f"图表已保存至: {figure_path}")

# 显示图形
plt.show()

# 创建结果字典
result = {
    'sml_slope': sml_slope,
    'er_at_beta_127': er_at_beta_127,
    'figure_path': os.path.abspath(figure_path)
}

print("\n结果字典:")
print(f"sml_slope: {result['sml_slope']}%")
print(f"er_at_beta_127: {result['er_at_beta_127']:.4f}%")
print(f"figure_path: {result['figure_path']}")
