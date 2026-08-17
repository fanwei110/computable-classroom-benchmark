import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# 1. 读取数据并计入无风险利率
def load_and_preprocess_data(file_path, annual_rf_rate=0.021):
    """读取CSV文件并预处理数据"""
    df = pd.read_csv(file_path, parse_dates=['date'], index_col='date')
    daily_rf_rate = annual_rf_rate / 252  # 假设252个交易日
    return df, daily_rf_rate

# 2. 计算滚动年化夏普比率
def calculate_rolling_sharpe(df, window=60, annual_rf_rate=0.021):
    """计算滚动年化夏普比率"""
    daily_rf_rate = annual_rf_rate / 252
    excess_returns = df['fund'] - daily_rf_rate

    # 计算滚动均值和标准差
    rolling_mean = excess_returns.rolling(window=window).mean()
    rolling_std = excess_returns.rolling(window=window).std()

    # 年化夏普比率
    annualized_sharpe = (rolling_mean / rolling_std) * np.sqrt(252)
    return annualized_sharpe

# 3. 绘制时间序列图并报告最后一个窗口值
def plot_and_report(rolling_sharpe, window=60):
    """绘制滚动夏普比率并报告最后一个值"""
    plt.figure(figsize=(12, 6))
    rolling_sharpe.plot(title=f'{window}-Day Rolling Annualized Sharpe Ratio')
    plt.ylabel('Sharpe Ratio')
    plt.grid(True)

    # 保存图形
    figure_path = Path('rolling_sharpe_ratio.png')
    plt.savefig(figure_path)
    plt.close()

    # 获取最后一个窗口的值
    last_sharpe = rolling_sharpe.iloc[-1]
    return last_sharpe, figure_path

# 主流程
def main():
    # 文件路径
    file_path = 'data/market_snapshot_v1.csv'

    # 1. 读取数据
    df, daily_rf_rate = load_and_preprocess_data(file_path)

    # 2. 计算滚动夏普比率（默认60日窗口）
    window = 60
    rolling_sharpe = calculate_rolling_sharpe(df, window=window)

    # 3. 绘制图形并报告结果
    last_sharpe, figure_path = plot_and_report(rolling_sharpe, window=window)

    # 4. 保存结果
    result = {
        'rolling_sharpe_last': last_sharpe,
        'figure_path': str(figure_path)
    }
    return result

# 执行主流程
if __name__ == '__main__':
    result = main()
    print(result)
