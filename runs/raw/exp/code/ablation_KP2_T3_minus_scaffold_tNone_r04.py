import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 给定参数
beta = 1.42
market_monthly_return = -0.058           # 市场月收益率（小数）
rf_annual = 0.047                       # 无风险年利率（小数）

# 月无风险利率（简单除法）
rf_monthly = rf_annual / 12.0

# CAPM 月度期望收益：E(Ri) = Rf + beta * (Rm - Rf)
capm_return_monthly = rf_monthly + beta * (market_monthly_return - rf_monthly)

# 输出结果字典
result = {
    'capm_return_monthly': capm_return_monthly
}

# 打印结果（教师投屏）
print("按CAPM计算的该股票上个月应获得的月收益率：")
print(f"{capm_return_monthly:.6f}  (即 {capm_return_monthly*100:.2f}%)")
