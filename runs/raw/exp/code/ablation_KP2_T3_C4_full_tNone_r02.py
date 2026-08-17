import numpy as np
import pandas as pd

# 给定参数
beta = 1.42
market_return_monthly = -0.058   # 上月市场收益（已用小数表示，-5.8%）
risk_free_rate_annual = 0.047   # 年化无风险利率 4.7%

# 1. 把年无风险利率按简单除法折算为月利率
risk_free_rate_monthly = risk_free_rate_annual / 12

# 2. 在月度层面套用 CAPM
# CAPM: E(R_i) = R_f + beta * (R_m - R_f)
# R_m 与 R_f 均为月收益率
capm_return_monthly = risk_free_rate_monthly + beta * (market_return_monthly - risk_free_rate_monthly)

# 3. 填充 result 字典
result = {
    'capm_return_monthly': capm_return_monthly
}

# 输出结果（供课堂投屏参考）
print("无风险月利率:", risk_free_rate_monthly)
print("CAPM 月度期望收益:", capm_return_monthly)
