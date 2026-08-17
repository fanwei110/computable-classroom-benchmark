import numpy as np
import matplotlib.pyplot as plt

# ==================== 可调参数 ====================
risk_free_rate = 2.3   # 百分比，无风险利率
market_return = 9.4    # 百分比，市场期望收益
# =================================================

# 给定股票数据
stocks = {
    'X': {'beta': 0.62, 'return': 8.1},
    'Y': {'beta': 1.18, 'return': 13.1},
    'Z': {'beta': 1.51, 'return': 9.9},
}

# 计算 SML 斜率 (市场风险溢价)
sml_slope = market_return - risk_free_rate   # 单位：%

# 计算 beta = 1.27 处的 CAPM 期望收益
beta_target = 1.27
er_at_beta_127 = risk_free_rate + beta_target * sml_slope

# 输出结果字典
result = {
    'sml_slope': sml_slope,
    'er_at_beta_127': er_at_beta_127,
    'figure_path': 'sml_plot.png'
}

# ----------------- 绘图 -----------------
plt.figure(figsize=(8, 6))

# 绘制证券市场线 (beta 从 0 到 2)
betas = np.linspace(0, 2, 100)
expected_returns = risk_free_rate + betas * sml_slope
plt.plot(betas, expected_returns, 'b-', linewidth=2, label='Security Market Line (SML)')

# 标注无风险资产点 (beta=0)
plt.scatter(0, risk_free_rate, color='black', s=80, zorder=5)
plt.annotate(f'Risk-free\n({0:.2f}, {risk_free_rate:.1f}%)',
             xy=(0, risk_free_rate), xytext=(0.15, risk_free_rate - 0.5),
             arrowprops=dict(arrowstyle='->', color='gray'), fontsize=9)

# 标注市场组合点 (beta=1)
plt.scatter(1, market_return, color='black', s=80, zorder=5)
plt.annotate(f'Market\n({1:.2f}, {market_return:.1f}%)',
             xy=(1, market_return), xytext=(1.05, market_return + 0.5),
             arrowprops=dict(arrowstyle='->', color='gray'), fontsize=9)

# 标注股票 X, Y, Z
colors = ['red', 'green', 'purple']
for i, (name, data) in enumerate(stocks.items()):
    beta_val = data['beta']
    ret_val = data['return']
    plt.scatter(beta_val, ret_val, color=colors[i], s=80, zorder=5, label=f'{name} (β={beta_val:.2f}, E(R)={ret_val:.1f}%)')
    plt.annotate(name, xy=(beta_val, ret_val),
                 xytext=(beta_val + 0.07, ret_val + 0.3),
                 fontsize=10, color=colors[i], fontweight='bold')

# 坐标轴及标签
plt.xlabel('Beta (β)', fontsize=12)
plt.ylabel('Expected Return (%)', fontsize=12)
plt.title('Security Market Line (SML)', fontsize=14)
plt.xlim(0, 2)
plt.ylim(0, 20)
plt.xticks(np.arange(0, 2.1, 0.25))
plt.yticks(np.arange(0, 21, 2.5))
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(loc='upper left', fontsize=9)

# 保存图片
plt.tight_layout()
plt.savefig(result['figure_path'], dpi=150)
plt.close()

# 输出结果
print("Result dictionary:")
for key, value in result.items():
    print(f"  {key}: {value}")
