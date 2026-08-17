import matplotlib.pyplot as plt
import numpy as np
import os

# ================= 可调参数 =================
rf = 0.023          # 无风险利率 (2.3%)
market_er = 0.094   # 市场期望收益率 (9.4%)
# ===========================================

# 三个标记点
points = {
    'X': (0.62, 0.081),
    'Y': (1.18, 0.131),
    'Z': (1.51, 0.099),
}

# 计算 SML 斜率（市场风险溢价）
sml_slope = market_er - rf

# beta=1.27 对应的期望收益
beta_val = 1.27
er_at_beta_127 = rf + beta_val * sml_slope

# 生成 SML 线
beta_range = np.linspace(0, 2, 100)
er_sml = rf + beta_range * sml_slope

# 绘图
plt.figure(figsize=(8, 6))
plt.plot(beta_range, er_sml, 'b-', linewidth=2, label='Security Market Line (SML)')

# 标记市场组合 M
plt.scatter(1, market_er, color='black', s=80, zorder=5, label='Market (M)')
plt.text(1.02, market_er, f'M (1, {market_er:.3f})', fontsize=9, va='bottom')

# 标记三个点 X, Y, Z
colors = {'X': 'red', 'Y': 'green', 'Z': 'orange'}
for name, (b, er) in points.items():
    plt.scatter(b, er, color=colors[name], s=80, zorder=5, label=f'{name} ({b}, {er:.3f})')
    plt.text(b + 0.02, er, f'{name}', fontsize=9, va='bottom')

# 标注轴和图例
plt.xlabel('Beta (β)')
plt.ylabel('Expected Return')
plt.title('Security Market Line')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)
plt.xlim(0, 2)
plt.ylim(0, 0.20)   # 可根据数据调整

# 保存图片
figure_path = os.path.abspath('sml_plot.png')
plt.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close()

# 组装结果字典
result = {
    'sml_slope': sml_slope,          # 0.071
    'er_at_beta_127': er_at_beta_127, # 0.11317
    'figure_path': figure_path
}

# 打印结果
print("SML斜率 (市场风险溢价):", result['sml_slope'])
print(f"Beta=1.27 对应的期望收益: {result['er_at_beta_127']:.5f}")
print("图片保存至:", result['figure_path'])
