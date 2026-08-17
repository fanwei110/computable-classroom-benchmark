import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# 1. 读取数据并计入无风险利率
def load_and_preprocess_data(file_path, annual_rf_rate=0.021):
    """读取CSV文件并预处理数据"""
    df = pd.read_csv(file_path, parse_dates=['date'], index_col='date')
    daily_rf_rate = annual_rf_rate / 252  # 假设252个交易日/年
    return df, daily_rf_rate

# 2. 计算滚动年化夏普比率
def calculate_rolling_sharpe(df, window=60, daily_rf_rate=0.0):
    """计算滚动年化夏普比率"""
    excess_returns = df['fund'] - daily_rf_rate
    rolling_mean = excess_returns.rolling(window=window).mean()
    rolling_std = excess_returns.rolling(window=window).std()
    rolling_sharpe = (rolling_mean / rolling_std) * np.sqrt(252)  # 年化
    return rolling_sharpe

# 3. 绘制时间序列图并保存
def plot_and_save_rolling_sharpe(rolling_sharpe, window=60, save_path='rolling_sharpe.png'):
    """绘制滚动夏普比率并保存图形"""
    plt.figure(figsize=(12, 6))
    rolling_sharpe.plot(title=f'{window}-Day Rolling Annualized Sharpe Ratio')
    plt.ylabel('Sharpe Ratio')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()
    return save_path

# 主流程
def main():
    # 路径设置
    data_path = Path('data/market_snapshot_v1.csv')
    output_dir = Path('output')
    output_dir.mkdir(exist_ok=True)
    figure_path = output_dir / 'rolling_sharpe.png'

    # 参数设置
    window = 60  # 可调窗口长度
    annual_rf_rate = 0.021  # 年化无风险利率

    # 1. 读取数据
    df, daily_rf_rate = load_and_preprocess_data(data_path, annual_rf_rate)

    # 2. 计算滚动夏普比率
    rolling_sharpe = calculate_rolling_sharpe(df, window, daily_rf_rate)

    # 3. 报告最后一个窗口的值
    last_sharpe = rolling_sharpe.dropna().iloc[-1]

    # 4. 绘图并保存
    saved_figure_path = plot_and_save_rolling_sharpe(rolling_sharpe, window, figure_path)

    # 准备结果
    result = {
        'rolling_sharpe_last': last_sharpe,
        'figure_path': str(saved_figure_path)
    }

    return result

# 执行并输出结果
if __name__ == '__main__':
    result = main()
    print(result)
