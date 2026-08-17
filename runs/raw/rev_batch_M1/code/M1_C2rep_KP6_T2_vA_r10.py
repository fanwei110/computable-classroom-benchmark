import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# 1. 读取数据并计入无风险利率
def load_and_preprocess_data(file_path, annual_rf_rate=0.021):
    df = pd.read_csv(file_path, parse_dates=['date'], index_col='date')
    daily_rf_rate = annual_rf_rate / 252  # 假设年交易日为252天
    df['fund_excess_return'] = df['fund'] - daily_rf_rate
    return df

# 2. 计算滚动年化夏普比率
def calculate_rolling_sharpe(df, window=60):
    rolling_mean = df['fund_excess_return'].rolling(window=window).mean()
    rolling_std = df['fund_excess_return'].rolling(window=window).std()
    rolling_sharpe = rolling_mean / rolling_std * np.sqrt(252)  # 年化
    return rolling_sharpe

# 3. 绘制时间序列并报告最后一个窗口值
def plot_and_report(rolling_sharpe, window=60):
    plt.figure(figsize=(12, 6))
    rolling_sharpe.plot(title=f'{window}-Day Rolling Annualized Sharpe Ratio')
    plt.ylabel('Sharpe Ratio')
    plt.grid(True)

    # 保存图形
    figure_path = Path('rolling_sharpe.png')
    plt.savefig(figure_path)
    plt.close()

    # 获取最后一个窗口的值
    last_sharpe = rolling_sharpe.iloc[-1]

    return last_sharpe, figure_path

# 主流程
def main():
    # 设置参数
    window_size = 60
    data_path = 'data/market_snapshot_v1.csv'

    # 1. 读取数据
    df = load_and_preprocess_data(data_path)

    # 2. 计算滚动夏普比率
    rolling_sharpe = calculate_rolling_sharpe(df, window=window_size)

    # 3. 绘图并报告
    last_sharpe, figure_path = plot_and_report(rolling_sharpe, window=window_size)

    # 4. 填充result
    result = {
        'rolling_sharpe_last': last_sharpe,
        'figure_path': str(figure_path)
    }

    return result

# 执行
if __name__ == '__main__':
    result = main()
    print(result)
