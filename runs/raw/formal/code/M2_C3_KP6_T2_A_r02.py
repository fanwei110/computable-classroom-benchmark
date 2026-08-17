import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 假设 df 已包含 'fund' 列，索引为日期
def compute_rolling_sharpe(df, window=60, rf=0.021):
    daily_ret = df['fund'].pct_change().dropna()
    # 滚动年化收益率（252天），滚动波动率（样本ddof=1）
    roll_mean = daily_ret.rolling(window).mean() * 252
    roll_std = daily_ret.rolling(window).std(ddof=1) * np.sqrt(252)
    rolling_sharpe = (roll_mean - rf) / roll_std
    return rolling_sharpe.dropna()

# 示例使用
# df = pd.read_csv('your_data.csv', index_col=0, parse_dates=True)
# window = 60
# rf = 0.021
# sharpe_series = compute_rolling_sharpe(df, window, rf)

# 最后窗口数值
# last_value = sharpe_series.iloc[-1]

# 绘图保存
# fig, ax = plt.subplots()
# sharpe_series.plot(ax=ax, title=f'{window}-Day Rolling Annualized Sharpe')
# fig_path = 'rolling_sharpe.png'
# plt.savefig(fig_path)
# plt.close()

# result = {
#     'rolling_sharpe_last': round(last_value, 4),
#     'figure_path': fig_path
# }
