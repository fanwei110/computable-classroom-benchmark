import numpy as np
import matplotlib.pyplot as plt
import os

def calculate_and_plot_sml():
    # 参数设定
    risk_free_rate = 2.3  # 无风险利率（%）
    market_return = 9.4   # 市场期望收益（%）

    # 计算证券市场线(SML)的斜率
    sml_slope = (market_return - risk_free_rate) / 100  # 转换为小数

    # 计算beta=1.27处的CAPM期望收益
    beta_127 = 1.27
    er_at_beta_127 = risk_free_rate + beta_127 * (market_return - risk_free_rate)

    # 生成beta值范围
    betas = np.linspace(0, 2, 100)
    expected_returns = risk_free_rate + betas * (market_return - risk_free_rate)

    # 股票数据
    stocks = {
        'X': {'beta': 0.62, 'return': 8.1},
        'Y': {'beta': 1.18, 'return': 13.1},
        'Z': {'beta': 1.51, 'return': 9.9}
    }

    # 创建图形
    plt.figure(figsize=(10, 6))
    plt.plot(betas, expected_returns, label='Security Market Line', color='blue')

    # 绘制股票点
    for stock, data in stocks.items():
        plt.scatter(data['beta'], data['return'], label=f'Stock {stock}')
        plt.annotate(f'{stock} ({data["beta"]}, {data["return"]}%)',
                     (data['beta'], data['return']),
                     textcoords="offset points",
                     xytext=(10,5),
                     ha='center')

    # 绘制无风险利率点
    plt.scatter(0, risk_free_rate, color='green', label='Risk-free Rate')
    plt.annotate(f'Risk-free ({risk_free_rate}%)',
                 (0, risk_free_rate),
                 textcoords="offset points",
                 xytext=(10,5),
                 ha='center')

    # 绘制市场组合点
    plt.scatter(1, market_return, color='red', label='Market Portfolio')
    plt.annotate(f'Market ({market_return}%)',
                 (1, market_return),
                 textcoords="offset points",
                 xytext=(10,5),
                 ha='center')

    # 图形设置
    plt.title('Security Market Line (SML) with Stocks X, Y, Z')
    plt.xlabel('Beta (β)')
    plt.ylabel('Expected Return (%)')
    plt.legend()
    plt.grid(True)

    # 保存图形
    figure_path = 'sml_plot.png'
    plt.savefig(figure_path)
    plt.close()

    # 准备结果字典
    result = {
        'sml_slope': sml_slope,
        'er_at_beta_127': er_at_beta_127,
        'figure_path': os.path.abspath(figure_path)
    }

    return result

# 执行并输出结果
result = calculate_and_plot_sml()
print(result)
