import numpy as np
import pandas as pd

# 给定参数
beta = 1.42
market_return_monthly = -0.058   # 上个月市场收益率（小数）
annual_riskfree_rate = 0.047     # 年无风险利率（小数）

# 1. 年无风险利率 → 月无风险利率（简单除法）
monthly_riskfree_rate = annual_riskfree_rate / 12

# 2. 月度 CAPM：E(R_i) = R_f + beta * (R_m - R_f)
capm_return_monthly = monthly_riskfree_rate + beta * (market_return_monthly - monthly_riskfree_rate)

# 3. 存入结果字典
result = {
    'capm_return_monthly': capm_return_monthly
}

# 打印检查（仅供演示，投屏可运行打印）
print(result)
