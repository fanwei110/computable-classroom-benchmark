import matplotlib.pyplot as plt
import numpy as np
import os

# 参数
rf = 0.023  # 无风险收益率
market_return = 0.094  # 市场收益率
betas = np.linspace(0, 2, 100)  # beta范围
sml_returns = rf + betas * (market_return - rf)  # SML线

# 计算SML斜率
sml_slope = market_return - rf

# 计算beta=1.27对应的预期收益
er_at_beta_127 = rf + 1.27 * (market_return - rf)

# 绘图
plt.figure(figsize=(10, 6))
plt.plot(betas, sml_returns, label='SML', color='blue')
plt.scatter([0, 1], [rf, market_return], color='red', label='Market & RF')  # RF和市场点
plt.scatter([0.62, 1.18, 1.51], [0.081, 0.131, 0.099], color='green', label='X, Y, Z')  # X, Y, Z点

# 标注点
plt.annotate('X (0.62, 8.1%)', xy=(0.62, 0.081), xytext=(0.5, 0.05),
             arrowprops=dict(facecolor='black', shrink=0.05))
plt.annotate('Y (1.18, 13.1%)', xy=(1.18, 0.131), xytext=(1.0, 0.15),
             arrowprops=dict(facecolor='black', shrink=0.05))
plt.annotate('Z (1.51, 9.9%)', xy=(1.51, 0.099), xytext=(1.3, 0.07),
             arrowprops=dict(facecolor='black', shrink=0.05))
plt.annotate('RF (0, 2.3%)', xy=(0, rf), xytext=(0.1, rf + 0.01),
             arrowprops=dict(facecolor='black', shrink=0.05))
plt.annotate('Market (1, 9.4%)', xy=(1, market_return), xytext=(0.8, market_return + 0.01),
             arrowprops=dict(facecolor='black', shrink=0.05))

plt.xlabel('Beta')
plt.ylabel('Expected Return')
plt.title('Security Market Line (SML)')
plt.legend()
plt.grid(True)

# 保存图片
figure_path = 'sml_plot.png'
plt.savefig(figure_path)
plt.close()

# 结果存入字典
result = {
    'sml_slope': sml_slope,
    'er_at_beta_127': er_at_beta_127,
    'figure_path': os.path.abspath(figure_path)
}

print(result)
