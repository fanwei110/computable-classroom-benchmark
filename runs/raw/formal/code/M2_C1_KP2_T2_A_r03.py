import matplotlib.pyplot as plt
import numpy as np

# ======== 可调参数 ========
rf = 0.023          # 无风险利率 2.3%
market_er = 0.094   # 市场期望收益 9.4%
# =========================

# 计算 SML 斜率 = 市场风险溢价
sml_slope = market_er - rf

# 计算 beta=1.27 对应的期望收益
beta_target = 1.27
er_at_beta_127 = rf + sml_slope * beta_target

# 生成 beta 值 [0, 2]
beta = np.linspace(0, 2, 100)
er = rf + sml_slope * beta   # SML 线

# 绘图
plt.figure(figsize=(8, 5))
plt.plot(beta, er, 'b-', linewidth=2, label='SML')
plt.axhline(y=rf, color='gray', linestyle='--', linewidth=0.8)
plt.axvline(x=1, color='gray', linestyle='--', linewidth=0.8)

# 市场组合点
plt.scatter(1, market_er, color='blue', s=80, zorder=5, label='Market (β=1)')

# 标出三个给定点
points = {'X': (0.62, 0.081), 'Y': (1.18, 0.131), 'Z': (1.51, 0.099)}
for name, (bx, ex) in points.items():
    plt.scatter(bx, ex, color='red', s=80, zorder=5)
    plt.text(bx + 0.02, ex, f'{name}({bx},{ex*100:.1f}%)', fontsize=9, color='red')

plt.xlabel('Beta (β)', fontsize=12)
plt.ylabel('Expected Return', fontsize=12)
plt.title(f'Security Market Line (rf={rf*100}%, E(Rm)={market_er*100}%)', fontsize=14)
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()

# 保存图片
figure_path = 'sml_plot.png'
plt.savefig(figure_path, dpi=150)
plt.close()

# 结果存入字典
result = {
    'sml_slope': sml_slope,           # 0.071
    'er_at_beta_127': er_at_beta_127, # 0.11317
    'figure_path': figure_path        # 'sml_plot.png'
}

print(result)
