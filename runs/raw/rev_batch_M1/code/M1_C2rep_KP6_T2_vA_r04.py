import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# 设置参数
WINDOW_DAYS = 60  # 滚动窗口长度（可调）
ANNUAL_RISK_FREE_RATE = 0.021  # 年化无风险利率
DAILY_RISK_FREE_RATE = ANNUAL_RISK_FREE_RATE / 252  # 转换为日无风险利率
FIGURE_PATH = "rolling_sharpe.png"  # 图形保存路径

# 1. 读取数据
def load_data(file_path):
    df = pd.read_csv(file_path, parse_dates=['date'], index_col='date')
    return df

# 2. 计算滚动年化夏普比率
def calculate_rolling_sharpe(df, window_days=WINDOW_DAYS):
    # 提取基金收益率
    fund_returns = df['fund'].dropna()

    # 计算超额收益（减去日无风险利率）
    excess_returns = fund_returns - DAILY_RISK_FREE_RATE

    # 计算滚动年化夏普比率
    rolling_mean = excess_returns.rolling(window=window_days).mean()
    rolling_std = excess_returns.rolling(window=window_days).std()

    # 年化处理
    annualized_sharpe = (rolling_mean / rolling_std) * np.sqrt(252)

    return annualized_sharpe

# 3. 绘制图形并报告结果
def plot_and_report(sharpe_series, window_days=WINDOW_DAYS):
    # 创建图形
    plt.figure(figsize=(12, 6))
    sharpe_series.plot(title=f'{window_days}-Day Rolling Annualized Sharpe Ratio')
    plt.ylabel('Sharpe Ratio')
    plt.grid(True)

    # 保存图形
    plt.savefig(FIGURE_PATH)
    plt.close()

    # 获取最后一个窗口的夏普值
    last_sharpe = sharpe_series.dropna().iloc[-1]

    return last_sharpe

# 主流程
def main():
    # 读取数据
    data_path = Path('data/market_snapshot_v1.csv')
    df = load_data(data_path)

    # 计算滚动夏普比率
    rolling_sharpe = calculate_rolling_sharpe(df, WINDOW_DAYS)

    # 绘制图形并获取结果
    last_sharpe = plot_and_report(rolling_sharpe, WINDOW_DAYS)

    # 准备结果字典
    result = {
        'rolling_sharpe_last': last_sharpe,
        'figure_path': str(Path(FIGURE_PATH).absolute())
    }

    return result

# 执行主流程
if __name__ == "__main__":
    result = main()
    print(result)
