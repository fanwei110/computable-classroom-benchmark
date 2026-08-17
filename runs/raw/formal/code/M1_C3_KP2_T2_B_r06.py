import matplotlib.pyplot as plt
import numpy as np
import os

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
plt.figure(figsize=(10, 6))
plt.plot(betas, sml_returns, label='SML', color='blue')
plt.scatter([p['beta'] for p in points.values()], [p['return'] for p in points.values()],
            color=['red', 'green', 'purple'], zorder=5)

# 标注点
for label, p in points.items():
    plt.annotate(label, (p['beta'], p['return']), textcoords="offset points", xytext=(10,5), ha='center')

plt.axhline(y=rf, color='gray', linestyle='--', label=f'Rf = {rf*100:.1f}%')
plt.axvline(x=1, color='gray', linestyle='--', label=f'Market (β=1, E(Rm)={market_return*100:.1f}%)')
plt.xlabel('Beta')
plt.ylabel('Expected Return')
plt.title('Security Market Line (SML)')
plt.legend()
plt.grid(True)

# 保存图像
figure_path = 'sml_plot.png'
plt.savefig(figure_path)
plt.close()

# 结果字典
result = {
    'sml_slope': market_return - rf,  # 斜率 = E(Rm) - Rf
    'er_at_beta_127': rf + 1.27 * (market_return - rf),
    'figure_path': os.path.abspath(figure_path)
}

print(result)
