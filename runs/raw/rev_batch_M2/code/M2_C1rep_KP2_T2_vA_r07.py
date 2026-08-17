import matplotlib.pyplot as plt
import numpy as np

# ==================== 可调参数（请在此修改） ====================
rf = 0.023          # 无风险利率
market_return = 0.094  # 市场期望收益
# =============================================================

# 计算SML斜率（市场风险溢价）
sml_slope = market_return - rf

# 给定的三个点
points = {
    'X': (0.62, 0.081),
    'Y': (1.18, 0.131),
    'Z': (1.51, 0.099)
}

# 计算 beta = 1.27 对应的期望收益
beta_target = 1.27
er_at_beta_127 = rf + beta_target * sml_slope

# 生成beta值范围用于画线
beta = np.linspace(0, 2, 100)
er = rf + beta * sml_slope

# 画图
plt.figure(figsize=(8, 6))
plt.plot(beta, er, 'b-', linewidth=2, label='SML')
plt.scatter(1, market_return, color='green', s=100, zorder=5, label='Market Portfolio')
for name, (b, r) in points.items():
    plt.scatter(b, r, color='red', s=80, zorder=5)
    plt.text(b + 0.02, r, f'{name}({b}, {r*100:.1f}%)', fontsize=10)

# 标注坐标轴和标题
plt.xlabel('Beta')
plt.ylabel('Expected Return')
plt.title(f'Security Market Line (rf={rf*100:.1f}%, E(Rm)={market_return*100:.1f}%)')
plt.axhline(y=rf, color='gray', linestyle='--', linewidth=1, label=f'Risk-free rate = {rf*100:.1f}%')
plt.xlim(0, 2)
plt.ylim(0, 0.20)
plt.grid(alpha=0.3)
plt.legend()
plt.tight_layout()

# 保存图片
figure_path = 'sml.png'
plt.savefig(figure_path, dpi=150)
plt.close()

# ================== 输出结果字典 ==================
result = {
    'sml_slope': sml_slope,                # 斜率（小数形式）
    'er_at_beta_127': er_at_beta_127,      # beta=1.27的期望收益（小数形式）
    'figure_path': figure_path             # 图片保存路径
}

print(result)
