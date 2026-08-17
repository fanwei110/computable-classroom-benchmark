# 《证券投资学》课堂实时编程 - CAPM与证券市场线

# 已知参数（均用小数表示）
beta = 1.42
market_return_monthly = -0.058  # 上个月市场跌幅 5.8%
risk_free_rate_annual = 0.047   # 年化无风险利率 4.7%

# 步骤1：把年无风险利率按简单除法折算为月利率（年利率/12）
risk_free_rate_monthly = risk_free_rate_annual / 12

# 步骤2：在月度层面套用 CAPM 公式
# CAPM 公式: E(R_i) = R_f + β * (R_m - R_f)
capm_return_monthly = risk_free_rate_monthly + beta * (market_return_monthly - risk_free_rate_monthly)

# 步骤3：填充 result
result = {
    'capm_return_monthly': capm_return_monthly
}

# 课堂投屏辅助打印（验证结果用）
if __name__ == "__main__":
    print(f"月度无风险利率: {risk_free_rate_monthly:.6f}")
    print(f"按CAPM计算的上月期望收益率: {capm_return_monthly:.6f}")
    print(f"输出结果字典: {result}")
