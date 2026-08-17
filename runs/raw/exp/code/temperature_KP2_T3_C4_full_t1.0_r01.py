import numpy as np
import pandas as pd

# 给定参数
beta = 1.42
market_monthly_return = -0.058   # 上月市场涨跌 -5.8%
annual_rf = 0.047               # 年无风险利率 4.7%

# 1. 将年无风险利率按简单除法折算为月利率
monthly_rf = annual_rf / 12

# 2. 月度 CAPM: E(R_i) = R_f + beta * (R_m - R_f)
capm_return_monthly = monthly_rf + beta * (market_monthly_return - monthly_rf)

# 3. 填充 result 字典
result = {
    'capm_return_monthly': capm_return_monthly
}

# 输出 result（供课堂展示）
print(result)
