import numpy as np
import matplotlib.pyplot as plt
import os

# 参数设定
risk_free_rate = 0.023  # 无风险利率 2.3%
market_return = 0.094   # 市场期望收益 9.4%

# 股票数据
stocks = {
    'X': {'beta': 0.62, 'return': 0.081},
    'Y': {'beta': 1.18, 'return': 0.131},
    'Z': {'beta': 1.51, 'return': 0.099}
}

# 1. 绘制证券市场线 (SML)
def plot_sml(rf, rm, stocks):
    # 生成 beta 值 (0 到 2)
    betas = np.linspace(0, 2, 100)
    # 计算 SML 上的期望收益
    expected_returns = rf + betas * (rm - rf)

    # 创建图形
    plt.figure(figsize=(10, 6))
    plt.plot(betas, expected_returns, label='Security Market Line (SML)', color='blue')

    # 绘制股票点
    for name, data in stocks.items():
        plt.scatter(data['beta'], data['return'], label=f'Stock {name}', s=100)
        plt.annotate(name, (data['beta'], data['return']),
                     textcoords="offset points", xytext=(10,5), ha='center')

    # 标记无风险利率点
    plt.scatter(0, rf, color='red', label='Risk-Free Rate', s=100)
    plt.annotate('RF', (0, rf), textcoords="offset points", xytext=(10,5), ha='center')

    # 标记市场组合点
    plt.scatter(1, rm, color='green', label='Market Portfolio', s=100)
    plt.annotate('M', (1, rm), textcoords="offset points", xytext=(10,5), ha='center')

    # 图形设置
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

    return figure_path

# 2. 计算 SML 斜率和 beta=1.27 处的期望收益
sml_slope = market_return - risk_free_rate
er_at_beta_127 = risk_free_rate + 1.27 * sml_slope

# 3. 生成图形
figure_path = plot_sml(risk_free_rate, market_return, stocks)

# 4. 保存结果
result = {
    'sml_slope': sml_slope,
    'er_at_beta_127': er_at_beta_127,
    'figure_path': os.path.abspath(figure_path)
}

# 输出结果（供教师使用）
print(result)
