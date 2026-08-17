import numpy as np

# 输入参数
beta = 1.42
market_return_monthly = -0.058   # 市场上月下跌 5.8%
rf_annual = 0.047               # 年无风险利率 4.7%

# 1. 将年无风险利率折算为月利率（复利折算，保持内部一致）
rf_monthly = (1 + rf_annual) ** (1 / 12) - 1

# 2. 在月度层面套用 CAPM 公式：E(R) = rf + beta * (Rm - rf)
capm_return_monthly = rf_monthly + beta * (market_return_monthly - rf_monthly)

# 3. 按要求存入字典
result = {
    'capm_return_monthly': capm_return_monthly
}

# 课堂投屏时输出结果
print(result)
