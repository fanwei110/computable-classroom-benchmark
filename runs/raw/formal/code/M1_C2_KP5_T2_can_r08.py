import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# 设置参数
CONFIDENCE_LEVEL = 0.95  # 可调置信水平
POSITION_VALUE = 1_000_000  # 头寸价值（元）
DATA_PATH = "data/market_snapshot_v1.csv"  # 数据路径
FIGURE_PATH = "var_histogram.png"  # 图形保存路径

# 1. 读取数据并构造日损益
def load_and_process_data(file_path):
    """读取CSV文件并计算日收益率"""
    df = pd.read_csv(file_path)
    daily_returns = df['fund'].dropna().pct_change().dropna()
    daily_pnl = daily_returns * POSITION_VALUE  # 转换为损益
    return daily_pnl

# 2. 计算历史VaR
def calculate_historical_var(pnl_series, confidence_level):
    """计算历史VaR"""
    var = np.percentile(pnl_series, 100 * (1 - confidence_level))
    return var

# 3. 绘制直方图并标注VaR
def plot_pnl_histogram(pnl_series, confidence_level, var_value, save_path):
    """绘制损益分布直方图并标注VaR"""
    plt.figure(figsize=(10, 6))
    plt.hist(pnl_series, bins=50, alpha=0.75, color='skyblue', edgecolor='black')

    # 标注VaR线
    plt.axvline(var_value, color='red', linestyle='--', linewidth=2)
    plt.text(var_value - 5000, plt.ylim()[1] * 0.9,
             f'{confidence_level:.0%} VaR: ¥{abs(var_value):,.2f}',
             color='red', ha='right', va='top')

    plt.title(f'Daily P&L Distribution with {confidence_level:.0%} VaR')
    plt.xlabel('Daily P&L (RMB)')
    plt.ylabel('Frequency')
    plt.grid(True, alpha=0.3)

    # 保存图形
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    return save_path

# 主流程
def main():
    # 1. 读取并处理数据
    daily_pnl = load_and_process_data(DATA_PATH)

    # 2. 计算VaR
    var_95 = calculate_historical_var(daily_pnl, CONFIDENCE_LEVEL)

    # 3. 绘制图形
    figure_path = plot_pnl_histogram(
        daily_pnl,
        CONFIDENCE_LEVEL,
        var_95,
        FIGURE_PATH
    )

    # 准备结果
    result = {
        'hist_var_95_1d': round(abs(var_95), 2),  # 95%一日历史VaR（人民币）
        'figure_path': str(Path(figure_path).absolute())  # 图形绝对路径
    }

    return result

# 执行并输出结果
if __name__ == "__main__":
    result = main()
    print(result)
