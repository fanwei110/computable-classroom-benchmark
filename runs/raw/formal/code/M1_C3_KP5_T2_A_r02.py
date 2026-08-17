import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

def calculate_historical_var(confidence_level=0.95):
    # 读取数据
    df = pd.read_csv('data/market_snapshot_v1.csv')

    # 计算日收益率
    returns = df['fund'].pct_change().dropna()

    # 计算日损益（头寸100万元）
    position = 1_000_000
    pnl = returns * position

    # 计算历史VaR
    var = -np.percentile(pnl, 100 * (1 - confidence_level))

    # 绘制直方图
    plt.figure(figsize=(10, 6))
    plt.hist(pnl, bins=50, alpha=0.75, edgecolor='black')
    plt.axvline(x=-var, color='r', linestyle='--', label=f'{confidence_level*100:.0f}% 1-day Historical VaR: {var:,.2f}元')
    plt.title('Daily P&L Distribution')
    plt.xlabel('Daily P&L (RMB)')
    plt.ylabel('Frequency')
    plt.legend()
    plt.grid(True, alpha=0.3)

    # 保存图片
    os.makedirs('output', exist_ok=True)
    figure_path = 'output/historical_var_plot.png'
    plt.savefig(figure_path)
    plt.close()

    # 准备结果
    result = {
        'hist_var_95_1d': var,
        'figure_path': figure_path
    }

    return result

# 计算95%置信水平的VaR
result = calculate_historical_var(confidence_level=0.95)
print(result)
