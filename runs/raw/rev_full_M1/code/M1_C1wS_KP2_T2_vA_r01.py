import numpy as np
import matplotlib.pyplot as plt
import os

# 参数设置
rf = 0.023  # 无风险利率
market_return = 0.094  # 市场期望收益

# 计算SML斜率
sml_slope = market_return - rf

# 计算beta=1.27处的期望收益
beta_127 = 1.27
er_at_beta_127 = rf + sml_slope * beta_127

# 创建beta范围
betas = np.linspace(0, 2, 100)
sml_returns = rf + sml_slope * betas

# 三个股票点的数据
stocks = {
    'X': {'beta': 0.62, 'return': 0.081},
    'Y': {'beta': 1.18, 'return': 0.131},
    'Z': {'beta': 1.51, 'return': 0.099}
}

# 创建图形
plt.figure(figsize=(10, 6))
plt.plot(betas, sml_returns, label='Security Market Line', color='blue')

# 标记三个股票点
for name, data in stocks.items():
    plt.scatter(data['beta'], data['return'], label=f'Stock {name}', s=100)
    plt.text(data['beta'] + 0.02, data['return'] - 0.005,
             f'{name} ({data["beta"]}, {data["return"]*100:.1f}%)',
             verticalalignment='top')

# 标记beta=1.27的点
plt.scatter(beta_127, er_at_beta_127, color='red', s=100, marker='x')
plt.text(beta_127 + 0.02, er_at_beta_127 - 0.005,
         f'Beta=1.27 ({er_at_beta_127*100:.2f}%)',
         verticalalignment='top', color='red')

# 图形设置
plt.title('Security Market Line (SML) with Sample Stocks')
plt.xlabel('Beta (β)')
plt.ylabel('Expected Return')
plt.grid(True)
plt.legend()
plt.xlim(0, 2)
plt.ylim(0, 0.2)

# 保存图形
figure_path = 'sml_plot.png'
plt.savefig(figure_path, dpi=300, bbox_inches='tight')
plt.close()

# 准备结果字典
result = {
    'sml_slope': sml_slope,
    'er_at_beta_127': er_at_beta_127,
    'figure_path': os.path.abspath(figure_path)
}

# 输出结果以便验证
print(result)
