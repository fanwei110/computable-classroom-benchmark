import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# 设定参数
WINDOW_DAYS = 60  # 滚动窗口长度（可调）
ANNUAL_RISK_FREE_RATE = 0.021  # 年化无风险利率
DAILY_RISK_FREE_RATE = ANNUAL_RISK_FREE_RATE / 252  # 转换为日无风险利率
FIGURE_SAVE_PATH = "rolling_sharpe.png"  # 图形保存路径

# 1. 读取数据
def load_data(file_path):
    df = pd.read_csv(file_path, parse_dates=['date'])
    df = df[['date', 'fund']].dropna().set_index('date')
    return df

# 2. 计算滚动年化夏普比率
def calculate_rolling_sharpe(returns, window_days, daily_rf_rate):
    # 计算超额收益
    excess_returns = returns - daily_rf_rate

    # 滚动计算均值和标准差
    rolling_mean = excess_returns.rolling(window=window_days).mean()
    rolling_std = excess_returns.rolling(window=window_days).std()

    # 年化夏普比率
    annualized_sharpe = (rolling_mean / rolling_std) * np.sqrt(252)

    return annualized_sharpe

# 3. 绘制图形并报告结果
def plot_and_report(rolling_sharpe, window_days):
    plt.figure(figsize=(12, 6))
    rolling_sharpe.plot(title=f'{window_days}-Day Rolling Annualized Sharpe Ratio')
    plt.ylabel('Sharpe Ratio')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(FIGURE_SAVE_PATH)
    plt.close()

    # 获取最后一个窗口的值
    last_sharpe = rolling_sharpe.iloc[-1]

    return last_sharpe

# 主流程
def main():
    # 加载数据
    data_path = Path("data/market_snapshot_v1.csv")
    returns_df = load_data(data_path)

    # 计算滚动夏普比率
    rolling_sharpe = calculate_rolling_sharpe(
        returns=returns_df['fund'],
        window_days=WINDOW_DAYS,
        daily_rf_rate=DAILY_RISK_FREE_RATE
    )

    # 绘图并报告结果
    last_sharpe = plot_and_report(rolling_sharpe, WINDOW_DAYS)

    # 构建结果字典
    result = {
        'rolling_sharpe_last': last_sharpe,
        'figure_path': str(Path(FIGURE_SAVE_PATH).absolute())
    }

    return result

# 执行并输出结果
if __name__ == "__main__":
    result = main()
    print(result)
