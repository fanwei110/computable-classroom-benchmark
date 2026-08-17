import pandas as pd
import numpy as np

# ===================== 1. 读取快照 CSV =====================
df = pd.read_csv('data/market_snapshot_v1.csv')

# ===================== 提取 fund 列 =====================
fund = df['fund'].dropna().values.astype(float)

# ===================== 判断 fund 是价格还是收益率 =====================
# 若全为正且最小值 > 1，大概率是价格/净值序列，需先转收益率
if np.all(fund > 0) and np.min(fund) > 1.0:
    # 视为价格 → 计算简单收益率
    returns = np.diff(fund) / fund[:-1]
else:
    # 视为收益率序列，直接使用
    returns = fund

# ===================== 推断数据频率（年化周期数） =====================
periods_per_year = 252  # 默认假设为日度数据

# 尝试从日期列推断频率
date_col = None
for col in df.columns:
    if col.lower() in ('date', 'time', '日期', '交易日期'):
        date_col = col
        break

if date_col is None:
    # 尝试第一列是否可解析为日期
    try:
        test_dates = pd.to_datetime(df.iloc[:, 0], errors='coerce')
        if test_dates.notna().sum() > len(test_dates) * 0.5:
            date_col = df.columns[0]
    except Exception:
        pass

if date_col is not None:
    try:
        dates = pd.to_datetime(df[date_col])
        diffs = dates.diff().dropna().dt.days
        median_gap = diffs.median()
        if median_gap <= 1.5:
            periods_per_year = 252   # 日度
        elif median_gap <= 8:
            periods_per_year = 52    # 周度
        elif median_gap <= 35:
            periods_per_year = 12    # 月度
        elif median_gap <= 95:
            periods_per_year = 4     # 季度
        else:
            periods_per_year = 1     # 年度
    except Exception:
        pass  # 解析失败，沿用默认日度

# ===================== 2. 计算全样本年化夏普比率 =====================
rf_annual = 0.021                     # 年化无风险利率 2.1%
rf_period = rf_annual / periods_per_year  # 每期无风险利率

excess_returns = returns - rf_period
mean_excess = np.mean(excess_returns)
std_excess = np.std(excess_returns, ddof=1)  # 样本标准差

# 夏普比率年化： Sharpe_annual = (mean / std) * sqrt(periods_per_year)
sharpe_annual = (mean_excess / std_excess) * np.sqrt(periods_per_year)

# ===================== 3. 存入 result =====================
result = {'sharpe_annual': sharpe_annual}

print(f"数据频率推断: 每年 {periods_per_year} 期")
print(f"年化无风险利率: {rf_annual:.1%}")
print(f"每期无风险利率: {rf_period:.6%}")
print(f"每期超额收益均值: {mean_excess:.6f}")
print(f"每期超额收益标准差: {std_excess:.6f}")
print(f"年化夏普比率: {sharpe_annual:.6f}")
print(result)
