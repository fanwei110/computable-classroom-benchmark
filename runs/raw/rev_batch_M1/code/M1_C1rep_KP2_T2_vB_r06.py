import numpy as np
import matplotlib.pyplot as plt
import os

# 参数
rf = 0.023  # 无风险收益率
market_return = 0.094  # 市场收益率
betas = np.linspace(0, 2, 100)  # beta范围
assets = {
    'X': {'beta': 0.62, 'return': 0.081},
    'Y': {'beta': 1.18, 'return': 0.131},
    'Z': {'beta': 1.51, 'return': 0.099}
}

# 计算SML线上的预期收益率
sml_returns = rf + betas * (market_return - rf)

# 计算SML斜率
sml_slope = (market_return - rf) / (1 - 0)  # beta从0到1的斜率

# 计算beta=1.27对应的预期收益率
er_at_beta_127 = rf + 1.27 * (market_return - rf)

# 绘图
plt.figure(figsize=(10, 6))
plt.plot(betas, sml_returns, label='SML', color='blue')
plt.scatter([asset['beta'] for asset in assets.values()],
            [asset['return'] for asset in assets.values()],
            color=['red', 'green', 'purple'], zorder=5)

# 标注点
for name, asset in assets.items():
    plt.text(asset['beta'], asset['return'], f' {name}', verticalalignment='bottom')

plt.scatter(0, rf, color='black', label=f'Risk-free (β=0, r={rf*100:.1f}%)')
plt.scatter(1, market_return, color='orange', label=f'Market (β=1, r={market_return*100:.1f}%)')

plt.xlabel('Beta (β)')
plt.ylabel('Expected Return')
plt.title('Security Market Line (SML)')
plt.legend()
plt.grid(True)

# 保存图片
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
