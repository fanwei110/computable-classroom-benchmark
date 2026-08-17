import numpy as np

# ========== 输入参数 ==========
beta = 1.42
market_return_monthly = -0.058          # 市场上月收益率（小数）
risk_free_rate_annual = 0.047           # 年化无风险利率

# ========== 计算 ==========
# 将年化无风险利率转换为月（简单除以12）
risk_free_rate_monthly = risk_free_rate_annual / 12

# CAPM 公式：E(R_i) = R_f + beta * (E(R_m) - R_f)
capm_return_monthly = risk_free_rate_monthly + beta * (market_return_monthly - risk_free_rate_monthly)

# ========== 存储结果 ==========
result = {
    'capm_return_monthly': capm_return_monthly
}

# ========== 显示 ==========
print("按CAPM，该股票上个月期望收益率（月，小数形式）：")
print(result['capm_return_monthly'])
