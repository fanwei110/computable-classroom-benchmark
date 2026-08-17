import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# 设置参数
CONFIDENCE_LEVEL = 0.95  # 可调置信水平
POSITION = 1_000_000  # 头寸100万元
DATA_PATH = 'data/market_snapshot_v1.csv'
FIGURE_PATH = 'var_histogram.png'

# 1. 读取数据并计算日损益
def calculate_pnl():
    # 读取CSV文件
    df = pd.read_csv(DATA_PATH)

    # 计算日收益率 (fund列)
    df['daily_return'] = df['fund'].pct_change()

    # 计算日损益 (头寸 × 收益率)
    df['daily_pnl'] = POSITION * df['daily_return']

    # 去除NaN值 (第一个数据点)
    pnl = df['daily_pnl'].dropna().values
    return pnl

# 2. 计算历史VaR
def calculate_historical_var(pnl, confidence_level):
    # 计算分位数 (损失为负值，因此取1-confidence_level)
    var = np.percentile(pnl, 100 * (1 - confidence_level))
    return var

# 3. 绘制直方图并标注VaR线
def plot_histogram_with_var(pnl, var, confidence_level):
    plt.figure(figsize=(10, 6))

    # 绘制直方图
    n, bins, patches = plt.hist(pnl, bins=50, alpha=0.75, color='skyblue', edgecolor='black')

    # 标注VaR线
    plt.axvline(x=var, color='red', linestyle='--', linewidth=2, label=f'{confidence_level:.0%} VaR: {var:,.2f}')

    # 设置标签和标题
    plt.title(f'Daily PnL Distribution with {confidence_level:.0%} Historical VaR', fontsize=14)
    plt.xlabel('Daily PnL (RMB)', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.legend(fontsize=12)
    plt.grid(True, alpha=0.3)

    # 保存图形
    plt.savefig(FIGURE_PATH, dpi=300, bbox_inches='tight')
    plt.close()

    return FIGURE_PATH

# 主流程
def main():
    # 计算日损益
    pnl = calculate_pnl()

    # 计算VaR
    var_95 = calculate_historical_var(pnl, CONFIDENCE_LEVEL)

    # 绘制图形
    figure_path = plot_histogram_with_var(pnl, var_95, CONFIDENCE_LEVEL)

    # 构建结果字典
    result = {
        'hist_var_95_1d': float(var_95),
        'figure_path': figure_path
    }

    return result

# 执行并输出结果
if __name__ == '__main__':
    result = main()
    print(result)
