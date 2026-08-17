import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy  # 仅导入以满足要求，未实际使用

# ---------------------------- 参数设置 ----------------------------
WINDOW = 60                 # 滚动窗口长度，可调
RF_ANNUAL = 0.021           # 年化无风险利率
TRADING_DAYS = 252          # 年交易日数假设
CSV_PATH = 'data/market_snapshot_v1.csv'
FIG_PATH = 'rolling_sharpe.png'

# ---------------------------- 1. 读取数据 ----------------------------
# 假设第一列为日期，已设为索引；'fund'列为基金日收益
df = pd.read_csv(CSV_PATH, parse_dates=True, index_col=0)
fund_returns = df['fund']

# ---------------------------- 2. 计算超额收益 ----------------------------
rf_daily = RF_ANNUAL / TRADING_DAYS
excess_returns = (fund_returns - rf_daily).dropna()  # 删除缺失值，保证连续交易日

# ---------------------------- 3. 滚动年化夏普比率 ----------------------------
def annualized_sharpe(series: pd.Series) -> float:
    """计算窗口内的年化夏普比率（假设日频数据）"""
    # 使用样本标准差（ddof=1）
    return series.mean() / series.std(ddof=1) * np.sqrt(TRADING_DAYS)

rolling_sharpe = excess_returns.rolling(window=WINDOW).apply(annualized_sharpe, raw=False)

# 最近一个完整窗口的夏普值（若数据不足则为NaN）
last_sharpe = rolling_sharpe.iloc[-1]
# 若为NaN则保留为None，方便JSON序列化等场景
rolling_sharpe_last = float(last_sharpe) if not np.isnan(last_sharpe) else None

# ---------------------------- 4. 画图并保存 ----------------------------
plt.figure(figsize=(12, 5))
rolling_sharpe.plot(color='navy', linewidth=1.2)
plt.title(f'{WINDOW}-Day Rolling Annualized Sharpe Ratio', fontsize=14)
plt.xlabel('Date')
plt.ylabel('Sharpe Ratio')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(FIG_PATH, dpi=150)
plt.close()

# ---------------------------- 5. 输出结果 ----------------------------
result = {
    'rolling_sharpe_last': rolling_sharpe_last,
    'figure_path': FIG_PATH
}

# 当堂运行时，教师可直接查看该字典
print(result)
