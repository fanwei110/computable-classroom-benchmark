import pandas as pd
import numpy as np

# ==============================
# 1. 读取数据并提取 fund 列
# ==============================
df = pd.read_csv("data/market_snapshot_v1.csv")

# 假设数据中存在 'fund' 列
fund = df['fund']

# 如果 fund 列是价格数据（净值），自动转换为简单收益率
# 判断条件：如果序列的最小值 > 0 且没有出现负值（价格特征），求差分收益率
if fund.min() > 0 and not (fund < 0).any():
    # 可能是价格序列，转换为日收益率
    fund = fund.pct_change().dropna()
    # 如果原始是价格，计算后需要重新对齐索引
    fund = fund.reset_index(drop=True)

# 如果 fund 值明显是百分比形式（均值 > 1），转换为小数
if fund.mean() > 1:
    fund = fund / 100.0

# ==============================
# 2. 确定数据频率及年化参数
# ==============================
# 优先根据日期列判断，如果不存在日期列则按行数判断
if 'date' in df.columns or 'Date' in df.columns or 'DATE' in df.columns:
    date_col = df.columns[df.columns.str.lower() == 'date'][0]
    dates = pd.to_datetime(df[date_col])
    # 计算相邻日期的平均间隔天数
    delta_days = dates.diff().dropna().dt.days.mean()
    if delta_days <= 2:
        annual_factor = np.sqrt(252)
        freq_str = 'daily'
    elif delta_days <= 31:
        annual_factor = np.sqrt(12)
        freq_str = 'monthly'
    else:
        # 季度或更长，取12/间隔月数
        months_per_year = 12 / (delta_days / 30.4375)
        annual_factor = np.sqrt(months_per_year)
        freq_str = f'{delta_days/30.4375:.1f} months'
else:
    # 无日期列，根据样本长度推断频率：>200 认为日度，否则月度
    if len(fund) > 200:
        annual_factor = np.sqrt(252)
        freq_str = 'daily (inferred)'
    else:
        annual_factor = np.sqrt(12)
        freq_str = 'monthly (inferred)'

# 确保 fund 没有缺失值
fund = fund.dropna()

# ==============================
# 3. 设置无风险利率并计算超额收益
# ==============================
rf_annual = 0.021  # 2.1% 年化无风险利率

# 将年化无风险利率转换为对应频率
if freq_str.startswith('daily'):
    rf_period = rf_annual / 252
elif freq_str.startswith('monthly'):
    rf_period = rf_annual / 12
else:
    # 通用，按照每年周期数计算
    periods_per_year = (annual_factor) ** 2  # 因为 annual_factor = sqrt(periods)
    rf_period = rf_annual / periods_per_year

excess_returns = fund - rf_period

# ==============================
# 4. 计算年化夏普比率
# ==============================
mean_excess = excess_returns.mean()
std_excess = excess_returns.std()  # 样本标准差，除以 N-1（与 pd.std() 默认一致）

if std_excess == 0:
    sharpe_annual = np.nan
else:
    sharpe_annual = (mean_excess / std_excess) * annual_factor

# ==============================
# 5. 结果输出
# ==============================
result = {
    'sharpe_annual': sharpe_annual
}

print(f"数据频率: {freq_str}")
print(f"年化无风险利率: {rf_annual*100:.2f}%")
print(f"年化夏普比率: {sharpe_annual:.4f}")
