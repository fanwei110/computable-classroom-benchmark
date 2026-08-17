import numpy as np

# 给定参数（小数表示）
beta = 1.42
market_return_monthly = -0.058          # 上个月市场收益率
annual_risk_free = 0.047                # 年无风险利率

# 1. 年无风险利率按简单除法折算为月利率
rf_monthly = annual_risk_free / 12

# 2. CAPM 公式：月度期望收益 = 月无风险利率 + beta * (市场月收益 - 月无风险利率)
capm_return_monthly = rf_monthly + beta * (market_return_monthly - rf_monthly)

# 3. 按要求存入字典
result = {
    'capm_return_monthly': capm_return_monthly
}

# 可供教师直接查看输出
print(result)
