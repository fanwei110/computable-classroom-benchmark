import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# 设置参数
CONFIDENCE_LEVEL = 0.95  # 可调置信水平
POSITION_SIZE = 1_000_000  # 头寸100万元
DATA_PATH = 'data/market_snapshot_v1.csv'
FIGURE_PATH = 'var_histogram.png'

# 1. 读取数据并构造日损益
def calculate_daily_pnl():
    # 读取CSV文件
    df = pd.read_csv(DATA_PATH)

    # 计算日收益率 (fund列)
    df['daily_return'] = df['fund'].pct_change()

    # 计算日损益 (人民币)
    df['daily_pnl'] = df['daily_return'] * POSITION_SIZE

    # 去除NaN值 (第一天无收益率)
    pnl_series = df['daily_pnl'].dropna()

    return pnl_series

# 2. 计算历史VaR
def calculate_historical_var(pnl_series, confidence_level):
    # 计算分位数 (损失为负值，因此取1-confidence_level)
    var = -np.percentile(pnl_series, 100 * (1 - confidence_level))
    return var

# 3. 绘制直方图并标注VaR线
def plot_histogram_with_var(pnl_series, var, confidence_level):
    plt.figure(figsize=(10, 6))

    # 绘制直方图
    plt.hist(pnl_series, bins=50, alpha=0.7, color='skyblue', edgecolor='black')

    # 添加VaR线
    plt.axvline(x=-var, color='red', linestyle='--', linewidth=2,
                label=f'{confidence_level*100:.0f}% 1-day VaR: ¥{var:,.2f}')

    # 设置标题和标签
    plt.title('Daily PnL Distribution with Historical VaR', fontsize=14)
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
    # 1. 计算日损益
    pnl_series = calculate_daily_pnl()

    # 2. 计算VaR
    var_95_1d = calculate_historical_var(pnl_series, CONFIDENCE_LEVEL)

    # 3. 绘制图形
    figure_path = plot_histogram_with_var(pnl_series, var_95_1d, CONFIDENCE_LEVEL)

    # 4. 构建结果字典
    result = {
        'hist_var_95_1d': var_95_1d,
        'figure_path': str(Path(FIGURE_PATH).absolute())
    }

    return result

# 执行并输出结果
if __name__ == '__main__':
    result = main()
    print(result)
