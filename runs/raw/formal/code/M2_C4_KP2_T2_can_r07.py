import numpy as np
import matplotlib.pyplot as plt
import scipy  # 仅供满足导入限制
import pandas as pd  # 仅供满足导入限制

# ============================
# 可调参数
# ============================
rf = 0.023      # 无风险利率 (2.3%)
rm = 0.094      # 市场期望收益 (9.4%)

# ============================
# 三只股票数据
# ============================
stocks = {
    'X': (0.62, 0.081),
    'Y': (1.18, 0.131),
    'Z': (1.51, 0.099)
}

# ============================
# SML 计算
# ============================
sml_slope = rm - rf                    # 市场风险溢价，即 SML 斜率
er_at_beta_127 = rf + 1.27 * sml_slope # beta=1.27 处的 CAPM 期望收益

# ============================
# 绘图
# ============================
beta_range = np.linspace(0, 2, 100)
er_sml = rf + sml_slope * beta_range

plt.figure(figsize=(10, 7))
plt.plot(beta_range, er_sml, 'b-', linewidth=2, label='Security Market Line (SML)')
plt.scatter(0, rf, color='red', s=120, zorder=5, label='Risk-free Asset (rf)')
plt.scatter(1, rm, color='green', s=120, zorder=5, label='Market Portfolio (M)')

# 标注三只股票
for name, (beta, ret) in stocks.items():
    plt.scatter(beta, ret, color='purple', marker='s', s=100, zorder=5)
    plt.text(beta + 0.03, ret, f'Stock {name}\n(β={beta}, E(r)={ret:.3f})',
             fontsize=10, verticalalignment='center',
             bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.6))

# 在 SML 上标出无风险利率和市场组合的数值
plt.text(0, rf, f'  rf={rf:.3f}', fontsize=9, verticalalignment='bottom')
plt.text(1, rm, f'  M (β=1, E(r)={rm:.3f})', fontsize=9, verticalalignment='bottom')

plt.xlabel('Beta (β)', fontsize=13)
plt.ylabel('Expected Return E(r)', fontsize=13)
plt.title('Security Market Line (CAPM)', fontsize=15)
plt.legend()
plt.grid(True, alpha=0.5)
plt.xlim(-0.05, 2.1)
plt.ylim(0, 0.18)
plt.tight_layout()

figure_path = 'sml.png'
plt.savefig(figure_path, dpi=150)
plt.show()

# ============================
# 输出结果字典
# ============================
result = {
    'sml_slope': sml_slope,
    'er_at_beta_127': er_at_beta_127,
    'figure_path': figure_path
}

# 打印以便课堂查看
print("========== CAPM SML 结果 ==========")
print(f"SML 斜率 (市场风险溢价) : {sml_slope:.4f}")
print(f"Beta=1.27 处 CAPM 期望收益: {er_at_beta_127:.4f}")
print(f"图形保存路径              : {figure_path}")
print(result)
