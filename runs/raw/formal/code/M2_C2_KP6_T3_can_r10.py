import pandas as pd
import numpy as np

# 1. 读取数据
df = pd.read_csv('data/market_snapshot_v1.csv')

# 提取fund列收益率，剔除缺失值
fund = df['fund'].dropna()

# 2. 推断数据频率，确定年化因子
if 'date' in df.columns:
    df['date'] = pd.to_datetime(df['date'])
    # 计算相邻日期的时间间隔，取中位数（天）
    intervals = df['date'].diff().dropna()
    median_days = intervals.median().days
    if median_days <= 1:          # 日频
        annual_factor = 252
    elif median_days <= 7:        # 周频
        annual_factor = 52
    elif median_days <= 31:       # 月频
        annual_factor = 12
    else:                         # 年频或更长
        annual_factor = 1
else:
    # 若无日期列，默认按日频处理
    annual_factor = 252

# 3. 设定无风险利率（年化）
rf_annual = 0.021

# 4. 计算年化收益率与年化标准差
mean_ret = fund.mean()
std_ret = fund.std()

annual_mean = mean_ret * annual_factor
annual_std = std_ret * np.sqrt(annual_factor)

# 5. 计算年化夏普比率
sharpe = (annual_mean - rf_annual) / annual_std

# 6. 存入结果字典
result = {'sharpe_annual': sharpe}

print(result)
