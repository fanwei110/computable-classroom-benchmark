import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

def calculate_historical_var():
    # 读取数据
    df = pd.read_csv('data/market_snapshot_v1.csv')

    # 计算日收益率
    fund_returns = df['fund'].pct_change().dropna()

    # 头寸金额
    position = 1_000_000

    # 计算日损益
    daily_pnl = fund_returns * position

    # 可调置信水平（默认95%）
    confidence_level = 0.95

    # 计算历史VaR
    var = -np.percentile(daily_pnl, 100 * (1 - confidence_level))

    # 绘制直方图
    plt.figure(figsize=(10, 6))
    plt.hist(daily_pnl, bins=50, alpha=0.75, edgecolor='black')

    # 添加VaR线
    plt.axvline(x=-var, color='red', linestyle='--', label=f'{confidence_level*100:.0f}% 1-day Historical VaR: {var:,.2f}')

    plt.title('Daily P&L Distribution with Historical VaR')
    plt.xlabel('Daily P&L (RMB)')
    plt.ylabel('Frequency')
    plt.legend()
    plt.grid(True, alpha=0.3)

    # 保存图片
    if not os.path.exists('output'):
        os.makedirs('output')
    figure_path = 'output/historical_var_plot.png'
    plt.savefig(figure_path)
    plt.close()

    # 准备结果
    result = {
        'hist_var_95_1d': var,
        'figure_path': figure_path
    }

    return result

# 执行计算
result = calculate_historical_var()
print(result)
