import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# 设置参数
INITIAL_POSITION = 1_000_000  # 初始头寸（人民币）
CONFIDENCE_LEVEL = 0.95       # 默认置信水平
DATA_PATH = "data/market_snapshot_v1.csv"  # 数据路径
FIGURE_PATH = "var_histogram.png"  # 图形保存路径

# 1. 读取数据并构造日损益
def load_and_preprocess_data(file_path):
    """读取CSV文件并计算日收益率和日损益"""
    df = pd.read_csv(file_path)
    daily_returns = df['fund'].dropna().pct_change().dropna()
    daily_pnl = daily_returns * INITIAL_POSITION
    return daily_pnl

# 2. 计算历史VaR
def calculate_historical_var(pnl_series, confidence_level):
    """计算历史VaR"""
    var = np.percentile(pnl_series, 100 * (1 - confidence_level))
    return var

# 3. 绘制直方图并标注VaR
def plot_pnl_histogram_with_var(pnl_series, confidence_level, figure_path):
    """绘制日损益直方图并标注VaR"""
    plt.figure(figsize=(10, 6))
    plt.hist(pnl_series, bins=50, alpha=0.75, color='skyblue', edgecolor='black')

    var = calculate_historical_var(pnl_series, confidence_level)
    plt.axvline(var, color='red', linestyle='--', linewidth=2,
                label=f'{confidence_level:.0%} VaR: ¥{var:,.2f}')

    plt.title(f'Daily P&L Distribution with {confidence_level:.0%} Historical VaR')
    plt.xlabel('Daily P&L (RMB)')
    plt.ylabel('Frequency')
    plt.legend()
    plt.grid(True, alpha=0.3)

    plt.savefig(figure_path, dpi=300, bbox_inches='tight')
    plt.close()
    return figure_path

# 主流程
def main():
    # 1. 读取数据
    daily_pnl = load_and_preprocess_data(DATA_PATH)

    # 2. 计算VaR
    var_95_1d = calculate_historical_var(daily_pnl, CONFIDENCE_LEVEL)

    # 3. 绘制图形
    figure_path = plot_pnl_histogram_with_var(daily_pnl, CONFIDENCE_LEVEL, FIGURE_PATH)

    # 4. 准备结果
    result = {
        'hist_var_95_1d': round(var_95_1d, 2),  # 保留2位小数
        'figure_path': str(Path(figure_path).absolute())
    }

    return result

# 执行并输出结果
if __name__ == "__main__":
    result = main()
    print(result)
