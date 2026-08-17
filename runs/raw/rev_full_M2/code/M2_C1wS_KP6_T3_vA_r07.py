import pandas as pd
import numpy as np

# 读取数据快照
df = pd.read_csv('快照.csv')

# ---------- 日期处理 ----------
date_col = None
for col in ['Date', 'date', '日期']:
    if col in df.columns:
        date_col = col
        break

if date_col is not None:
    df[date_col] = pd.to_datetime(df[date_col])
    df.set_index(date_col, inplace=True)
    df.sort_index(inplace=True)

# ---------- 提取基金序列 ----------
fund = df['fund']

# 判断数据是净值还是收益率
# 若最小值为负或绝对值普遍小于0.5，视为收益率；否则视为净值
if fund.min() < 0 or (fund.abs() < 0.5).all():
    returns = fund.dropna()
else:
    # 视作净值，计算简单收益率
    returns = fund.pct_change().dropna()

# ---------- 推断年化频率 ----------
if date_col is not None and len(df) > 2:
    time_diffs = df.index.to_series().diff().dropna()
    median_seconds = time_diffs.median().total_seconds()
    median_days = median_seconds / (24 * 3600)

    if median_days <= 2:
        periods_per_year = 252      # 日频
    elif median_days <= 9:
        periods_per_year = 52       # 周频
    elif median_days <= 35:
        periods_per_year = 12       # 月频
    elif median_days <= 100:
        periods_per_year = 4        # 季频
    else:
        periods_per_year = 1        # 年频
else:
    # 缺少日期信息时默认按日频处理
    periods_per_year = 252

# ---------- 夏普比率计算 ----------
annual_rf = 0.021                     # 年化无风险利率
period_rf = annual_rf / periods_per_year

excess_returns = returns - period_rf

# 年化夏普比率 = sqrt(周期数) * (平均超额收益 / 收益标准差)
# 使用样本标准差 (ddof=1)，若需总体标准差可改为 ddof=0
sharpe_annual = np.sqrt(periods_per_year) * excess_returns.mean() / excess_returns.std(ddof=1)

# ---------- 输出 ----------
result = {'sharpe_annual': sharpe_annual}

if __name__ == '__main__':
    print(result)
