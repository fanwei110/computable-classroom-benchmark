import matplotlib.pyplot as plt
import numpy as np
import os

# ==================== 可调参数（上课直接改这里） ====================
rf = 2.3 / 100          # 无风险利率
E_rm = 9.4 / 100        # 市场期望收益
# ==================================================================

# 计算 SML 斜率
sml_slope = E_rm - rf

# Beta 范围
beta = np.linspace(0, 2, 100)
sml = rf + sml_slope * beta

# 三个点
points = {
    'X': (0.62, 8.1 / 100),
    'Y': (1.18, 13.1 / 100),
    'Z': (1.51, 9.9 / 100)
}

# Beta=1.27 对应期望收益
beta_target = 1.27
er_at_beta_127 = rf + sml_slope * beta_target

# 画图
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(beta, sml, 'b-', linewidth=2, label='SML')
ax.axhline(y=rf, color='gray', linestyle='--', linewidth=0.8)
ax.axvline(x=1, color='gray', linestyle='--', linewidth=0.8)

# 标注三个点
colors = {'X': 'red', 'Y': 'green', 'Z': 'orange'}
for name, (b, er) in points.items():
    ax.scatter(b, er, color=colors[name], s=80, zorder=5)
    ax.annotate(f'{name}\n(β={b}, E(r)={er*100:.1f}%)', 
                (b, er), textcoords="offset points", xytext=(10,10),
                fontsize=9, color=colors[name], fontweight='bold')

# 标注 β=1.27
ax.axvline(x=beta_target, color='purple', linestyle=':', alpha=0.7)
ax.scatter(beta_target, er_at_beta_127, color='purple', s=60, zorder=5)
ax.annotate(f'β={beta_target}\nE(r)={er_at_beta_127*100:.2f}%',
            (beta_target, er_at_beta_127), textcoords="offset points", 
            xytext=(-10,-25), fontsize=9, color='purple')

# 轴标签、标题、图例
ax.set_xlabel('β (Beta)', fontsize=12)
ax.set_ylabel('Expected Return', fontsize=12)
ax.set_title(f'Security Market Line (rf={rf*100:.1f}%, E(rm)={E_rm*100:.1f}%)', fontsize=14)
ax.set_xlim(0, 2)
ax.set_ylim(0, max(E_rm, max(p[1] for p in points.values())) * 1.2)
# 把y轴刻度改为百分数显示
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y*100:.0f}%'))
ax.legend(loc='lower right')
ax.grid(True, linestyle=':', alpha=0.5)

plt.tight_layout()
figure_path = os.path.abspath('sml_plot.png')
plt.savefig(figure_path, dpi=150)
plt.close()

# 构建结果字典
result = {
    'sml_slope': round(sml_slope, 6),
    'er_at_beta_127': round(er_at_beta_127, 6),
    'figure_path': figure_path
}

# 输出结果（课堂上可以直接查看）
print("Result dictionary:")
print(result)
