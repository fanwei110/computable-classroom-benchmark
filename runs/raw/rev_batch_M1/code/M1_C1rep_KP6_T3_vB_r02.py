import numpy as np

# 示例数据（请替换为实际值）
annual_return = 0.10  # 基金年化收益率（10%）
annual_volatility = 0.15  # 基金年化波动率（15%）
rf = 0.021  # 无风险收益率（2.1%）

# 计算年化夏普比率
sharpe_annual = (annual_return - rf) / annual_volatility

# 存入结果字典
result = {
    'sharpe_annual': sharpe_annual
}

print(result)
