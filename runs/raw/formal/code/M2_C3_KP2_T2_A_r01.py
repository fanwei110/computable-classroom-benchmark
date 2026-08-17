import matplotlib.pyplot as plt
import numpy as np

# ========== 可调参数（上课时可直接修改这两个值） ==========
rf = 0.023          # 无风险利率 (2.3%)
E_rm = 0.094        # 市场期望收益率 (9.4%)
# ======================================================

# 计算 SML 斜率（市场风险溢价）
sml_slope = E_rm - rf   # 0.071 (即 7.1%)

# 给定三个点
points = {
    'X': (0.62, 0.081),
    'Y': (1.18, 0.131),
    'Z': (1.51, 0.099)
}

# beta=1.27 对应的期望收益
beta_target = 1.27
er_at_beta_127 = rf + beta_target * sml_slope  # 0.11317 (11.317%)

# ========== 画图 ==========
fig, ax = plt.subplots(figsize=(8, 6))

# 绘制 SML 直线：beta 从 0 到 2
beta_range = np.linspace(0, 2, 100)
er_sml = rf + beta_range * sml_slope
ax.plot(beta_range, er_sml, 'b-', linewidth=2, label='SML')

# 标注三个点 X, Y, Z
for name, (b, er) in points.items():
    ax.scatter(b, er, color='red', zorder=5)
    ax.annotate(f'{name}\n(β={b}, E(r)={er:.1%})', (b, er),
                textcoords="offset points", xytext=(10, -10), ha='left',
                fontsize=9, bbox=dict(boxstyle='round,pad=0.3', fc='yellow', alpha=0.7))

# 标注 beta=1.27
ax.scatter(beta_target, er_at_beta_127, color='green', zorder=5)
ax.annotate(f'β=1.27\nE(r)={er_at_beta_127:.3%}', (beta_target, er_at_beta_127),
            textcoords="offset points", xytext=(-15, 15), ha='right',
            fontsize=9, color='green')

# 坐标轴和网格
ax.set_xlabel('Beta (β)', fontsize=12)
ax.set_ylabel('Expected Return E(r)', fontsize=12)
ax.set_title('Security Market Line (SML)', fontsize=14)
ax.axhline(y=rf, color='gray', linestyle='--', linewidth=1, alpha=0.5, label=f'rf = {rf:.1%}')
ax.axvline(x=1, color='gray', linestyle='--', linewidth=1, alpha=0.5, label='β = 1 (Market)')
ax.legend()
ax.grid(True, alpha=0.3)
ax.set_xlim(0, 2)
ax.set_ylim(0, 0.20)

# 保存图片
figure_path = 'sml.png'
fig.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close(fig)

# ========== 输出字典 ==========
result = {
    'sml_slope': sml_slope,            # 0.071
    'er_at_beta_127': er_at_beta_127,  # 0.11317
    'figure_path': figure_path         # 'sml.png'
}

print(result)
