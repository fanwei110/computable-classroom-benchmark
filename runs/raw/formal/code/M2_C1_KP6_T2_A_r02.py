import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 假设 fund 是收益率序列
# fund = pd.Series(...)
rf = 0.021  # 2.1%
window = 60

# 滚动年化夏普: (mean_return - rf) / std_return * sqrt(252)
rolling_sharpe = (
    (fund.rolling(window).mean() - rf/252) / fund.rolling(window).std()
) * np.sqrt(252)

# 画图
fig, ax = plt.subplots()
rolling_sharpe.plot(ax=ax, title=f"{window}-Day Rolling Annualized Sharpe")
fig_path = "rolling_sharpe_curve.png"
fig.savefig(fig_path)
plt.close()

rolling_sharpe_last = rolling_sharpe.dropna().iloc[-1]

result = {
    "rolling_sharpe_last": rolling_sharpe_last,
    "figure_path": fig_path
}
