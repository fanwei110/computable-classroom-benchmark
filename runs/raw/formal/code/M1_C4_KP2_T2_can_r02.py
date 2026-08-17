import numpy as np
import matplotlib.pyplot as plt
import os

# 参数设定
risk_free_rate = 0.023  # 无风险利率 2.3%
market_return = 0.094   # 市场期望收益 9.4%

# 计算SML斜率
sml_slope = market_return - risk_free_rate

# 计算beta=1.27处的期望收益
beta_127 = 1.27
er_at_beta_127 = risk_free_rate + beta_127 * sml_slope

# 生成beta值范围 (0到2)
betas = np.linspace(0, 2, 100)
# 计算对应的期望收益 (SML线)
expected_returns = risk_free_rate + betas * sml_slope

# 股票数据
stocks = {
    'X': {'beta': 0.62, 'return': 0.081},
    'Y': {'beta': 1.18, 'return': 0.131},
    'Z': {'beta': 1.51, 'return': 0.099}
}

# 创建图形
plt.figure(figsize=(10, 6))
plt.plot(betas, expected_returns, label='Security Market Line (SML)', color='blue')

# 绘制股票点
for stock, data in stocks.items():
    plt.scatter(data['beta'], data['return'], label=f'Stock {stock}', s=100)
    plt.text(data['beta'] + 0.02, data['return'] + 0.002, stock,
             fontsize=10, ha='left', va='bottom')

# 标注无风险利率点
plt.scatter(0, risk_free_rate, color='red', label='Risk-free Rate', s=100)
plt.text(0.02, risk_free_rate + 0.002, 'Risk-free',
         fontsize=10, ha='left', va='bottom')

# 标注市场组合点
plt.scatter(1, market_return, color='green', label='Market Portfolio', s=100)
plt.text(1.02, market_return + 0.002, 'Market',
         fontsize=10, ha='left', va='bottom')

# 图形设置
plt.title('Security Market Line (CAPM)')
plt.xlabel('Beta (Systematic Risk)')
plt.ylabel('Expected Return')
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
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

# 输出结果以供验证
print(result)
