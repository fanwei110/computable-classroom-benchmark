import numpy as np
import pandas as pd

# 假设 fund 是包含基金净值的 Series 或 DataFrame 列
# 示例数据（实际应替换为真实数据）
# fund = pd.Series([1.00, 1.01, 1.02, 0.99, 1.03, ...])  # 基金净值序列

# 1. 计算日收益率
daily_returns = fund.pct_change().dropna()

# 2. 年化收益率
annualized_return = daily_returns.mean() * 252

# 3. 年化波动率（样本标准差，ddof=1）
annualized_volatility = daily_returns.std(ddof=1) * np.sqrt(252)

# 4. 年化夏普比率（无风险利率 2.1%）
risk_free_rate = 0.021
sharpe_annual = (annualized_return - risk_free_rate) / annualized_volatility

# 存入结果字典
result = {
    'sharpe_annual': sharpe_annual
}
