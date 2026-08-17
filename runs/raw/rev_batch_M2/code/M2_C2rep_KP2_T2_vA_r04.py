import numpy as np
import matplotlib.pyplot as plt

# ==============================================
# 可调参数：无风险利率与市场期望收益（年化）
# ==============================================
Rf = 0.023    # 2.3%
Rm = 0.094    # 9.4%

# --------------- 计算 SML ---------------
sml_slope = Rm - Rf                     # 证券市场线斜率

def capm_expected_return(beta):
    """CAPM 期望收益公式：E(R) = Rf + beta * (Rm - Rf)"""
    return Rf + sml_slope * beta

# 生成 beta 从 0 到 2 的线
beta_grid = np.linspace(0, 2, 200)
sml_line = capm_expected_return(beta_grid)

# --------------- 股票数据 ---------------
stocks = {
    'X': {'beta': 0.62, 'return': 0.081},
    'Y': {'beta': 1.18, 'return': 0.131},
    'Z': {'beta': 1.51, 'return': 0.099}
}

# --------------- 绘制 ---------------
plt.figure(figsize=(8, 5))
plt.plot(beta_grid, sml_line, color='blue', linewidth=2, label='SML')
for name, vals in stocks.items():
    plt.scatter(vals['beta'], vals['return'], color='red', s=60, zorder=5)
    plt.annotate(f"  {name}",
                 (vals['beta'], vals['return']),
                 textcoords="offset points",
                 xytext=(5, 5),
                 fontsize=12, fontweight='bold')

plt.xlabel('Beta', fontsize=12)
plt.ylabel('Expected Return', fontsize=12)
plt.title('Security Market Line (SML)', fontsize=14)
plt.legend(loc='lower right')
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()

# 保存图片
figure_filename = 'sml_plot.png'
plt.savefig(figure_filename, dpi=150)
print(f"图片已保存为：{figure_filename}")

# --------------- 报告 ---------------
beta_target = 1.27
er_at_beta_127 = capm_expected_return(beta_target)

print(f"SML 斜率：{sml_slope:.4f} （即市场风险溢价）")
print(f"Beta = {beta_target} 处的 CAPM 期望收益：{er_at_beta_127:.4f} = {er_at_beta_127*100:.2f}%")

# --------------- 填充 result 字典 ---------------
result = {
    'sml_slope': sml_slope,
    'er_at_beta_127': er_at_beta_127,
    'figure_path': figure_filename
}

# 输出 result 便于教师查看
print("\n输出字典 result：")
for key, value in result.items():
    print(f"  {key}: {value}")

# 如果希望直接显示图形（取消下面的注释）
# plt.show()
