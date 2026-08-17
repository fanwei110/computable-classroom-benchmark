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
expected_returns = risk_free_rate + beta_range * (market_return - risk_free_rate)

plt.figure(figsize=(10, 6))
plt.plot(beta_range, expected_returns, label='Security Market Line (SML)',
         color='blue', linestyle='-')

# 绘制股票点
for stock, data in stocks.items():
    plt.scatter(data['beta'], data['return'], label=f'Stock {stock}', s=100)
    plt.text(data['beta'] + 0.02, data['return'] - 0.005,
             f'{stock} (β={data["beta"]}, r={data["return"]*100:.1f}%)',
             fontsize=9, verticalalignment='top')

# 绘制无风险利率点
plt.scatter(0, risk_free_rate, color='red', label='Risk-free Rate', s=100)
plt.text(0.02, risk_free_rate - 0.003,
         f'Risk-free (β=0, r={risk_free_rate*100:.1f}%)',
         fontsize=9, verticalalignment='top')

# 绘制市场组合点
plt.scatter(1, market_return, color='green', label='Market Portfolio', s=100)
plt.text(1.02, market_return - 0.003,
         f'Market (β=1, r={market_return*100:.1f}%)',
         fontsize=9, verticalalignment='top')

# 图形设置
plt.title('Security Market Line (SML) with Stocks X, Y, Z', pad=20)
plt.xlabel('Beta (β)')
plt.ylabel('Expected Return')
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.xlim(0, 2)
plt.ylim(0, 0.15)

# 保存图形
figure_path = 'sml_plot.png'
plt.savefig(figure_path, dpi=300, bbox_inches='tight')
plt.close()

# 2. 计算斜率和特定beta的期望收益
sml_slope = market_return - risk_free_rate
er_at_beta_127 = risk_free_rate + 1.27 * sml_slope

# 3. 存储结果
result = {
    'sml_slope': sml_slope,
    'er_at_beta_127': er_at_beta_127,
    'figure_path': os.path.abspath(figure_path)
}

# 输出结果（供教师查看）
print("Result dictionary:")
print(result)
