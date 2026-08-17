import numpy as np
import matplotlib.pyplot as plt
import os

# 课程计算约定参数
risk_free_rate = 0.023  # 无风险利率 2.3%
market_return = 0.094   # 市场期望收益 9.4%

# 证券市场线 (SML) 的斜率计算
sml_slope = market_return - risk_free_rate

# beta=1.27 处的 CAPM 期望收益
beta_target = 1.27
expected_return_at_beta_127 = risk_free_rate + beta_target * sml_slope

# 生成 beta 从 0 到 2 的 SML 数据点
betas = np.linspace(0, 2, 100)
sml_returns = risk_free_rate + betas * sml_slope

# 股票数据
stocks = {
    'X': {'beta': 0.62, 'return': 0.081},
    'Y': {'beta': 1.18, 'return': 0.131},
    'Z': {'beta': 1.51, 'return': 0.099}
}

# 绘图
plt.figure(figsize=(10, 6))
plt.plot(betas, sml_returns, label='Security Market Line (SML)', color='blue')

# 绘制股票点
for stock, data in stocks.items():
    plt.scatter(data['beta'], data['return'], label=f'Stock {stock}', s=100)
    plt.annotate(stock, (data['beta'], data['return']),
                 textcoords="offset points", xytext=(10,5), ha='center')

# 图形设置
plt.title('Security Market Line (CAPM)')
plt.xlabel('Beta')
plt.ylabel('Expected Return')
plt.xlim(0, 2)
plt.ylim(0, 0.15)
plt.grid(True)
plt.legend()
plt.tight_layout()

# 保存图形
figure_path = 'sml_plot.png'
plt.savefig(figure_path)
plt.close()

# 结果字典
result = {
    'sml_slope': sml_slope,
    'er_at_beta_127': expected_return_at_beta_127,
    'figure_path': os.path.abspath(figure_path)
}

# 输出结果（供课堂展示）
print(result)
