import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ------------------- 已知参数 -------------------
beta = 1.42                      # 股票贝塔
market_return_monthly = -0.058   # 上个月市场收益率（小数），即 -5.8%
risk_free_rate_annual = 0.047    # 年无风险利率 4.7%

# 1. 年无风险利率按月简单折算（年/12）
risk_free_rate_monthly = risk_free_rate_annual / 12

# 2. 按月 CAPM 计算该股票的期望收益
# E(ri) = rf + beta * (E(rm) - rf)
capm_return_monthly = risk_free_rate_monthly + beta * (market_return_monthly - risk_free_rate_monthly)

# 3. 存入 result 字典
result = {
    'capm_return_monthly': capm_return_monthly
}

# 打印结果（可选）
print(f"月无风险利率: {risk_free_rate_monthly:.6f} ({risk_free_rate_monthly*100:.4f}%)")
print(f"CAPM 下该股票上月期望收益: {capm_return_monthly:.6f} ({capm_return_monthly*100:.4f}%)")
print(f"result = {result}")
