import pandas as pd
import numpy as np

# 1. 读取快照 CSV
df = pd.read_csv('data/market_snapshot_v1.csv')

# 无风险利率设定为 2.1%
rf_annual = 0.021

# 自动推断数据频率（默认假设为日度数据，一年252个交易日）
annualization_factor = 252
# 尝试通过日期列推断数据频率
date_col = None
if 'date' in df.columns:
    date_col = 'date'
elif 'Date' in df.columns:
    date_col = 'Date'

if date_col:
    try:
        df[date_col] = pd.to_datetime(df[date_col])
        df = df.sort_values(date_col)
        time_diffs = df[date_col].diff().dt.days.dropna()
        if len(time_diffs) > 0:
            median_diff = time_diffs.median()
            if median_diff > 20:   # 月度数据
                annualization_factor = 12
            elif median_diff > 5:   # 周度数据
                annualization_factor = 52
            # 否则维持默认的252（日度）
    except Exception:
        pass

# 提取 fund 列
fund_series = df['fund']

# 判断 fund 列是净值/价格序列还是收益率序列
# 若绝对值均值较大（如大于0.5），通常为净值/价格序列，需计算百分比收益率；否则视为已是收益率
if fund_series.abs().mean() > 0.5:
    returns = fund_series.pct_change().dropna()
else:
    returns = fund_series.copy()
    # 若为百分比数值（如 1.5 代表 1.5%），需除以100
    if returns.abs().mean() > 0.1:  
        returns = returns / 100.0

# 2. 计算全样本年化夏普比率
mean_period = returns.mean()
std_period = returns.std()

# 期间无风险利率
rf_period = rf_annual / annualization_factor

# 年化夏普比率公式: (期间平均收益 - 期间无风险利率) / 期间收益标准差 * sqrt(年化因子)
sharpe_annual = (mean_period - rf_period) / std_period * np.sqrt(annualization_factor)

# 3. 把结果存入 result
result = {'sharpe_annual': sharpe_annual}

# 输出结果以便教师投屏查看
print(f"年化夏普比率: {sharpe_annual:.4f}")
print(f"结果字典: {result}")
