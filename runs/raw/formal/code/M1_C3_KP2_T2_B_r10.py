import matplotlib.pyplot as plt
import numpy as np
import os

# 参数
rf = 0.023  # 无风险收益率
market_return = 0.094  # 市场收益率
betas = np.array([0, 2])  # beta范围
sml_returns = rf + betas * (market_return - rf)  # SML线

# 点X, Y, Z
points = {
    'X': {'beta': 0.62, 'return': 0.081},
    'Y': {'beta': 1.18, 'return': 0.131},
    'Z': {'beta': 1.51, 'return': 0.099}
}

# 计算斜率和beta=1.27对应的收益
sml_slope = market_return - rf
er_at_beta_127 = rf + 1.27 * sml_slope

# 绘图
plt.figure(figsize=(10, 6))
plt.plot(betas, sml_returns, label='SML', color='blue')
plt.scatter(points['X']['beta'], points['X']['return'], color='red', label='X')
plt.scatter(points['Y']['beta'], points['Y']['return'], color='green', label='Y')
plt.scatter(points['Z']['beta'], points['Z']['return'], color='purple', label='Z')
plt.text(points['X']['beta'], points['X']['return'], 'X', fontsize=12, verticalalignment='bottom')
plt.text(points['Y']['beta'], points['Y']['return'], 'Y', fontsize=12, verticalalignment='bottom')
plt.text(points['Z']['beta'], points['Z']['return'], 'Z', fontsize=12, verticalalignment='bottom')

plt.xlabel('Beta')
plt.ylabel('Expected Return')
plt.title('Security Market Line (SML)')
plt.legend()
plt.grid(True)

# 保存图片
figure_path = 'sml_plot.png'
plt.savefig(figure_path)
plt.close()

# 结果字典
result = {
    'sml_slope': sml_slope,
    'er_at_beta_127': er_at_beta_127,
    'figure_path': os.path.abspath(figure_path)
}

print(result)
