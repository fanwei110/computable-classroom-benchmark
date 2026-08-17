import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# 设置参数
WINDOW_DAYS = 60  # 滚动窗口长度（可调）
ANNUAL_RISK_FREE_RATE = 0.021  # 年化无风险利率
DAILY_RISK_FREE_RATE = ANNUAL_RISK_FREE_RATE / 252  # 日化无风险利率（假设252交易日/年）

# 1. 读取数据
def load_data(file_path):
    df = pd.read_csv(file_path, parse_dates=['date'])
    df = df[['date', 'fund']].dropna().set_index('date')
    return df

# 2. 计算滚动年化夏普比率
def calculate_rolling_sharpe(df, window_days):
    # 计算日超额收益
    excess_returns = df['fund'] - DAILY_RISK_FREE_RATE

    # 计算滚动年化夏普比率
    rolling_mean = excess_returns.rolling(window=window_days).mean()
    rolling_std = excess_returns.rolling(window=window_days).std()
    rolling_sharpe = (rolling_mean / rolling_std) * np.sqrt(252)  # 年化

    return rolling_sharpe

# 3. 绘制时间序列图并保存
def plot_and_save(rolling_sharpe, window_days):
    plt.figure(figsize=(12, 6))
    rolling_sharpe.plot(title=f'{window_days}-Day Rolling Annualized Sharpe Ratio')
    plt.ylabel('Sharpe Ratio')
    plt.grid(True)

    # 保存图形
    figure_path = Path('rolling_sharpe_ratio.png')
    plt.savefig(figure_path)
    plt.close()

    return figure_path

# 主流程
def main():
    # 加载数据
    data_path = Path('data/market_snapshot_v1.csv')
    df = load_data(data_path)

    # 计算滚动夏普比率
    rolling_sharpe = calculate_rolling_sharpe(df, WINDOW_DAYS)

    # 获取最后一个窗口的值
    last_sharpe = rolling_sharpe.iloc[-1]

    # 绘图并保存
    figure_path = plot_and_save(rolling_sharpe, WINDOW_DAYS)

    # 准备结果
    result = {
        'rolling_sharpe_last': last_sharpe,
        'figure_path': str(figure_path)
    }

    return result

# 执行并输出结果
if __name__ == '__main__':
    result = main()
    print(result)
