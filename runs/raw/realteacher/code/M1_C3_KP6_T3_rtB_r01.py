import numpy as np
import pandas as pd

# 假设 df 是包含基金日收益的 DataFrame，fund 列为基金日收益
# 示例：df = pd.read_csv('课程数据文件.csv')

# 提取基金日收益
fund_daily_returns = df['fund'].dropna().values  # 转为 numpy 数组

# 无风险利率（年化 2.1%，按年复利）
risk_free_annual = 0.021
risk_free_daily = (1 + risk_free_annual) ** (1/252) - 1  # 日无风险利率

# 计算日超额收益
excess_daily_returns = fund_daily_returns - risk_free_daily

# 计算日超额收益的均值和标准差（ddof=1 为样本标准差）
mean_daily_excess = np.mean(excess_daily_returns)
std_daily_excess = np.std(excess_daily_returns, ddof=1)

# 年化处理
annualized_return = mean_daily_excess * 252
annualized_volatility = std_daily_excess * np.sqrt(252)

# 计算年化夏普比率
sharpe_annual = annualized_return / annualized_volatility

# 存入结果字典
result = {
    'sharpe_annual': sharpe_annual
}
