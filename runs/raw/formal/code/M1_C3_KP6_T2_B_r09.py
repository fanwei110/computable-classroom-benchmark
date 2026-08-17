import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

def calculate_rolling_sharpe(fund, rf=0.021, window=60):
    """
    计算滚动夏普比率

    参数:
    fund: Series或DataFrame列，包含基金的日收益率
    rf: 年化无风险利率，默认2.1%
    window: 滚动窗口长度，默认60天

    返回:
    result: 包含最后一个窗口夏普比率和图片路径的字典
    """
    # 日化无风险利率
    daily_rf = rf / 252

    # 计算滚动收益率均值和标准差
    rolling_mean = fund.rolling(window=window).mean()
    rolling_std = fund.rolling(window=window).std(ddof=1)

    # 计算滚动夏普比率（年化）
    rolling_sharpe = (rolling_mean - daily_rf) / rolling_std * np.sqrt(252)

    # 最后一个窗口的夏普比率
    last_sharpe = rolling_sharpe.iloc[-1]

    # 绘制图形
    plt.figure(figsize=(10, 6))
    rolling_sharpe.plot(title=f'{window}-day Rolling Sharpe Ratio')
    plt.ylabel('Sharpe Ratio')
    plt.grid(True)

    # 保存图片
    figure_path = 'rolling_sharpe.png'
    plt.savefig(figure_path)
    plt.close()

    # 返回结果
    result = {
        'rolling_sharpe_last': last_sharpe,
        'figure_path': os.path.abspath(figure_path)
    }

    return result

# 示例用法（假设fund是一个包含日收益率的Series）
# fund = pd.Series(...)  # 你的基金日收益率数据
# result = calculate_rolling_sharpe(fund, rf=0.021, window=60)
# print(result)
