import numpy as np
import matplotlib.pyplot as plt
import os

# 参数设定
risk_free_rate = 0.023  # 无风险利率
market_return = 0.094   # 市场期望收益

# 计算SML斜率
sml_slope = market_return - risk_free_rate

# 计算beta=1.27处的期望收益
beta_127 = 1.27
er_at_beta_127 = risk_free_rate + beta_127 * sml_slope

# 生成SML数据
betas = np.linspace(0, 2, 100)
expected_returns = risk_free_rate + betas * sml_slope

# 股票数据
stocks = {
    'X': {'beta': 0.62, 'return': 0.081},
    'Y': {'beta': 1.18, 'return': 0.131},
    'Z': {'beta': 1.51, 'return': 0.099}
}

# 创建图形
plt.figure(figsize=(10, 6))
plt.plot(betas, expected_returns, label='Security Market Line', color='blue')

# 绘制股票点
for stock, data in stocks.items():
    plt.scatter(data['beta'], data['return'], label=f'Stock {stock}', s=100)
    plt.annotate(stock,
                 (data['beta'], data['return']),
                 textcoords="offset points",
                 xytext=(10,5),
                 ha='center')

# 添加图形元素
plt.title('Security Market Line (SML) with Stocks X, Y, Z')
plt.xlabel('Beta (β)')
plt.ylabel('Expected Return')
plt.grid(True)
plt.legend()
plt.xlim(0, 2)
plt.ylim(0, 0.15)

# 保存图形
figure_path = 'sml_plot.png'
plt.savefig(figure_path)
plt.close()

# 准备结果
result = {
    'sml_slope': sml_slope,
    'er_at_beta_127': er_at_beta_127,
    'figure_path': os.path.abspath(figure_path)
}

# 输出结果（供课堂展示）
print("SML斜率:", result['sml_slope'])
print("Beta=1.27处的期望收益:", result['er_at_beta_127'])
print("图形已保存至:", result['figure_path'])
