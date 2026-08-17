import matplotlib.pyplot as plt
import numpy as np

# ===== 可调参数（上课时修改这里即可） =====
rf = 2.3      # 无风险利率 (%)
rm = 9.4      # 市场期望收益 (%)
# ==========================================

# SML 方程
def sml(beta, rf, rm):
    return rf + beta * (rm - rf)

# Beta 范围
beta_vals = np.linspace(0, 2, 100)
er_vals = sml(beta_vals, rf, rm)

# 三个点
points = {'X': (0.62, 8.1),
          'Y': (1.18, 13.1),
          'Z': (1.51, 9.9)}

# 斜率与特定期望收益
sml_slope = rm - rf
beta_target = 1.27
er_target = sml(beta_target, rf, rm)

# 绘图
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(beta_vals, er_vals, 'b-', label=f'SML (rf={rf}%, rm={rm}%)')
ax.axhline(rf, color='gray', linestyle='--', alpha=0.5)
ax.axvline(0, color='gray', linestyle='--', alpha=0.5)

# 标记三个点
for label, (b, e) in points.items():
    ax.scatter(b, e, color='red', zorder=5)
    ax.text(b + 0.02, e + 0.3, f'{label} (β={b}, {e}%)', fontsize=9, color='red')

# 标注 β=1.27
ax.axvline(beta_target, color='green', linestyle=':', alpha=0.7)
ax.scatter(beta_target, er_target, color='green', zorder=5)
ax.text(beta_target + 0.02, er_target - 1.2, f'β={beta_target}: {er_target:.3f}%', color='green')

ax.set_xlabel('Beta (β)')
ax.set_ylabel('Expected Return (%)')
ax.set_title('Security Market Line (SML)')
ax.legend()
ax.grid(True, linestyle='--', alpha=0.6)
ax.set_xlim(0, 2)
ax.set_ylim(0, max(er_vals) + 3)

plt.tight_layout()
fig_path = 'sml.png'
plt.savefig(fig_path)
plt.show()

# ===== 所需输出结果 =====
result = {
    'sml_slope': sml_slope,
    'er_at_beta_127': er_target,
    'figure_path': fig_path
}
print(result)
