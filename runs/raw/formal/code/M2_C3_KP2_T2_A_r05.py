import numpy as np
import matplotlib.pyplot as plt

# ================= 可调参数（上课直接改这里）=================
rf = 0.023        # 无风险利率 (2.3%)
rm = 0.094        # 市场期望收益 (9.4%)
# =========================================================

# 计算斜率
sml_slope = rm - rf

# 计算 beta=1.27 时的期望收益
beta_target = 1.27
er_at_beta_127 = rf + beta_target * sml_slope

# 生成 SML 直线（beta 从 0 到 2）
beta = np.linspace(0, 2, 100)
sml = rf + beta * sml_slope

# 三个需要标注的点
points = {
    'X': (0.62, 0.081),
    'Y': (1.18, 0.131),
    'Z': (1.51, 0.099)
}

# 画图
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(beta, sml, 'k-', linewidth=2, label='SML')
ax.set_xlabel('Beta', fontsize=12)
ax.set_ylabel('Expected Return', fontsize=12)
ax.set_title('Security Market Line (SML)', fontsize=14)
ax.grid(True, linestyle='--', alpha=0.6)
ax.set_xlim(0, 2)
ax.set_ylim(0, 0.16)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y:.1%}'))

# 标出 X, Y, Z
for name, (b, er) in points.items():
    ax.scatter(b, er, s=80, zorder=5)
    ax.annotate(f'{name}\n({b:.2f}, {er:.2%})',
                xy=(b, er), xytext=(10, 10),
                textcoords='offset points', fontsize=10,
                bbox=dict(boxstyle='round,pad=0.3', fc='yellow', alpha=0.8),
                arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))

ax.legend()
plt.tight_layout()

# 保存图片
figure_path = 'sml.png'
fig.savefig(figure_path, dpi=150)
plt.close(fig)

# ================= 输出契约 =================
result = {
    'sml_slope': sml_slope,            # 市场的风险溢价
    'er_at_beta_127': er_at_beta_127,  # beta=1.27 时的期望收益
    'figure_path': figure_path         # 图片保存路径
}

print(result)
