import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# 设置中文字体以避免显示问题
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

def calculate_historical_var():
    # 1. 读取数据并构造日损益
    data_path = Path('data/market_snapshot_v1.csv')
    df = pd.read_csv(data_path)
    daily_returns = df['fund'].dropna().values  # 获取fund列的日收益率序列

    position = 1_000_000  # 头寸规模（元）
    daily_pnl = position * daily_returns  # 计算日损益（人民币）

    # 2. 计算95%历史VaR
    confidence_level = 0.95
    var_95 = np.percentile(daily_pnl, 100 * (1 - confidence_level))

    # 3. 绘制直方图并标注VaR
    plt.figure(figsize=(10, 6))
    plt.hist(daily_pnl, bins=50, alpha=0.75, color='skyblue', edgecolor='black')

    # 添加VaR竖线
    plt.axvline(var_95, color='red', linestyle='--', linewidth=2)
    plt.text(var_95 * 1.05, plt.ylim()[1] * 0.9,
             f'95% VaR: {var_95:,.2f}元',
             color='red', ha='left', va='top')

    plt.title('日损益分布与95%历史VaR')
    plt.xlabel('日损益（人民币）')
    plt.ylabel('频数')
    plt.grid(True, alpha=0.3)

    # 保存图形
    figure_path = Path('var_histogram.png')
    plt.savefig(figure_path)
    plt.close()

    # 4. 构建结果字典
    result = {
        'hist_var_95_1d': float(var_95),
        'figure_path': str(figure_path.absolute())
    }

    return result

# 执行计算并输出结果
result = calculate_historical_var()
print(result)
