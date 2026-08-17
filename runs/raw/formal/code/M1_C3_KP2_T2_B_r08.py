import matplotlib.pyplot as plt
import numpy as np
import os

# 参数
rf = 0.023  # 无风险收益率
market_return = 0.094  # 市场收益率
betas = [0, 2]  # beta范围
points = {
    'X': {'beta': 0.62, 'return': 0.081},
    'Y': {'beta': 1.18, 'return': 0.131},
    'Z': {'beta': 1.51, 'return': 0.099}
}

# 计算SML斜率和beta=1.27对应的收益率
sml_slope = market_return - rf
er_at_beta_127 = rf + 1.27 * sml_slope

# 绘制SML
plt.figure(figsize=(10, 6))
beta_range = np.linspace(0, 2, 100)
sml_returns = rf + beta_range * sml_slope
plt.plot(beta_range, sml_returns, label='SML', color='blue')

# 标注点X、Y、Z
for label, point in points.items():
    plt.scatter(point['beta'], point['return'], label=label, s=100)
    plt.text(point['beta'], point['return'], f' {label}', verticalalignment='bottom')

# 设置图形属性
plt.title('Security Market Line (SML)')
plt.xlabel('Beta')
plt.ylabel('Expected Return')
plt.xlim(0, 2)
plt.ylim(0, 0.15)
plt.grid(True)
plt.legend()

# 保存图形
figure_path = 'sml_plot.png'
plt.savefig(figure_path)
plt.close()

# 存储结果
result = {
    'sml_slope': sml_slope,
    'er_at_beta_127': er_at_beta_127,
    'figure_path': os.path.abspath(figure_path)
}

print(result)
