import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

# 给定参数
beta = 1.42
market_return_monthly = -0.058  # 市场月收益率，-5.8%
risk_free_rate_annual = 0.047   # 年无风险利率 4.7%

# 步骤1: 年无风险利率 -> 月无风险利率 (简单除法)
risk_free_rate_monthly = risk_free_rate_annual / 12

# 步骤2: 月度CAPM公式: E(R_i) = R_f + beta * (R_m - R_f)
capm_return_monthly = risk_free_rate_monthly + beta * (market_return_monthly - risk_free_rate_monthly)

# 步骤3: 填充result字典
result = {
    'capm_return_monthly': capm_return_monthly
}

# 输出结果
print("月无风险利率:", risk_free_rate_monthly)
print("CAPM月度期望收益:", capm_return_monthly)
print("result字典:", result)
