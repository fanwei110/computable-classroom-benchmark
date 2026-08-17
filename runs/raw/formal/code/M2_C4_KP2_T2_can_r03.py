import numpy as np
import matplotlib.pyplot as plt

# ==========================
# 可调参数（用小数表示）
# ==========================
Rf = 0.023          # 无风险利率 2.3%
E_Rm = 0.094        # 市场期望收益 9.4%

# ==========================
# 计算 SML
# ==========================
sml_slope = E_Rm - Rf                     # 市场风险溢价，即 SML 斜率

beta_range = np.linspace(0, 2, 100)       # beta 从 0 到 2
sml_line = Rf + sml_slope * beta_range    # 证券市场线

# ==========================
# 三只股票的数据 (beta, 期望收益)
# ==========================
stocks = {
    'X': (0.62, 0.081),
    'Y': (1.18, 0.131),
    'Z': (1.51, 0.099)
}

# ==========================
# 绘图
# ==========================
plt.figure(figsize=(8, 5))
plt.plot(beta_range, sml_line, 'b-', label='SML', linewidth=2)

# 绘制股票点并标注
for name, (beta, ret) in stocks.items():
    plt.scatter(beta, ret, color='red', zorder=5)
    plt.annotate(name, (beta, ret),
                 textcoords="offset points",
                 xytext=(0, 10),
                 ha='center',
                 fontsize=10,
                 color='red')

# 标示无风险利率和市场组合点（可选，使图更清晰）
plt.scatter(0, Rf, color='green', zorder=5)
plt.annotate('Rf', (0, Rf),
             textcoords="offset points",
             xytext=(0, 10),
             ha='center', fontsize=9, color='green')

plt.scatter(1, E_Rm, color='green', zorder=5)
plt.annotate('M', (1, E_Rm),
             textcoords="offset points",
             xytext=(0, 10),
             ha='center', fontsize=9, color='green')

# 添加水平虚线便于观察
plt.axhline(y=Rf, color='grey', linestyle='--', alpha=0.6)
plt.axvline(x=1, color='grey', linestyle='--', alpha=0.6)

plt.xlabel('Beta')
plt.ylabel('Expected Return')
plt.title('Security Market Line (SML)')
plt.legend(loc='lower right')
plt.grid(alpha=0.3)
plt.tight_layout()

# 保存图形
figure_path = 'sml_plot.png'
plt.savefig(figure_path, dpi=150)
plt.close()   # 若需显示可改为 plt.show()

# ==========================
# 计算指定 beta 下的 CAPM 期望收益
# ==========================
beta_target = 1.27
er_at_beta_127 = Rf + sml_slope * beta_target

# ==========================
# 结果字典
# ==========================
result = {
    'sml_slope': sml_slope,
    'er_at_beta_127': er_at_beta_127,
    'figure_path': figure_path
}

# 输出到控制台（方便课堂查看）
print(result)
