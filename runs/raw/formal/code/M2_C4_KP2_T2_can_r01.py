import numpy as np
import matplotlib.pyplot as plt
import os

# ==================== 参数定义（可调） ====================
# 所有比率均使用小数表示，例如 0.05 表示 5%
rf = 0.023          # 无风险利率
market_return = 0.094  # 市场期望收益率

# ==================== 股票数据 ====================
# 股票名称、Beta、实际期望收益（小数）
stocks = {
    'X': {'beta': 0.62, 'return': 0.081},
    'Y': {'beta': 1.18, 'return': 0.131},
    'Z': {'beta': 1.51, 'return': 0.099}
}

# ==================== SML 计算 ====================
market_premium = market_return - rf          # 市场风险溢价，即 SML 斜率
sml_slope = market_premium                  # 按要求键名 'sml_slope'

# 计算 beta = 1.27 处的 CAPM 期望收益
beta_target = 1.27
er_at_beta_127 = rf + beta_target * market_premium

# ==================== 绘图 ====================
fig, ax = plt.subplots(figsize=(8, 6))

# --- 绘制证券市场线（SML） ---
beta_range = np.linspace(0, 2, 100)
sml_line = rf + beta_range * market_premium
ax.plot(beta_range, sml_line, 'b-', linewidth=2, label='SML')

# --- 标注无风险资产与市场组合（SML上的参考点） ---
ax.scatter(0, rf, color='blue', marker='o', s=80, zorder=5)
ax.annotate('Risk-free (Rf)', (0, rf), textcoords="offset points",
            xytext=(-10, 10), ha='center', fontsize=9, color='blue')
ax.scatter(1, market_return, color='blue', marker='o', s=80, zorder=5)
ax.annotate('Market (M)', (1, market_return), textcoords="offset points",
            xytext=(10, -15), ha='center', fontsize=9, color='blue')

# --- 绘制三只股票的点 ---
colors = {'X': 'red', 'Y': 'green', 'Z': 'darkorange'}
for name, data in stocks.items():
    beta_val = data['beta']
    ret_val = data['return']
    ax.scatter(beta_val, ret_val, color=colors[name], marker='D', s=100, zorder=6)
    ax.annotate(f'{name}\n(β={beta_val:.2f}, E(R)={ret_val:.3f})',
                (beta_val, ret_val), textcoords="offset points",
                xytext=(10, 15), ha='center', fontsize=9,
                color=colors[name],
                arrowprops=dict(arrowstyle='->', color=colors[name], lw=1.2))

# --- 图表修饰 ---
ax.set_xlabel('Beta (β)', fontsize=12)
ax.set_ylabel('Expected Return E(R)', fontsize=12)
ax.set_title('Security Market Line (SML) with Stocks X, Y, Z', fontsize=14)
ax.set_xlim(0, 2)
ax.set_ylim(0, 0.20)  # 纵轴范围适当放大以容纳所有点
ax.axhline(y=0, color='gray', linestyle='--', linewidth=0.5)
ax.grid(True, linestyle=':', alpha=0.7)
ax.legend(loc='lower right', fontsize=9)

# 将收益率以百分比形式显示在y轴刻度上（可选，便于阅读）
import matplotlib.ticker as mtick
ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda y, _: f'{y*100:.0f}%'))

plt.tight_layout()

# --- 保存图形 ---
figure_filename = 'sml_plot.png'
figure_path = os.path.join(os.getcwd(), figure_filename)
plt.savefig(figure_path, dpi=150)
plt.close()

# ==================== 输出结果字典 ====================
result = {
    'sml_slope': sml_slope,
    'er_at_beta_127': er_at_beta_127,
    'figure_path': figure_path
}

# 打印结果供课堂投屏展示
print("=" * 50)
print("CAPM / SML 分析结果")
print("=" * 50)
print(f"SML 斜率 (市场风险溢价) : {sml_slope:.5f}  ({sml_slope*100:.2f}%)")
print(f"Beta = {beta_target} 处的 CAPM 期望收益 : {er_at_beta_127:.5f}  ({er_at_beta_127*100:.2f}%)")
print(f"图形已保存至 : {figure_path}")
print("=" * 50)
print("结果字典 result:")
print(result)
