import numpy as np
import matplotlib.pyplot as plt
import os

# 参数设置
risk_free_rate = 0.023  # 无风险利率 2.3%
market_return = 0.094   # 市场期望收益 9.4%

# 股票数据
stocks = {
    'X': {'beta': 0.62, 'return': 0.081},
    'Y': {'beta': 1.18, 'return': 0.131},
    'Z': {'beta': 1.51, 'return': 0.099}
}

# 1. 绘制证券市场线 (SML)
beta_range = np.linspace(0, 2, 100)
sml_returns = risk_free_rate + beta_range * (market_return - risk_free_rate)

plt.figure(figsize=(10, 6))
plt.plot(beta_range, sml_returns, label='Security Market Line (SML)', color='blue')

# 标注股票点
for stock, data in stocks.items():
    plt.scatter(data['beta'], data['return'], label=f'Stock {stock}', s=100)
    plt.text(data['beta'] + 0.02, data['return'] - 0.005, stock,
             fontsize=10, verticalalignment='top')

# 图形设置
plt.title('Security Market Line (CAPM) with Stocks X, Y, Z')
plt.xlabel('Beta (β)')
plt.ylabel('Expected Return')
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()
plt.xlim(0, 2)
plt.ylim(0, 0.15)

# 保存图形
figure_path = 'sml_plot.png'
plt.savefig(figure_path)
plt.close()

# 3. 计算斜率和 beta=1.27 处的期望收益
sml_slope = market_return - risk_free_rate
er_at_beta_127 = risk_free_rate + 1.27 * sml_slope

# 输出结果
result = {
    'sml_slope': sml_slope,
    'er_at_beta_127': er_at_beta_127,
    'figure_path': os.path.abspath(figure_path)
}

# 打印结果以便验证
print(result)
