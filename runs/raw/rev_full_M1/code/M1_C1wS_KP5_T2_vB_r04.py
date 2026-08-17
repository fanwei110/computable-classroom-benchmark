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

    # 构造头寸的日损益（头寸100万）
    position = 1_000_000
    daily_pnl = daily_returns * position

    # 2. 计算95%历史VaR
    confidence_level = 0.95
    var_95_1d = -np.percentile(daily_pnl, 100 * (1 - confidence_level))

    # 3. 绘制直方图并添加VaR线
    plt.figure(figsize=(10, 6))
    n, bins, patches = plt.hist(daily_pnl, bins=50, alpha=0.75, color='skyblue', edgecolor='black')

    # 添加VaR标注线
    plt.axvline(x=-var_95_1d, color='red', linestyle='--', linewidth=2)
    plt.text(-var_95_1d * 1.05, max(n) * 0.9,
             f'95% 1-day VaR: ¥{var_95_1d:,.2f}',
             color='red', fontsize=12, bbox=dict(facecolor='white', alpha=0.8))

    # 图形美化
    plt.title('Daily P&L Distribution with Historical VaR', fontsize=14)
    plt.xlabel('Daily P&L (RMB)', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.grid(axis='y', alpha=0.3)

    # 保存图形
    figure_path = Path('var_histogram.png')
    plt.savefig(figure_path, dpi=300, bbox_inches='tight')
    plt.close()

    # 4. 填充result字典
    result = {
        'hist_var_95_1d': round(var_95_1d, 2),
        'figure_path': str(figure_path.absolute())
    }

    return result

# 执行计算并输出结果
result = calculate_historical_var()
print(result)
