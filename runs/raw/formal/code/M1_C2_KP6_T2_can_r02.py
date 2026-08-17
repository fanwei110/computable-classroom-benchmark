import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# 1. 读取数据并计入无风险利率
def load_and_preprocess_data(file_path):
    df = pd.read_csv(file_path, parse_dates=['date'])
    df = df.sort_values('date').reset_index(drop=True)

    # 提取fund列的日收益率
    fund_returns = df.set_index('date')['fund'].dropna()

    # 年化无风险利率转换为日利率
    annual_rf_rate = 0.021
    daily_rf_rate = (1 + annual_rf_rate) ** (1/252) - 1

    return fund_returns, daily_rf_rate

# 2. 计算滚动年化夏普比率
def calculate_rolling_sharpe(returns, risk_free_rate, window=60):
    # 计算超额收益
    excess_returns = returns - risk_free_rate

    # 计算滚动均值和标准差
    rolling_mean = excess_returns.rolling(window=window).mean()
    rolling_std = excess_returns.rolling(window=window).std()

    # 年化夏普比率
    annualized_sharpe = (rolling_mean / rolling_std) * np.sqrt(252)

    return annualized_sharpe

# 3. 绘制时间序列图并报告最后一个窗口值
def plot_and_report(rolling_sharpe, window):
    plt.figure(figsize=(12, 6))
    rolling_sharpe.plot(title=f'{window}-Day Rolling Annualized Sharpe Ratio')
    plt.ylabel('Sharpe Ratio')
    plt.xlabel('Date')
    plt.grid(True)

    # 保存图形
    figure_path = Path('rolling_sharpe_ratio.png')
    plt.savefig(figure_path)
    plt.close()

    # 获取最后一个窗口的夏普值
    last_sharpe = rolling_sharpe.iloc[-1]

    return last_sharpe, figure_path

# 主程序
def main():
    # 设置文件路径和窗口长度
    data_path = Path('data/market_snapshot_v1.csv')
    window_length = 60  # 可调窗口长度

    # 1. 加载数据
    fund_returns, daily_rf_rate = load_and_preprocess_data(data_path)

    # 2. 计算滚动夏普比率
    rolling_sharpe = calculate_rolling_sharpe(fund_returns, daily_rf_rate, window_length)

    # 3. 绘图并报告结果
    last_sharpe, figure_path = plot_and_report(rolling_sharpe, window_length)

    # 4. 填充result字典
    result = {
        'rolling_sharpe_last': last_sharpe,
        'figure_path': str(figure_path)
    }

    return result

# 执行主程序
if __name__ == '__main__':
    result = main()
    print(result)
