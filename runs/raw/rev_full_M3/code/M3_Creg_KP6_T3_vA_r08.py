import pandas as pd
import numpy as np

# 读取课程数据文件（假设文件名为 data.csv，若为其他格式或路径请按需修改此处文件名）
# 为了代码的自包含和健壮性，这里假设数据文件为同目录下的 data.csv
df = pd.read_csv('data.csv')

# 提取 fund 列
fund_data = df['fund']

# 判断 fund 列是净值还是收益率，以提高代码的健壮性
# 如果数据的最大值显著大于1（例如基金净值通常在1附近或以上），则认为是净值数据，需要计算日收益率
# 如果数据的绝对值普遍较小（在0附近波动），则认为已经是收益率数据
if fund_data.max() > 1.5:
    returns = fund_data.pct_change().dropna()
else:
    returns = fund_data

# 设定年化交易日天数（国内金融市场通常按242天或252天计算，此处采用通用的252天）
trading_days = 252

# 无风险利率设定为 2.1%
rf_annual = 0.021

# 计算日度无风险利率（简单算术平均近似，符合一般课程计算要求）
rf_daily = rf_annual / trading_days

# 计算日度超额收益的均值
mean_excess_daily = returns.mean() - rf_daily

# 计算日度收益率的标准差（样本标准差，ddof=1）
std_daily = returns.std()

# 计算年化夏普比率
# 年化夏普比率 = (日度超额收益均值 / 日度收益率标准差) * sqrt(年化交易日数)
sharpe_annual = (mean_excess_daily / std_daily) * np.sqrt(trading_days)

# 按照输出契约，将结果存入名为 result 的字典，键名为 'sharpe_annual'
result = {'sharpe_annual': sharpe_annual}

# 打印结果以供验证
print(result)
