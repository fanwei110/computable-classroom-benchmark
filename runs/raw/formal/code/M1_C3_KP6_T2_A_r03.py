import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

def calculate_rolling_sharpe(fund_returns, window=60, rf=0.021):
    """
    计算滚动年化夏普比率

    参数:
    - fund_returns: Series, 基金的日收益率
    - window: int, 滚动窗口大小（默认60日）
    - rf: float, 无风险利率（默认2.1%）

    返回:
    - rolling_sharpe: Series, 滚动夏普比率
    """
    # 计算滚动年化收益率和年化波动率
    rolling_mean = fund_returns.rolling(window=window).mean() * 252
    rolling_std = fund_returns.rolling(window=window).std(ddof=1) * np.sqrt(252)

    # 计算滚动夏普比率
    rolling_sharpe = (rolling_mean - rf) / rolling_std

    return rolling_sharpe

def main(fund_data, window=60, rf=0.021, figure_dir='.'):
    """
    主函数：计算滚动夏普比率并绘图

    参数:
    - fund_data: Series, 基金的日收益率
    - window: int, 滚动窗口大小（默认60日）
    - rf: float, 无风险利率（默认2.1%）
    - figure_dir: str, 图片保存目录（默认当前目录）

    返回:
    - result: dict, 包含'rolling_sharpe_last'和'figure_path'
    """
    # 计算滚动夏普比率
    rolling_sharpe = calculate_rolling_sharpe(fund_data, window=window, rf=rf)

    # 获取最后一个窗口的夏普比率
    rolling_sharpe_last = rolling_sharpe.iloc[-1]

    # 绘图
    plt.figure(figsize=(10, 6))
    rolling_sharpe.plot(label=f'{window}日滚动年化夏普比率')
    plt.title(f'{window}日滚动年化夏普比率 (rf={rf*100:.1f}%)')
    plt.xlabel('日期')
    plt.ylabel('夏普比率')
    plt.legend()
    plt.grid(True)

    # 保存图片
    figure_path = os.path.join(figure_dir, f'rolling_sharpe_{window}day.png')
    plt.savefig(figure_path)
    plt.close()

    # 构建结果字典
    result = {
        'rolling_sharpe_last': rolling_sharpe_last,
        'figure_path': figure_path
    }

    return result

# 示例用法（假设fund_data是日收益率Series）
# fund_data = pd.Series(...)  # 替换为实际数据
# result = main(fund_data, window=60, rf=0.021)
# print(result)
