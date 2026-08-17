import pandas as pd
import numpy as np

# ------------------------ 1. 读取数据 ------------------------
df = pd.read_csv('data/market_snapshot_v1.csv')
print('列名:', df.columns.tolist())

# 定位 fund 列（不区分大小写）
fund_col = None
for c in df.columns:
    if 'fund' in c.lower():
        fund_col = c
        break
if fund_col is None:
    # 若只有一列，默认使用该列
    if len(df.columns) == 1:
        fund_col = df.columns[0]
    else:
        raise ValueError('找不到 fund 列，请检查 CSV 文件')

# 定位日期列（若存在）
date_col = None
for c in df.columns:
    if 'date' in c.lower():
        date_col = c
        break

if date_col:
    df[date_col] = pd.to_datetime(df[date_col])
    df.set_index(date_col, inplace=True)
    df.sort_index(inplace=True)
    # 推断数据频率 -> 年化因子
    diffs = df.index.to_series().diff().dropna()
    avg_days = diffs.mean().days
    if avg_days <= 1.5:
        annual_factor = 252      # 日度
    elif avg_days <= 10:
        annual_factor = 52       # 周度
    elif avg_days <= 35:
        annual_factor = 12       # 月度
    elif avg_days <= 100:
        annual_factor = 4        # 季度
    else:
        annual_factor = 1        # 年度或更长，保持原频
    print(f'推断数据频率：平均间隔 {avg_days:.1f} 天，年化因子 {annual_factor}')
else:
    # 无日期列，默认按日频处理
    annual_factor = 252
    print('未找到日期列，默认使用日频，年化因子 = 252')

# 提取 fund 序列
fund_series = df[fund_col].dropna().astype(float)

# 判断序列是价格/净值还是收益率
# 若出现负值认为是收益率，否则视为价格/净值，需计算百分比变化
if (fund_series < 0).any():
    returns = fund_series          # 已为收益率
    print('fund 序列含负值，视为收益率')
else:
    returns = fund_series.pct_change().dropna()
    print('fund 序列非负，计算百分比收益率')

if len(returns) == 0:
    raise ValueError('收益率序列为空，无法计算夏普比率')

# ------------------------ 2. 计算年化夏普比率 ------------------------
rf_annual = 0.021           # 年化无风险利率

mean_period = returns.mean()
std_period = returns.std(ddof=1)   # 样本标准差（无偏估计），亦可用 ddof=0，此处用1更通用

if annual_factor == 1:
    annual_return = mean_period
    annual_std = std_period
else:
    annual_return = mean_period * annual_factor
    annual_std = std_period * np.sqrt(annual_factor)

sharpe_annual = (annual_return - rf_annual) / annual_std

# ------------------------ 3. 存入结果 ------------------------
result = {'sharpe_annual': sharpe_annual}
print(result)
