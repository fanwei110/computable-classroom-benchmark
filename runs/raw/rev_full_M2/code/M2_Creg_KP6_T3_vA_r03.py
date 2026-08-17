import numpy as np
import pandas as pd

# ========================
# 读取数据
# ========================
# 假设数据文件名为 data.csv，其中包含一个名为 'fund' 的列
# 该列可以是每日净值（价格）或每日收益率（小数形式）
df = pd.read_csv('data.csv')

# 确保 fund 列存在
if 'fund' not in df.columns:
    raise ValueError("数据文件必须包含 'fund' 列")

fund = df['fund'].dropna()

# ========================
# 判断数据类型并计算日收益率
# ========================
# 如果 fund 的值域类似价格（均大于1），则计算日收益率
if fund.min() > 1:
    # 认定为净值序列，计算日收益率
    returns = fund.pct_change().dropna()
else:
    # 认定为收益率序列
    returns = fund

# 若收益率序列因缺失值等因素为空，则报错
if len(returns) == 0:
    raise ValueError("计算得到的收益率序列为空，请检查数据")

# ========================
# 参数设定
# ========================
rf_annual = 0.021          # 年化无风险利率 2.1%
trading_days = 252         # 假设每日数据，一年252个交易日

# 日化无风险利率
rf_daily = rf_annual / trading_days

# ========================
# 计算年化夏普比率
# ========================
# 超额日收益率
excess_returns = returns - rf_daily

# 日均超额收益 & 日超额收益标准差
mean_excess_daily = excess_returns.mean()
std_excess_daily = excess_returns.std(ddof=1)   # 使用样本标准差

# 年化夏普比率 = (日均超额收益 / 日超额收益标准差) * sqrt(252)
sharpe_annual = (mean_excess_daily / std_excess_daily) * np.sqrt(trading_days)

# ========================
# 输出结果
# ========================
result = {
    'sharpe_annual': sharpe_annual
}

print(result)
