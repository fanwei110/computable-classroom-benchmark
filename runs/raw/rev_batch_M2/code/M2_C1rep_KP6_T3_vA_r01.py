import pandas as pd
import numpy as np

# 假设已经加载了课程数据，fund列包含基金收益率数据
# 这里用示例数据演示计算过程
# 实际应用中应使用课程提供的完整fund数据

# 计算年化收益率
# 假设数据为日收益率
annual_return = fund.mean() * 252  # 年化平均收益率

# 计算年化波动率
annual_volatility = fund.std() * np.sqrt(252)  # 年化标准差

# 计算年化夏普比率
risk_free_rate = 0.021  # 2.1%无风险利率
sharpe_annual = (annual_return - risk_free_rate) / annual_volatility

# 存储结果
result = {
    'sharpe_annual': sharpe_annual
}
