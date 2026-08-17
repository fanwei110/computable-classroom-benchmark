import pandas as pd
import numpy as np

# 读取数据
df = pd.read_csv('data/market_snapshot_v1.csv')

# 统一日期列名（可能存在 'date' 或 'Date'）
date_col = None
for col in df.columns:
    if col.lower() == 'date':
        date_col = col
        break

# 处理日期（如果存在）
if date_col is not None:
    df[date_col] = pd.to_datetime(df[date_col])
    df = df.sort_values(date_col).reset_index(drop=True)

# 提取 fund 列
fund_series = df['fund'].dropna()

# ---------- 判断 fund 序列是收益率还是价格 ----------
# 若有负值，肯定是收益率；若全为正值，假设为净值价格，需要计算收益率
if (fund_series < 0).any():
    # 已经是收益率序列
    returns = fund_series.copy()
    # 若绝对值最大值大于1，很可能是百分比形式（如 2.1 表示 2.1%），转为小数
    if returns.abs().max() > 1:
        returns = returns / 100.0
else:
    # 全为正值，当作净值价格
    returns = fund_series.pct_change().dropna()

# 若无日期列，默认日频，年化系数 252；否则根据间隔中位数推断频率
if date_col is None:
    annual_factor = 252
else:
    # 计算日期间隔（已排序）
    intervals = df[date_col].diff().dropna().dt.days
    if intervals.empty:
        annual_factor = 252  # 只有一条记录，回退默认
    else:
        median_interval = intervals.median()
        if median_interval <= 3:
            annual_factor = 252      # 日频
        elif median_interval <= 35:
            annual_factor = 12       # 月频
        elif median_interval <= 100:
            annual_factor = 4        # 季频
        else:
            annual_factor = 1        # 年频

# 无风险利率（年化 2.1%）
rf_annual = 0.021
rf_per_period = rf_annual / annual_factor

# 超额收益
excess_returns = returns - rf_per_period

# 年化夏普比率
sharpe_annual = excess_returns.mean() / excess_returns.std() * np.sqrt(annual_factor)

# 结果存储
result = {'sharpe_annual': sharpe_annual}

print(result)
