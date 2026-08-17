import numpy as np
import pandas as pd

# 假设您的课程数据文件已读入为 DataFrame，名为 df
# df = pd.read_csv('您的课程数据文件.csv')

# 1. 提取基金日收益列
fund_daily = df['fund']

# 2. 设定参数（按小数表示）
rf_annual = 0.021    # 2.1% 的年复利无风险利率
trading_days = 252   # 每年交易日

# 3. 将年复利无风险利率转换为日复利利率
rf_daily = (1 + rf_annual) ** (1 / trading_days) - 1

# 4. 计算日超额收益
excess_daily = fund_daily - rf_daily

# 5. 计算日均超额收益与日收益率的样本标准差 (ddof=1)
mean_excess = excess_daily.mean()
std_daily = fund_daily.std(ddof=1)  # 减去常数不改变标准差

# 6. 计算年化 Sharpe Ratio
sharpe_annual = (mean_excess / std_daily) * np.sqrt(trading_days)

# 7. 按输出契约存入字典
result = {'sharpe_annual': sharpe_annual}

# 打印结果
print(result)
