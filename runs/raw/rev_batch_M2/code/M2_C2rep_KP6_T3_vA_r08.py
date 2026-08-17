import pandas as pd
import numpy as np

# ----------------------------
# 1. 读取数据
# ----------------------------
data_path = "data/market_snapshot_v1.csv"
df = pd.read_csv(data_path)

# 检查是否存在常见的日期列，并尝试将其设为索引以推断频率
date_col = None
for col in ['date', 'Date', 'datetime', 'Datetime', 'timestamp']:
    if col in df.columns:
        date_col = col
        break

if date_col:
    df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
    df = df.dropna(subset=[date_col])
    df = df.set_index(date_col)
else:
    print("未找到日期列，假设数据为日频数据（年化因子252）")

# 提取 fund 列（假设该列名为 'fund'）
if 'fund' not in df.columns:
    # 如果列名有大小写差异，尝试进行不区分大小写的匹配
    cols_lower = [c.lower() for c in df.columns]
    if 'fund' in cols_lower:
        fund_col = df.columns[cols_lower.index('fund')]
    else:
        raise KeyError("数据中缺少 'fund' 列，请检查列名")
else:
    fund_col = 'fund'

fund_prices = df[fund_col].astype(float)

# 计算收益率（简单收益率）
fund_returns = fund_prices.pct_change().dropna()

# ----------------------------
# 2. 确定年化因子（每年观测数）
# ----------------------------
if date_col and isinstance(df.index, pd.DatetimeIndex):
    # 根据实际日期间隔估算年化因子
    total_days = (df.index.max() - df.index.min()).days
    total_years = total_days / 365.25
    if total_years > 0:
        annual_factor = len(fund_returns) / total_years
    else:
        annual_factor = 252  # 默认日频
    # 将因子四舍五入到合理整数（例如日频252，周频52，月频12）
    if annual_factor > 240:
        annual_factor = 252
    elif annual_factor > 48:
        annual_factor = 52
    elif annual_factor > 10:
        annual_factor = 12
    else:
        annual_factor = int(round(annual_factor))
else:
    # 无日期，假定为日频数据
    annual_factor = 252

print(f"推断的年化因子（每年观测数）: {annual_factor}")

# ----------------------------
# 3. 年化夏普比率计算
# ----------------------------
rf_annual = 0.021  # 年化无风险利率 2.1%
# 每期无风险利率（简单调整：rf_annual / annual_factor）
rf_period = rf_annual / annual_factor

# 超额收益率序列
excess_returns = fund_returns - rf_period

# 年化夏普比率 = sqrt(annual_factor) * 均值(超额) / 标准差(超额)
sharpe_annual = np.sqrt(annual_factor) * excess_returns.mean() / excess_returns.std()

# ----------------------------
# 4. 存入结果字典
# ----------------------------
result = {
    'sharpe_annual': sharpe_annual
}

print("计算结果：")
print(result)
