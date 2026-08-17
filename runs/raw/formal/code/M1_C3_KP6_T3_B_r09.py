import numpy as np
import pandas as pd

# 假设 fund 是基金的日收益率序列（pandas Series）
# rf 是年化无风险利率，2.1% = 0.021

def calculate_sharpe(fund, rf=0.021):
    # 计算年化收益率（几何平均）
    annualized_return = (1 + fund).prod() ** (252 / len(fund)) - 1

    # 计算年化波动率（样本标准差 * sqrt(252)）
    annualized_vol = fund.std(ddof=1) * np.sqrt(252)

    # 计算夏普比率
    sharpe_annual = (annualized_return - rf) / annualized_vol

    return {'sharpe_annual': sharpe_annual}

# 示例用法（假设 fund 是日收益率序列）
# result = calculate_sharpe(fund)
# print(result)
