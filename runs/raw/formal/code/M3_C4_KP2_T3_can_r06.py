# 《证券投资学》课堂实时编程 - CAPM 与证券市场线

# 已知参数（均用小数表示）
beta = 1.42
market_return_monthly = -0.058  # 上个月市场跌了 5.8%
risk_free_rate_annual = 0.047   # 无风险利率为每年 4.7%

# 步骤 1：把年无风险利率按简单除法折算为月利率（年利率/12）
risk_free_rate_monthly = risk_free_rate_annual / 12

# 步骤 2：在月度层面套用 CAPM
# CAPM 公式: E(R_i) = R_f + beta * (E(R_m) - R_f)
# 这里将月度市场收益率和月度无风险利率代入
capm_return_monthly = risk_free_rate_monthly + beta * (market_return_monthly - risk_free_rate_monthly)

# 步骤 3：填充 result
result = {
    'capm_return_monthly': capm_return_monthly
}

# 课堂展示辅助打印（便于投屏讲解）
print(f"月度无风险利率 R_f: {risk_free_rate_monthly:.6f} ({risk_free_rate_monthly:.4%})")
print(f"按 CAPM 计算的月度期望收益: {capm_return_monthly:.6f} ({capm_return_monthly:.4%})")
print(f"\n最终结果字典 result: {result}")
