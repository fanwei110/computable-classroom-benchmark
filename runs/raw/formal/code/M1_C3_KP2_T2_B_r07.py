import numpy as np
import matplotlib.pyplot as plt
import os

# 参数
rf = 0.023  # 无风险收益率
market_return = 0.094  # 市场收益率
betas = np.linspace(0, 2, 100)  # beta范围
sml_returns = rf + betas * (market_return - rf)  # SML线

# 点X, Y, Z
points = {
    'X': {'beta': 0.62, 'return': 0.081},
    'Y': {'beta': 1.18, 'return': 0.131},
    'Z': {'beta': 1.51, 'return': 0.099}
}

# 绘图
plt.figure(figsize=(10, 6))
plt.plot(betas, sml_returns, label='SML', color='blue')
plt.scatter([p['beta'] for p in points.values()],
            [p['return'] for p in points.values()],
            color='red')
for label, point in points.items():
    plt.text(point['beta'], point['return'], label, fontsize=12, verticalalignment='bottom')

plt.xlabel('Beta')
plt.ylabel('Expected Return')
plt.title('Security Market Line (SML)')
plt.grid(True)
plt.legend()

# 保存图片
figure_path = 'sml_plot.png'
plt.savefig(figure_path)
plt.close()

# 结果
result = {
    'sml_slope': market_return - rf,  # 斜率 = 市场风险溢价
    'er_at_beta_127': rf + 1.27 * (market_return - rf),  # beta=1.27对应的收益
    'figure_path': os.path.abspath(figure_path)
}

print(result)
