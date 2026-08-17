import numpy as np
import matplotlib.pyplot as plt

# ----------------------------------------------------------------------
# 可调参数：无风险利率与市场期望收益（年化，小数形式）
# 教师可直接修改此处数值并重新运行
rf = 0.023          # 无风险利率 2.3%
rm = 0.094          # 市场期望收益 9.4%
# ----------------------------------------------------------------------

# SML 斜率（市场风险溢价）
sml_slope = rm - rf

# 绘制 SML 的 beta 范围
beta_vals = np.linspace(0, 2, 200)
sml_vals = rf + sml_slope * beta_vals

# 三只股票的数据
stocks = {
    'X': {'beta': 0.62, 'return': 0.081},
    'Y': {'beta': 1.18, 'return': 0.131},
    'Z': {'beta': 1.51, 'return': 0.099}
}

# ----------------------------- 绘图 -----------------------------
plt.figure(figsize=(10, 7))

# 证券市场线
plt.plot(beta_vals, sml_vals, 'b-', linewidth=2, label='Security Market Line (SML)')

# 无风险资产与市场组合
plt.scatter(0, rf, c='black', s=80, zorder=5, label='Risk‑free asset (β=0)')
plt.scatter(1, rm, c='green', s=80, zorder=5, label='Market portfolio (β=1)')

# 三只股票
colors = {'X': 'red', 'Y': 'orange', 'Z': 'purple'}
for name, data in stocks.items():
    beta = data['beta']
    ret = data['return']
    plt.scatter(beta, ret, c=colors[name], s=80, zorder=5)
    plt.annotate(
        f'{name}  (β={beta:.2f}, {ret*100:.2f}%)',
        xy=(beta, ret),
        xytext=(10, 10),
        textcoords='offset points',
        fontsize=10,
        arrowprops=dict(arrowstyle='->', color=colors[name], lw=1.5),
        bbox=dict(boxstyle='round,pad=0.3', fc='white', alpha=0.7)
    )

# 标注与网格
plt.xlabel('Beta (β)', fontsize=13)
plt.ylabel('Expected return', fontsize=13)
plt.title('Security Market Line (SML)', fontsize=15, fontweight='bold')
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend(loc='lower right', fontsize=10)
plt.tight_layout()

# 保存图形
figure_path = 'sml.png'
plt.savefig(figure_path, dpi=200, bbox_inches='tight')
plt.show()

# ------------------------- 所需报告的计算 -------------------------
# CAPM 期望收益 @ beta = 1.27
beta_target = 1.27
er_at_beta_127 = rf + sml_slope * beta_target

# -------------------------- 输出契约 --------------------------
result = {
    'sml_slope': sml_slope,
    'er_at_beta_127': er_at_beta_127,
    'figure_path': figure_path
}

print("=== CAPM 计算结果 ===")
print(f"SML 斜率（市场风险溢价）: {sml_slope*100:.2f}%")
print(f"beta = 1.27 处的期望收益: {er_at_beta_127*100:.2f}%")
print(f"图形已保存至: {figure_path}")
