# 《证券投资学》课堂实时编程 - CAPM与证券市场线计算

# 已知数据
beta = 1.42
market_return_monthly = -0.058  # 上个月市场跌了 5.8%
risk_free_rate_annual = 0.047   # 年无风险利率 4.7%

# 步骤1：把年无风险利率折算为月利率
# 假设处理：采用单利折算方式（年利率 / 12），这在月度CAPM事后收益率计算中最为常见且与月度市场收益率口径一致。
# 若采用复利折算则为 (1 + Rf_annual)^(1/12) - 1，此处采用简单折算以保持与常规教学例题一致。
risk_free_rate_monthly = risk_free_rate_annual / 12

# 步骤2：在月度层面套用 CAPM 公式
# CAPM 公式：E(R_i) = R_f + β_i * (E(R_m) - R_f)
# 此处将上个月的市场实际收益率作为期望市场收益率的代理，计算该股票按CAPM本该有的月度收益率
capm_return_monthly = risk_free_rate_monthly + beta * (market_return_monthly - risk_free_rate_monthly)

# 步骤3：填充 result 字典
result = {
    'capm_return_monthly': capm_return_monthly
}

# 为课堂投屏展示，打印结果
if __name__ == "__main__":
    print(f"月度无风险利率: {risk_free_rate_monthly:.4%}")
    print(f"按CAPM计算的月度期望收益率: {capm_return_monthly:.4%}")
    print(f"result字典: {result}")
