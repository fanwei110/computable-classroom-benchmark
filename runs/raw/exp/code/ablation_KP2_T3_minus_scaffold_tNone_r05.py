import numpy as np

# 给定参数
beta = 1.42
market_return_monthly = -0.058   # 上个月市场收益率（小数）
risk_free_annual = 0.047         # 年化无风险利率（小数）

# 将年化无风险利率转换为月度（简单除法）
risk_free_monthly = risk_free_annual / 12

# CAPM 期望收益公式（月度）:
# E(R_i) = R_f + beta * (R_m - R_f)
capm_return_monthly = risk_free_monthly + beta * (market_return_monthly - risk_free_monthly)

# 按要求存入结果字典
result = {
    'capm_return_monthly': capm_return_monthly
}

# 输出结果（课堂展示用）
print("CAPM 月度期望收益 = {:.6f} （即 {:.4f}%）".format(
    result['capm_return_monthly'], result['capm_return_monthly'] * 100))
