import numpy as np

def calculate_capm_return():
    # 输入参数
    beta = 1.42
    market_return_monthly = -0.058  # 市场上个月跌了5.8%
    risk_free_rate_annual = 0.047  # 年化无风险利率4.7%

    # 将年化无风险利率转换为月度无风险利率（复利计算）
    risk_free_rate_monthly = (1 + risk_free_rate_annual) ** (1/12) - 1

    # CAPM 公式：E(R_i) = R_f + beta_i * (E(R_m) - R_f)
    # 这里 E(R_m) 是市场实际收益率（上个月的），不是预期收益率
    capm_return_monthly = risk_free_rate_monthly + beta * (market_return_monthly - risk_free_rate_monthly)

    # 结果存入字典
    result = {
        'capm_return_monthly': capm_return_monthly
    }

    return result

# 计算并输出结果
result = calculate_capm_return()
print(result)
