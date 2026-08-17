import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 给定参数
beta = 1.42
market_return_monthly = -0.058           # 上月市场收益率（-5.8%）
risk_free_annual = 0.047                # 年无风险利率 4.7%

# 1. 年无风险利率折算为月利率（简单除法）
risk_free_monthly = risk_free_annual / 12

# 2. 月度CAPM：E(ri) = rf + beta * (rm - rf)
capm_return_monthly = risk_free_monthly + beta * (market_return_monthly - risk_free_monthly)

# 3. 输出结果字典
result = {
    'capm_return_monthly': capm_return_monthly
}

# 显示结果
print("月无风险利率:", risk_free_monthly)
print("CAPM 期望月度收益率:", capm_return_monthly)
