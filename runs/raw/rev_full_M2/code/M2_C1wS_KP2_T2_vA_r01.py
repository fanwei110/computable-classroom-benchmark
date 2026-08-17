import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import os

# ========================
# 可调参数（无风险利率与市场期望收益）
# ========================
rf = 0.023        # 无风险利率，例如 2.3%
rm = 0.094        # 市场期望收益，例如 9.4%

# ========================
# 计算 SML 斜率与特定期望收益
# ========================
sml_slope = rm - rf                     # 市场风险溢价 / SML 斜率
beta_127 = 1.27
er_at_127 = rf + beta_127 * sml_slope   # beta=1.27 时的期望收益

# ========================
# 准备 SML 数据
# ========================
beta = np.linspace(0, 2, 100)
sml = rf + beta * sml_slope

# 三只股票的点：X, Y, Z
points = {
    'X': (0.62, 0.081),
    'Y': (1.18, 0.131),
    'Z': (1.51, 0.099)
}

# ========================
# 绘图
# ========================
fig, ax = plt.subplots(figsize=(8, 6))
ax.plot(beta, sml, 'b-', linewidth=2, label='SML')

# 颜色设置
colors = {'X': 'red', 'Y': 'green', 'Z': 'orange'}
for label, (b, er) in points.items():
    ax.scatter(b, er, color=colors[label], s=100, zorder=5,
               edgecolors='black', linewidths=0.8)
    ax.annotate(f'{label}\nβ={b:.2f}, E(r)={er*100:.2f}%',
                (b, er), textcoords="offset points",
                xytext=(12, 12), fontsize=9,
                color=colors[label],
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.7))

# 坐标轴与刻度
ax.set_xlabel('Beta')
ax.set_ylabel('Expected Return')
ax.set_title('Security Market Line (SML)')
ax.set_xlim(0, 2)
ax.set_ylim(0, 0.20)                     # 0% ~ 20%
ax.yaxis.set_major_formatter(mticker.PercentFormatter(1.0))  # 小数 -> 百分比显示
ax.legend()
ax.grid(True, linestyle='--', alpha=0.7)

# ========================
# 保存图像
# ========================
figure_path = 'sml.png'
fig.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close(fig)

# ========================
# 填充输出契约 result 字典
# ========================
result = {
    'sml_slope': sml_slope,                      # 斜率（小数形式）
    'er_at_beta_127': er_at_127,                 # beta=1.27 的期望收益（小数形式）
    'figure_path': os.path.abspath(figure_path)  # 图像绝对路径
}

# 课堂查看（可选）
print("证券投资学 — 课堂演示结果")
print(f"SML 斜率（市场风险溢价）: {sml_slope:.4f} = {sml_slope*100:.2f}%")
print(f"Beta = 1.27 的期望收益: {er_at_127:.4f} = {er_at_127*100:.2f}%")
print(f"图形已保存至: {result['figure_path']}")
