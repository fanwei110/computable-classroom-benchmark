import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

def calculate_rolling_sharpe(fund_returns, window=60, rf=0.021):
    """
    计算滚动年化夏普比率

    参数:
    - fund_returns: Series, 基金的日收益率数据
    - window: int, 滚动窗口大小（默认60日）
    - rf: float, 无风险利率（默认2.1%）

    返回:
    - rolling_sharpe: Series, 滚动夏普比率
    - last_sharpe: float, 最后一个窗口的夏普比率
    - figure_path: str, 保存的图片路径
    """
    # 计算滚动年化收益率和年化波动率
    rolling_mean = fund_returns.rolling(window=window).mean() * 252
    rolling_std = fund_returns.rolling(window=window).std(ddof=1) * np.sqrt(252)

    # 计算滚动夏普比率
    rolling_sharpe = (rolling_mean - rf) / rolling_std

    # 最后一个窗口的夏普比率
    last_sharpe = rolling_sharpe.iloc[-1]

    # 绘制曲线
    plt.figure(figsize=(10, 6))
    rolling_sharpe.plot(label=f'{window}日滚动年化夏普比率')
    plt.title(f'{window}日滚动年化夏普比率 (rf={rf*100:.1f}%)')
    plt.xlabel('日期')
    plt.ylabel('夏普比率')
    plt.legend()
    plt.grid(True)

    # 保存图片
    figure_path = 'rolling_sharpe.png'
    plt.savefig(figure_path)
    plt.close()

    return rolling_sharpe, last_sharpe, figure_path

# 示例数据（假设fund是日收益率数据）
# 如果fund是净值数据，需要先转换为日收益率：fund_returns = fund.pct_change().dropna()
np.random.seed(42)
dates = pd.date_range(start='2020-01-01', periods=500)
fund = pd.Series(np.random.normal(0.0005, 0.01, size=500), index=dates, name='fund_returns')

# 计算滚动夏普比率
window = 60
rf = 0.021
rolling_sharpe, last_sharpe, figure_path = calculate_rolling_sharpe(fund, window=window, rf=rf)

# 输出结果
result = {
    'rolling_sharpe_last': last_sharpe,
    'figure_path': os.path.abspath(figure_path)
}

print(result)
