import matplotlib.pyplot as plt
import numpy as np

# 可调参数（可按上课需要修改）
rf = 0.023          # 无风险利率（小数）
rm = 0.094          # 市场期望收益（小数）

# --- 计算 SML 斜率和特定 beta 的期望收益 ---
sml_slope = rm - rf
beta_target = 1.27
er_at_beta_127 = rf + beta_target * sml_slope

# --- 画图 ---
beta_range = np.linspace(0, 2, 100)
er_range = rf + beta_range * sml_slope

points = {
    'X': (0.62, 0.081),
    'Y': (1.18, 0.131),
    'Z': (1.51, 0.099)
}

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(beta_range, er_range * 100, 'b-', label=f'SML (rf={rf*100:.1f}%, E(rm)={rm*100:.1f}%)')

# 标出三个点
colors = {'X': 'red', 'Y': 'green', 'Z': 'orange'}
for label, (b, e) in points.items():
    ax.scatter(b, e * 100, color=colors[label], zorder=5)
    ax.text(b + 0.02, e * 100 + 0.2, f'{label}({b:.2f}, {e*100:.1f}%)',
            fontsize=9, color=colors[label])

ax.set_xlabel('Beta')
ax.set_ylabel('Expected Return (%)')
ax.set_title('Security Market Line (SML)')
ax.legend()
ax.grid(True, alpha=0.3)
ax.set_xlim(0, 2)
ax.set_ylim(0, 20)

# 保存图片
figure_path = 'sml.png'
fig.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close(fig)

# --- 按要求存入字典 ---
result = {
    'sml_slope': sml_slope,                 # 0.071
    'er_at_beta_127': er_at_beta_127,       # 约 0.11317
    'figure_path': figure_path              # 'sml.png'
}

# 打印结果（便于查看）
print(result)
