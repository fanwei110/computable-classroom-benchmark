import numpy as np

# 输入参数
beta = 1.42
market_return_monthly = -0.058  # 上个月大盘跌5.8%
rf_annual = 0.047  # 年化无风险利率4.7%

# 1. 将年无风险利率折算为月利率（连续复利）
rf_monthly = (1 + rf_annual) ** (1/12) - 1

# 2. 在月度层面套用CAPM公式：E(R_i) = R_f + beta_i * (E(R_m) - R_f)
capm_return_monthly = rf_monthly + beta * (market_return_monthly - rf_monthly)

# 3. 存入result字典
result = {
    'capm_return_monthly': capm_return_monthly
}

# 输出结果（供课堂展示）
print("根据CAPM模型，该股票上个月的预期收益率为：{:.4f}%".format(capm_return_monthly * 100))
print(result)
