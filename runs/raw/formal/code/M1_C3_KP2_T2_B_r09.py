import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# 参数
rf = 0.023
market_return = 0.094
betas = np.linspace(0, 2, 100)
sml_returns = rf + betas * (market_return - rf)

# 点数据
points = {
    'X': {'beta': 0.62, 'return': 0.081},
    'Y': {'beta': 1.18, 'return': 0.131},
    'Z': {'beta': 1.51, 'return': 0.099}
}

# 绘图
fig, ax = plt.subplots(figsize=(10, 6))
plt.subplots_adjust(bottom=0.2)

# SML线
ax.plot(betas, sml_returns, label='SML', color='blue')

# 标注点
for label, point in points.items():
    ax.scatter(point['beta'], point['return'], color='red')
    ax.annotate(label, (point['beta'], point['return']), textcoords="offset points", xytext=(10,5), ha='center')

# 标注rf和市场点
ax.scatter(0, rf, color='green', label='Risk-free (Rf)')
ax.scatter(1, market_return, color='purple', label='Market')

# 设置坐标轴
ax.set_xlabel('Beta')
ax.set_ylabel('Expected Return')
ax.set_title('Security Market Line (SML)')
ax.legend()
ax.grid(True)

# 保存图片
figure_path = 'sml_plot.png'
plt.savefig(figure_path)
plt.close()

# 结果字典
result = {
    'sml_slope': 0.071,
    'er_at_beta_127': 0.11317,
    'figure_path': figure_path
}

print(result)
