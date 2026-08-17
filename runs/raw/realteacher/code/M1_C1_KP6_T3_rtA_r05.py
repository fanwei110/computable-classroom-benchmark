import numpy as np

# 假设 fund_returns 是 fund 列的日收益率序列（pandas Series 或 numpy array）
# 示例代码（实际应用中需替换为真实数据）：
# fund_returns = df['fund']  # 从数据文件中读取

# 日化无风险利率
risk_free_daily = (1 + 0.021) ** (1/252) - 1

# 计算日超额收益
excess_returns = fund_returns - risk_free_daily

# 计算年化夏普比率
sharpe_annual = np.sqrt(252) * excess_returns.mean() / excess_returns.std()

# 存入结果字典
result = {
    'sharpe_annual': sharpe_annual
}
