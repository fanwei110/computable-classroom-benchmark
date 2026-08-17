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

# 1. 绘制证券市场线(SML)
def plot_sml(rf, rm, stocks):
    # 生成beta值范围
    betas = np.linspace(0, 2, 100)
    # 计算SML上的期望收益
    expected_returns = rf + betas * (rm - rf)

    # 创建图形
    plt.figure(figsize=(10, 6))
    plt.plot(betas, expected_returns, label='Security Market Line', color='blue')

    # 绘制股票点
    for name, data in stocks.items():
        plt.scatter(data['beta'], data['return'], label=f'Stock {name}', s=100)
        plt.text(data['beta'] + 0.02, data['return'] + 0.002, name,
                 fontsize=10, verticalalignment='bottom')

    # 标注无风险利率点
    plt.scatter(0, rf, color='red', label='Risk-free Rate', s=100)
    plt.text(0.02, rf + 0.002, 'Risk-free', fontsize=10)

    # 标注市场组合点
    plt.scatter(1, rm, color='green', label='Market Portfolio', s=100)
    plt.text(1.02, rm + 0.002, 'Market', fontsize=10)

    # 图形设置
    plt.title('Security Market Line (SML) with Stocks X, Y, Z')
    plt.xlabel('Beta (β)')
    plt.ylabel('Expected Return')
    plt.xlim(0, 2)
    plt.ylim(0, 0.15)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()

    # 保存图形
    figure_path = 'sml_plot.png'
    plt.savefig(figure_path, dpi=300, bbox_inches='tight')
    plt.close()

    return figure_path

# 2. 参数化处理（已通过函数参数实现）

# 3. 计算斜率和特定beta的期望收益
sml_slope = market_return - risk_free_rate
er_at_beta_127 = risk_free_rate + 1.27 * sml_slope

# 执行绘图
figure_path = plot_sml(risk_free_rate, market_return, stocks)

# 4. 保存结果
result = {
    'sml_slope': sml_slope,
    'er_at_beta_127': er_at_beta_127,
    'figure_path': os.path.abspath(figure_path)
}

# 输出结果以供验证
print(result)
