import numpy as np

# 给定参数
beta = 1.42
market_return_monthly = -0.058  # 市场月度收益 -5.8%
risk_free_annual = 0.047       # 年无风险利率 4.7%

# 步骤1：将年无风险利率折算为月利率
# 使用 (1 + r_annual)^(1/12) - 1 的精确复利折算方式
risk_free_monthly = (1 + risk_free_annual) ** (1 / 12) - 1

# 步骤2：CAPM 公式：E(R_i) = R_f + beta * (E(R_m) - R_f)
# 其中 E(R_m) 就是实际观察到的市场收益（作为已实现的期望代理）
capm_return_monthly = risk_free_monthly + beta * (market_return_monthly - risk_free_monthly)

# 步骤3：填充结果字典
result = {
    'capm_return_monthly': capm_return_monthly
}

# 打印结果以便查看
print(f"年无风险利率: {risk_free_annual:.4f}")
print(f"折算后月无风险利率: {risk_free_monthly:.6f}")
print(f"市场月度收益: {market_return_monthly:.4f}")
print(f"股票 beta: {beta}")
print(f"按 CAPM 计算的月度期望收益: {capm_return_monthly:.6f}")
print(f"\n结果字典: {result}")
