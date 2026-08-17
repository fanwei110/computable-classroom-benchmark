import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

# 给定参数
beta = 1.42
market_return_monthly = -0.058          # 市场月收益率（小数）
annual_risk_free_rate = 0.047           # 年无风险利率（小数）

# 1. 年无风险利率折算为月利率（简单除法）
monthly_risk_free_rate = annual_risk_free_rate / 12

# 2. 月度CAPM：E(R_i) = R_f + beta * (R_m - R_f)
capm_return_monthly = monthly_risk_free_rate + beta * (market_return_monthly - monthly_risk_free_rate)

# 3. 存入结果字典
result = {
    'capm_return_monthly': capm_return_monthly
}

# 输出结果（供教师投屏展示）
print("=== CAPM 月度期望收益计算 ===")
print(f"月无风险利率: {monthly_risk_free_rate:.6f} ({monthly_risk_free_rate*100:.4f}%)")
print(f"市场月收益率: {market_return_monthly:.4f} ({market_return_monthly*100:.2f}%)")
print(f"Beta: {beta}")
print(f"按CAPM计算的股票月度期望收益: {capm_return_monthly:.6f} ({capm_return_monthly*100:.4f}%)")
print("\nresult 字典内容:")
print(result)
