import numpy as np

# 给定参数
beta = 1.42
market_return_monthly = -0.058  # 上个月市场收益率（小数）
risk_free_annual = 0.047        # 年化无风险利率（小数）

# 按简单除法折算为月度无风险利率
risk_free_monthly = risk_free_annual / 12

# CAPM 公式：E(R_i) = R_f + beta * (E(R_m) - R_f)
# 这里 R_f、R_m 均为月度值
capm_return_monthly = risk_free_monthly + beta * (market_return_monthly - risk_free_monthly)

# 按要求存入字典
result = {
    'capm_return_monthly': capm_return_monthly
}

# 打印结果（教师投屏用）
print("CAPM 期望月收益率（小数形式）：", round(result['capm_return_monthly'], 6))
print("即大约", round(result['capm_return_monthly'] * 100, 4), "%")
