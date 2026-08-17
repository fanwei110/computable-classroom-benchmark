import numpy as np

# 输入参数
beta = 1.42
market_return_monthly = -0.058  # 上个月大盘跌5.8%
rf_annual = 0.047  # 年化无风险利率4.7%

# 1. 将年无风险利率折算为月利率（连续复利）
rf_monthly = (1 + rf_annual) ** (1/12) - 1

# 2. 在月度层面套用 CAPM 公式
# CAPM: E(R_i) = R_f + beta_i * (E(R_m) - R_f)
expected_return_monthly = rf_monthly + beta * (market_return_monthly - rf_monthly)

# 3. 填充 result 字典
result = {
    'capm_return_monthly': expected_return_monthly
}

# 输出结果（供教师投屏展示）
print("CAPM 预测的月度收益率:", result['capm_return_monthly'])
