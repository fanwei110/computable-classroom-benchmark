import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# 设置参数
POSITION_SIZE = 1_000_000  # 头寸规模（元）
CONFIDENCE_LEVEL = 0.95    # 默认置信水平
DATA_PATH = 'data/market_snapshot_v1.csv'
FIGURE_PATH = 'var_histogram.png'

def calculate_historical_var():
    # 1. 读取数据并构造日损益
    df = pd.read_csv(DATA_PATH)
    daily_returns = df['fund'].dropna().values  # 假设'fund'列为日收益率序列

    # 将收益率转换为绝对损益（元）
    daily_pnl = daily_returns * POSITION_SIZE

    # 2. 计算历史VaR
    var_percentile = (1 - CONFIDENCE_LEVEL) * 100
    historical_var = np.percentile(daily_pnl, var_percentile)

    # 3. 绘制直方图并标注VaR
    plt.figure(figsize=(10, 6))
    plt.hist(daily_pnl, bins=50, alpha=0.75, color='skyblue', edgecolor='black')

    # 添加VaR线
    plt.axvline(x=historical_var, color='red', linestyle='--', linewidth=2)
    plt.text(historical_var * 1.05, plt.ylim()[1] * 0.9,
             f'95% 1-day VaR: ¥{abs(historical_var):,.2f}',
             color='red', fontsize=12, bbox=dict(facecolor='white', alpha=0.8))

    plt.title(f'Daily P&L Distribution with {CONFIDENCE_LEVEL:.0%} VaR')
    plt.xlabel('Daily P&L (RMB)')
    plt.ylabel('Frequency')
    plt.grid(True, alpha=0.3)

    # 保存图形
    plt.savefig(FIGURE_PATH)
    plt.close()

    # 4. 构建结果字典
    result = {
        'hist_var_95_1d': abs(historical_var),  # 返回正值（损失金额）
        'figure_path': str(Path(FIGURE_PATH).absolute())
    }

    return result

# 执行计算并输出结果
result = calculate_historical_var()
print(result)
