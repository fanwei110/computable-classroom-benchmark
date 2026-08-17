import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

def calculate_rolling_sharpe():
    # 设置随机种子以确保可复现性
    np.random.seed(42)

    # 生成模拟课程数据（因为题目没有提供实际数据文件）
    # 假设有1000个交易日的收益率数据
    n_days = 1000
    dates = pd.date_range(end=pd.Timestamp.today(), periods=n_days, freq='D')
    fund_returns = pd.Series(
        np.random.normal(loc=0.0005, scale=0.01, size=n_days),
        index=dates,
        name='fund'
    )

    # 无风险利率（年化）
    annual_risk_free_rate = 0.021
    daily_risk_free_rate = annual_risk_free_rate / 252  # 假设252个交易日

    # 窗口长度（可调参数）
    window_length = 60

    # 计算超额收益率
    excess_returns = fund_returns - daily_risk_free_rate

    # 计算滚动年化夏普比率
    rolling_mean = excess_returns.rolling(window=window_length).mean()
    rolling_std = excess_returns.rolling(window=window_length).std()
    rolling_sharpe = (rolling_mean / rolling_std) * np.sqrt(252)

    # 获取最后一个窗口的夏普值
    last_sharpe = rolling_sharpe.iloc[-1]

    # 绘制时间序列图
    plt.figure(figsize=(12, 6))
    rolling_sharpe.plot(title=f'{window_length}-Day Rolling Annualized Sharpe Ratio')
    plt.ylabel('Sharpe Ratio')
    plt.grid(True)

    # 保存图片
    figure_path = Path('rolling_sharpe_ratio.png')
    plt.savefig(figure_path)
    plt.close()

    # 准备结果字典
    result = {
        'rolling_sharpe_last': last_sharpe,
        'figure_path': str(figure_path.absolute())
    }

    return result

# 执行计算并获取结果
result = calculate_rolling_sharpe()

# 输出结果以验证
print("Result dictionary:")
print(result)
