import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

def calculate_rolling_sharpe():
    # 设置随机种子以确保可复现性
    np.random.seed(42)

    # 生成模拟课程数据（因为没有实际数据，我们模拟一个）
    n_days = 200
    dates = pd.date_range(end=pd.Timestamp.today(), periods=n_days, freq='D')
    daily_returns = np.random.normal(loc=0.0005, scale=0.01, size=n_days)  # 模拟日收益率
    fund = pd.Series(daily_returns, index=dates, name='fund')

    # 无风险利率（年化）
    annual_risk_free_rate = 0.021
    daily_risk_free_rate = annual_risk_free_rate / 252  # 假设252个交易日

    # 可调窗口长度
    window_length = 60

    # 计算超额收益
    excess_returns = fund - daily_risk_free_rate

    # 计算滚动年化夏普比率
    rolling_mean = excess_returns.rolling(window=window_length).mean()
    rolling_std = excess_returns.rolling(window=window_length).std()
    rolling_sharpe = (rolling_mean / rolling_std) * np.sqrt(252)  # 年化

    # 获取最后一个窗口的夏普值
    last_sharpe = rolling_sharpe.iloc[-1]

    # 绘制图形
    plt.figure(figsize=(10, 6))
    rolling_sharpe.plot(title=f'{window_length}-Day Rolling Annualized Sharpe Ratio')
    plt.ylabel('Sharpe Ratio')
    plt.grid(True)

    # 保存图形
    figure_path = Path('rolling_sharpe_ratio.png')
    plt.savefig(figure_path)
    plt.close()

    # 准备结果
    result = {
        'rolling_sharpe_last': last_sharpe,
        'figure_path': str(figure_path.absolute())
    }

    return result

# 执行计算并输出结果
result = calculate_rolling_sharpe()
print(result)
