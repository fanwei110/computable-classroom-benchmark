import numpy as np
# 我们只需要 numpy，但根据要求保留其他库的导入（虽然未使用）
import scipy
import pandas as pd
import matplotlib

# 给定参数
beta = 1.42
market_return_monthly = -5.8 / 100  # 市场月收益率（小数）
risk_free_rate_annual = 4.7 / 100  # 年化无风险利率（小数）

# 将年化无风险利率转换为月利率（假设简单线性折算，因为CAPM通常用期间利率）
# 注意：CAPM 中无风险利率应与市场收益率的期间匹配，这里市场是月度，故用月无风险利率
risk_free_rate_monthly = risk_free_rate_annual / 12

# CAPM: E(R_i) = R_f + beta * (E(R_m) - R_f)
# 这里 E(R_m) 用实际市场收益率代替（假设市场预期实现为实际）
expected_return_monthly = risk_free_rate_monthly + beta * (market_return_monthly - risk_free_rate_monthly)

# 按照输出契约存储
result = {
    'capm_return_monthly': expected_return_monthly
}

# 输出结果（小数点后保留足够精度）
print(f"按CAPM计算的月度期望收益率为: {result['capm_return_monthly']:.6f} 或 {result['capm_return_monthly']*100:.4f}%")
