import matplotlib.pyplot as plt
import numpy as np
import os

# 参数设定
rf = 0.023  # 无风险收益率
market_return = 0.094  # 市场收益率
betas = np.linspace(0, 2, 100)  # beta范围
sml_returns = rf + betas * (market_return - rf)  # SML线

# 计算SML斜率
sml_slope = market_return - rf

# 计算beta=1.27对应的预期收益
er_at_beta_127 = rf + 1.27 * (market_return - rf)

# 绘制SML线
plt.figure(figsize=(10, 6))
plt.plot(betas, sml_returns, label='SML', color='blue')

# 标记rf和市场点
plt.scatter(0, rf, color='red', label=f'Risk-free (β=0, r={rf*100:.1f}%)')
plt.scatter(1, market_return, color='green', label=f'Market (β=1, r={market_return*100:.1f}%)')

# 标记X, Y, Z点
points = {
    'X': (0.62, 0.081),
    'Y': (1.18, 0.131),
    'Z': (1.51, 0.099)
}
for label, (beta, ret) in points.items():
    plt.scatter(beta, ret, color='purple')
    plt.text(beta, ret, f' {label}', verticalalignment='bottom')

# 图形设置
plt.title('Security Market Line (SML)')
plt.xlabel('Beta (β)')
plt.ylabel('Expected Return (r)')
plt.legend()
plt.grid(True)

# 保存图形
figure_path = 'sml_plot.png'
plt.savefig(figure_path)
plt.close()

# 存入结果字典
result = {
    'sml_slope': sml_slope,
    'er_at_beta_127': er_at_beta_127,
    'figure_path': os.path.abspath(figure_path)
}

print(result)
