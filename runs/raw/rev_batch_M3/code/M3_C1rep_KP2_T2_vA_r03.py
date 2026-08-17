import matplotlib.pyplot as plt
import numpy as np

# ================= 可调参数区 =================
rf = 0.023       # 无风险利率
rm = 0.094       # 市场期望收益
# ============================================

# 计算 SML 斜率与指定 Beta 的期望收益
sml_slope = rm - rf
beta_target = 1.27
er_at_beta_127 = rf + beta_target * sml_slope

# 定义三个点的坐标 (Beta, 期望收益)
points = {
    'X': (0.62, 0.081),
    'Y': (1.18, 0.131),
    'Z': (1.51, 0.099)
}

# 生成 SML 线的数据
betas = np.linspace(0, 2, 100)
sml_ers = rf + betas * sml_slope

# 开始绘图
plt.figure(figsize=(10, 7))
plt.plot(betas, sml_ers * 100, label='Security Market Line (SML)', color='blue', linewidth=2)

# 标出市场组合点 M (Beta=1)
plt.scatter(1, rm * 100, color='black', marker='D', s=80, zorder=5, label='Market Portfolio (M)')
plt.text(1.03, rm * 100 + 0.3, f'M (1.0, {rm*100:.1f}%)', fontsize=11)

# 标出 X, Y, Z 三个点
colors = {'X': 'red', 'Y': 'green', 'Z': 'purple'}
for name, (b, er) in points.items():
    plt.scatter(b, er * 100, color=colors[name], s=80, zorder=5)
    plt.text(b + 0.03, er * 100 + 0.4, f'{name} ({b}, {er*100:.1f}%)', fontsize=11, color=colors[name])

# 图表美化
plt.title(f'Security Market Line\n$r_f$={rf*100:.1f}%, $E(R_m)$={rm*100:.1f}%, Slope={sml_slope*100:.1f}%', fontsize=14)
plt.xlabel('Beta ($\\beta$)', fontsize=12)
plt.ylabel('Expected Return (%)', fontsize=12)
plt.xlim(0, 2.1)
plt.ylim(0, 16)
plt.axhline(rf*100, color='grey', linestyle='--', linewidth=0.8, alpha=0.7)
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend(fontsize=11)

# 保存图片
figure_path = 'sml_plot.png'
plt.savefig(figure_path, dpi=300, bbox_inches='tight')
plt.close()

# ================= 输出契约 =================
result = {
    'sml_slope': round(sml_slope, 4),
    'er_at_beta_127': round(er_at_beta_127, 4),
    'figure_path': figure_path
}

print(result)
