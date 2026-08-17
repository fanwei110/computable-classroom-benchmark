import numpy as np
import matplotlib.pyplot as plt
import os

# 课程计算约定参数
risk_free_rate = 0.023  # 无风险利率 2.3%
market_return = 0.094   # 市场期望收益 9.4%

# 股票数据：名称, beta, 实际收益
stocks = [
    {'name': 'X', 'beta': 0.62, 'return': 0.081},
    {'name': 'Y', 'beta': 1.18, 'return': 0.131},
    {'name': 'Z', 'beta': 1.51, 'return': 0.099}
]

# 1. 绘制证券市场线 (SML)
beta_range = np.linspace(0, 2, 100)
expected_returns = risk_free_rate + beta_range * (market_return - risk_free_rate)

plt.figure(figsize=(10, 6))
plt.plot(beta_range, expected_returns, label='Security Market Line (SML)', color='blue')

# 标注三只股票
for stock in stocks:
    plt.scatter(stock['beta'], stock['return'], color='red', zorder=5)
    plt.annotate(stock['name'],
                 (stock['beta'], stock['return']),
                 textcoords="offset points",
                 xytext=(10,5),
                 ha='center')

plt.title('Security Market Line (CAPM)')
plt.xlabel('Beta')
plt.ylabel('Expected Return')
plt.grid(True)
plt.legend()

# 保存图形
figure_path = 'sml_plot.png'
plt.savefig(figure_path)
plt.close()

# 2. 参数化无风险利率与市场收益（已通过变量实现）

# 3. 报告 SML 斜率与 beta=1.27 处的期望收益
sml_slope = market_return - risk_free_rate
er_at_beta_127 = risk_free_rate + 1.27 * sml_slope

# 4. 填充 result 字典
result = {
    'sml_slope': sml_slope,
    'er_at_beta_127': er_at_beta_127,
    'figure_path': os.path.abspath(figure_path)
}

# 输出 result 以供课堂使用
print(result)
