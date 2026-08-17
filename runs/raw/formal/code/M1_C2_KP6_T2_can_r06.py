import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# 设定参数
WINDOW_DAYS = 60  # 滚动窗口长度（可调）
ANNUAL_RISK_FREE_RATE = 0.021  # 年化无风险利率
DAILY_RISK_FREE_RATE = ANNUAL_RISK_FREE_RATE / 252  # 日化无风险利率
DATA_PATH = "data/market_snapshot_v1.csv"  # 数据路径
FIGURE_PATH = "rolling_sharpe.png"  # 图形保存路径

# 1. 读取数据并计算超额收益
def load_and_preprocess_data(file_path):
    df = pd.read_csv(file_path, parse_dates=['date'])
    df = df.sort_values('date').reset_index(drop=True)

    # 计算日超额收益（减去无风险利率）
    df['excess_return'] = df['fund'] - DAILY_RISK_FREE_RATE

    return df

# 2. 计算滚动年化夏普比率
def calculate_rolling_sharpe(df, window_days):
    # 计算滚动窗口内的均值和标准差
    rolling_mean = df['excess_return'].rolling(window=window_days).mean()
    rolling_std = df['excess_return'].rolling(window=window_days).std()

    # 年化夏普比率（日收益年化因子为sqrt(252)）
    rolling_sharpe = (rolling_mean / rolling_std) * np.sqrt(252)

    return rolling_sharpe

# 3. 绘制时间序列图
def plot_rolling_sharpe(rolling_sharpe, window_days):
    plt.figure(figsize=(12, 6))
    plt.plot(rolling_sharpe.index, rolling_sharpe.values, label=f'{window_days}-day Rolling Sharpe Ratio')
    plt.axhline(0, color='gray', linestyle='--', linewidth=0.5)
    plt.title(f'Annualized Rolling Sharpe Ratio ({window_days}-day window)')
    plt.xlabel('Date')
    plt.ylabel('Sharpe Ratio')
    plt.legend()
    plt.grid(True, alpha=0.3)

    # 保存图形
    plt.savefig(FIGURE_PATH)
    plt.close()

    return FIGURE_PATH

# 主流程
def main():
    # 1. 读取数据
    df = load_and_preprocess_data(DATA_PATH)

    # 2. 计算滚动夏普比率
    rolling_sharpe = calculate_rolling_sharpe(df, WINDOW_DAYS)

    # 3. 绘制图形并保存
    figure_path = plot_rolling_sharpe(rolling_sharpe, WINDOW_DAYS)

    # 4. 获取最后一个窗口的夏普值
    last_sharpe = rolling_sharpe.dropna().iloc[-1]

    # 存储结果
    result = {
        'rolling_sharpe_last': last_sharpe,
        'figure_path': str(Path(FIGURE_PATH).absolute())
    }

    return result

# 执行并输出结果
if __name__ == "__main__":
    result = main()
    print(result)
