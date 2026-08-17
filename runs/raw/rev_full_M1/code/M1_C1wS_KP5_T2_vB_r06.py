import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# 1. 读取数据并构造日损益
def calculate_historical_var():
    # 读取CSV文件
    data_path = Path('data/market_snapshot_v1.csv')
    df = pd.read_csv(data_path)

    # 计算日收益率
    daily_returns = df['fund'].pct_change().dropna()

    # 计算头寸的日损益（头寸100万）
    position = 1_000_000
    daily_pnl = daily_returns * position

    # 2. 计算95%历史VaR
    confidence_level = 0.95
    var_95 = np.percentile(daily_pnl, 100 * (1 - confidence_level))

    # 3. 绘制直方图并添加VaR线
    plt.figure(figsize=(10, 6))
    n, bins, patches = plt.hist(daily_pnl, bins=50, alpha=0.75, color='skyblue', edgecolor='black')

    # 添加VaR线
    plt.axvline(var_95, color='red', linestyle='dashed', linewidth=2,
                label=f'95% 1-day VaR: {var_95:,.2f} CNY')

    plt.title('Daily P&L Distribution with Historical VaR')
    plt.xlabel('Daily P&L (CNY)')
    plt.ylabel('Frequency')
    plt.legend()
    plt.grid(True, alpha=0.3)

    # 保存图形
    figure_path = Path('var_histogram.png')
    plt.savefig(figure_path)
    plt.close()

    # 4. 填充result字典
    result = {
        'hist_var_95_1d': float(var_95),
        'figure_path': str(figure_path.absolute())
    }

    return result

# 执行计算并输出结果
result = calculate_historical_var()
print(result)
