import numpy as np

# 定义输入参数
beta = 1.42
market_return_monthly = -0.058  # 上个月市场收益率 -5.8%
risk_free_rate_annual = 0.047   # 年化无风险利率 4.7%

# 将年化无风险利率转换为月度无风险利率
# 采用最常见的简单折算方法（年化利率除以12）
risk_free_rate_monthly = risk_free_rate_annual / 12

# 根据 CAPM 公式计算该股票上个月本该的预期收益率
# CAPM 公式: E(R_i) = R_f + Beta * (E(R_m) - R_f)
capm_return_monthly = risk_free_rate_monthly + beta * (market_return_monthly - risk_free_rate_monthly)

# 按照输出契约，将结果存入名为 result 的字典
result = {
    'capm_return_monthly': capm_return_monthly
}

# 打印结果以供验证
print(f"该股票上个月本该的 CAPM 收益率为: {capm_return_monthly:.6f} (即 {capm_return_monthly*100:.4f}%)")
print("结果字典:", result)
