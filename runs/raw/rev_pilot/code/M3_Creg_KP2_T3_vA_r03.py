import numpy as np

# 已知参数
beta = 1.42                      # 股票的 Beta 值
market_return_monthly = -0.058   # 上个月市场收益率 (-5.8%)
risk_free_rate_annual = 0.047    # 年化无风险利率 (4.7%)

# 将年化无风险利率转换为月度无风险利率
# 采用简单算术平均的方法（年利率 / 12），以匹配单月的市场收益率周期
risk_free_rate_monthly = risk_free_rate_annual / 12

# 根据 CAPM 模型计算上个月的预期收益率
# 公式: E(R_i) = R_f + beta * (E(R_m) - R_f)
capm_return_monthly = risk_free_rate_monthly + beta * (market_return_monthly - risk_free_rate_monthly)

# 按照输出契约，将结果存入字典
result = {
    'capm_return_monthly': capm_return_monthly
}

# 打印结果以供验证
print(result)
