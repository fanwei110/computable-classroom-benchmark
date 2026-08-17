import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

def calculate_rolling_sharpe(fund_returns, rf=0.021, window=60):
    """
    计算滚动夏普比率

    参数:
    fund_returns: 基金收益率序列（日收益率）
    rf: 无风险收益率（年化）
    window: 滚动窗口长度（天数）

    返回:
    滚动夏普比率序列
    """
    # 将年化无风险收益率转换为日收益率
    daily_rf = (1 + rf) ** (1/252) - 1

    # 计算超额收益
    excess_returns = fund_returns - daily_rf

    # 计算滚动夏普比率
    rolling_mean = excess_returns.rolling(window=window).mean()
    rolling_std = excess_returns.rolling(window=window).std(ddof=1)
    rolling_sharpe = (rolling_mean / rolling_std) * np.sqrt(252)

    return rolling_sharpe

# 生成示例数据（如果没有实际数据）
np.random.seed(42)
n_days = 500
fund_returns = np.random.normal(loc=0.0005, scale=0.01, size=n_days)

# 计算滚动夏普比率
rolling_sharpe = calculate_rolling_sharpe(fund_returns, rf=0.021, window=60)

# 准备结果
result = {
    'rolling_sharpe_last': rolling_sharpe.iloc[-1] if len(rolling_sharpe) > 0 else np.nan,
    'figure_path': None
}

# 绘制图表
plt.figure(figsize=(12, 6))
plt.plot(rolling_sharpe, label='60-day Rolling Sharpe Ratio')
plt.axhline(y=0, color='r', linestyle='--')
plt.title('60-Day Rolling Sharpe Ratio')
plt.xlabel('Date')
plt.ylabel('Sharpe Ratio')
plt.legend()
plt.grid(True)

# 保存图表
figure_path = 'rolling_sharpe.png'
plt.savefig(figure_path)
plt.close()

result['figure_path'] = os.path.abspath(figure_path)

# 输出结果
print(result)
