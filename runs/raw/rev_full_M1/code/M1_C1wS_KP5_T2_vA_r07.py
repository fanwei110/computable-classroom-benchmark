import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# 1. 读取数据并构造日损益
def calculate_historical_var(confidence_level=0.95):
    # 读取CSV文件
    data_path = Path('data/market_snapshot_v1.csv')
    df = pd.read_csv(data_path)

    # 计算日收益率（简单收益率）
    fund_prices = df['fund']
    daily_returns = fund_prices.pct_change().dropna()

    # 计算头寸的日损益（人民币）
    position_size = 1_000_000  # 100万元
    daily_pnl = daily_returns * position_size

    # 2. 计算历史VaR
    # 使用经验分布的分位数
    var_percentile = 1 - confidence_level
    historical_var = np.percentile(daily_pnl, var_percentile * 100)

    # 3. 绘制直方图并添加VaR线
    plt.figure(figsize=(10, 6))
    plt.hist(daily_pnl, bins=50, alpha=0.75, color='skyblue', edgecolor='black')

    # 添加VaR线
    plt.axvline(x=historical_var, color='red', linestyle='--',
                label=f'{confidence_level*100:.0f}% 1-day VaR: ¥{historical_var:,.2f}')
    plt.title('Daily P&L Distribution with Historical VaR')
    plt.xlabel('Daily P&L (RMB)')
    plt.ylabel('Frequency')
    plt.legend()
    plt.grid(True, alpha=0.3)

    # 保存图形
    figure_path = 'var_histogram.png'
    plt.savefig(figure_path)
    plt.close()

    # 4. 返回结果
    result = {
        'hist_var_95_1d': historical_var,
        'figure_path': figure_path
    }
    return result

# 执行计算并输出结果
result = calculate_historical_var(confidence_level=0.95)
print(result)
