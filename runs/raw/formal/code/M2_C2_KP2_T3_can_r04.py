import numpy as np

# 给定参数
beta = 1.42
market_return_monthly = -0.058  # 上个月市场跌了5.8%
risk_free_annual = 0.047        # 年无风险利率 4.7%

# 将年无风险利率折算为月利率：
# 假设采用单利折算（年利率/12），这是证券投资学中常见的简化处理
risk_free_monthly = risk_free_annual / 12

# 按照CAPM计算该股票上个月的预期收益率
# CAPM公式：E(R_i) = R_f + beta * (E(R_m) - R_f)
capm_return_monthly = risk_free_monthly + beta * (market_return_monthly - risk_free_monthly)

# 保存结果至字典
result = {
    'capm_return_monthly': capm_return_monthly
}

# 输出结果，便于课堂投屏
print("=== CAPM 月度预期收益率计算结果 ===")
print(f"年无风险利率: {risk_free_annual*100:.2f}%")
print(f"折算后月无风险利率: {risk_free_monthly*100:.4f}%")
print(f"市场月度收益率: {market_return_monthly*100:.2f}%")
print(f"股票 beta: {beta}")
print(f"股票月度预期收益率 (CAPM): {capm_return_monthly*100:.4f}%")
print("\n要求的 result 字典内容：")
print(result)
