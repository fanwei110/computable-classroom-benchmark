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

    # 提取fund列的日收益率
    daily_returns = df['fund'].dropna().values

    # 计算1,000,000元头寸的日损益
    position = 1_000_000
    daily_pnl = position * daily_returns

    # 2. 计算95%历史VaR
    confidence_level = 0.95
    var_95 = np.percentile(daily_pnl, 100 * (1 - confidence_level))

    # 3. 绘制直方图并标注VaR
    plt.figure(figsize=(10, 6))
    plt.hist(daily_pnl, bins=50, alpha=0.75, color='skyblue', edgecolor='black')

    # 添加VaR标注线
    plt.axvline(var_95, color='red', linestyle='--', linewidth=2)
    plt.text(var_95 * 1.05, plt.ylim()[1] * 0.9,
             f'95% VaR: ¥{abs(var_95):,.2f}',
             color='red', fontsize=12, bbox=dict(facecolor='white', alpha=0.8))

    plt.title('1,000,000元头寸日损益分布', fontsize=14)
    plt.xlabel('日损益 (人民币)', fontsize=12)
    plt.ylabel('频数', fontsize=12)
    plt.grid(True, alpha=0.3)

    # 保存图形
    figure_path = Path('var_histogram.png')
    plt.savefig(figure_path, dpi=300, bbox_inches='tight')
    plt.close()

    # 4. 构建结果字典
    result = {
        'hist_var_95_1d': round(abs(var_95), 2),
        'figure_path': str(figure_path.absolute())
    }

    return result

# 执行计算并输出结果
result = calculate_historical_var()
print(result)
