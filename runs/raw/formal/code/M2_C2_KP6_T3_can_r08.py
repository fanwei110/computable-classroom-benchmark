import pandas as pd
import numpy as np

# 读取数据
df = pd.read_csv('data/market_snapshot_v1.csv')

# ----- 识别日期列与频率 ------------------------------------------------
date_col = None
for col in df.columns:
    if 'date' in col.lower():
        date_col = col
        break

if date_col is not None:
    # 存在日期列，利用时间差推断频率
    dates = pd.to_datetime(df[date_col])
    # 计算相邻时间差的中位数（以天为单位）
    diff_days = dates.diff().median() / np.timedelta64(1, 'D')
    if diff_days <= 2:
        periods_per_year = 252   # 日度
    elif 28 <= diff_days <= 31:
        periods_per_year = 12    # 月度
    elif 85 <= diff_days <= 95:
        periods_per_year = 4     # 季度
    else:
        periods_per_year = 1     # 年度（或更长）
else:
    # 无日期列，根据样本长度推断频率
    n = len(df)
    if n >= 200:
        periods_per_year = 252   # 日度
    elif n >= 20:
        periods_per_year = 12    # 月度
    else:
        periods_per_year = 4     # 季度（保守假设）

# ----- 提取 fund 列 -----------------------------------------------------
fund_col = None
for col in df.columns:
    if 'fund' in col.lower():
        fund_col = col
        break
if fund_col is None:
    raise ValueError("数据中未找到 fund 列")

fund = df[fund_col].astype(float)

# ----- 计算收益率 -------------------------------------------------------
# 若 fund 始终为正，视为净值序列，计算百分比收益率；否则直接作为收益率使用
if fund.min() > 0:
    returns = fund.pct_change().dropna()
else:
    returns = fund.dropna()   # 假设已经是收益率数据

# ----- 年化无风险利率转换为周期利率 -------------------------------------
annual_rf = 0.021
rf_period = annual_rf / periods_per_year   # 简单年化分割

# 超额收益
excess = returns - rf_period

# ----- 计算年化夏普比率 -------------------------------------------------
mean_excess = excess.mean()
std_excess = excess.std(ddof=1)            # 样本标准差
sharpe_annual = np.sqrt(periods_per_year) * mean_excess / std_excess

# ----- 输出结果 ---------------------------------------------------------
result = {'sharpe_annual': sharpe_annual}

# 仅用于课堂展示打印（不影响 result 字典）
print(result)
