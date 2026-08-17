import numpy as np
import matplotlib.pyplot as plt
import os

# 参数设定
risk_free_rate = 0.023  # 无风险利率 2.3%
market_return = 0.094   # 市场期望收益 9.4%

# 证券市场线 (SML) 函数
def calculate_sml_return(beta, risk_free_rate, market_return):
    return risk_free_rate + beta * (market_return - risk_free_rate)

# 计算 SML 斜率
sml_slope = market_return - risk_free_rate

# 计算 beta=1.27 处的期望收益
beta_127 = 1.27
er_at_beta_127 = calculate_sml_return(beta_127, risk_free_rate, market_return)

# 生成 beta 从 0 到 2 的 SML 数据
betas = np.linspace(0, 2, 100)
sml_returns = calculate_sml_return(betas, risk_free_rate, market_return)

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
    plt.text(data['beta'] + 0.02, data['return'] + 0.002, stock,
             fontsize=12, verticalalignment='bottom')

# 标注无风险利率点
plt.scatter(0, risk_free_rate, color='red', s=100, label='Risk-free Rate')
plt.text(0.02, risk_free_rate + 0.002, 'Risk-free Rate',
         fontsize=12, verticalalignment='bottom')

# 标注市场组合点
plt.scatter(1, market_return, color='green', s=100, label='Market Portfolio')
plt.text(1.02, market_return + 0.002, 'Market Portfolio',
         fontsize=12, verticalalignment='bottom')

# 图形设置
plt.title('Security Market Line (SML) with Stocks X, Y, Z', fontsize=14)
plt.xlabel('Beta (β)', fontsize=12)
plt.ylabel('Expected Return', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend(fontsize=10)
plt.xlim(0, 2)
plt.ylim(0, 0.15)

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

# 输出结果（供教师查看）
print(result)
