import numpy as np
import pandas as pd

# 已知参数
beta = 1.42
market_return_monthly = -0.058      # 上个月市场跌了5.8%
risk_free_annual = 0.047            # 无风险利率每年4.7%

# 1. 将年无风险利率按简单除法折算为月利率
risk_free_monthly = risk_free_annual / 12

# 2. CAPM公式：E(R) = Rf + beta * (Rm - Rf)
capm_return_monthly = risk_free_monthly + beta * (market_return_monthly - risk_free_monthly)

# 3. 存入结果字典
result = {
    'capm_return_monthly': capm_return_monthly
}

# 输出结果，方便课堂投屏查看
print(f"月无风险利率: {risk_free_monthly:.6f} ({risk_free_monthly*100:.4f}%)")
print(f"市场月收益率: {market_return_monthly:.6f} ({market_return_monthly*100:.4f}%)")
print(f"beta: {beta}")
print(f"按CAPM计算的上个月期望收益率: {capm_return_monthly:.6f} ({capm_return_monthly*100:.4f}%)")
print(f"\nresult字典: {result}")
