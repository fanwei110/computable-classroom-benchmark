import matplotlib.pyplot as plt
import numpy as np

# 可调参数
rf = 0.023      # 无风险利率
rm = 0.094      # 市场期望收益

# SML 直线
beta_vals = np.linspace(0, 2, 100)
er_vals = rf + beta_vals * (rm - rf)

# 点
points = {
    'X': (0.62, 0.081),
    'Y': (1.18, 0.131),
    'Z': (1.51, 0.099),
}

# 绘图
plt.figure(figsize=(8, 5))
plt.plot(beta_vals, er_vals, 'k-', label='SML')
plt.scatter(1, rm, color='blue', zorder=5)
plt.text(1, rm, f'Market\n(1, {rm:.1%})', ha='left', va='bottom')
for label, (b, er) in points.items():
    plt.scatter(b, er, zorder=5)
    plt.text(b, er, f'{label}\n({b}, {er:.1%})', ha='left', va='bottom')
plt.xlabel('Beta')
plt.ylabel('Expected Return')
plt.title('Security Market Line')
plt.axhline(rf, color='gray', linestyle='--', linewidth=0.8)
plt.axvline(0, color='gray', linestyle='--', linewidth=0.8)
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend()
plt.tight_layout()
figure_path = 'sml.png'
plt.savefig(figure_path, dpi=150)

# 计算
sml_slope = rm - rf
er_at_beta_127 = rf + 1.27 * sml_slope

result = {
    'sml_slope': sml_slope,
    'er_at_beta_127': er_at_beta_127,
    'figure_path': figure_path,
}
result
