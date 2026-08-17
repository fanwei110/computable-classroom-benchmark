import numpy as np

# 给定数据
beta = 1.42
market_return_monthly = -0.058          # 大盘上月下跌 5.8%
rf_annual = 0.047                      # 年化无风险利率 4.7%

# 1. 将年化无风险利率折算为月无风险利率
# 假设采用简单利率折算（算术平均），即 rf_monthly = rf_annual / 12
rf_monthly = rf_annual / 12.0

# 2. 套用 CAPM 公式
# E(R_i) = R_f + beta_i * (E(R_m) - R_f)
capm_return_monthly = rf_monthly + beta * (market_return_monthly - rf_monthly)

# 3. 填充结果字典
result = {
    'capm_return_monthly': capm_return_monthly
}

# 简单输出，方便教师检查
if __name__ == "__main__":
    print(f"月无风险利率: {rf_monthly:.6f} ({rf_monthly*100:.4f}%)")
    print(f"市场月超额收益: {market_return_monthly - rf_monthly:.6f} ({ (market_return_monthly - rf_monthly)*100:.4f}%)")
    print(f"CAPM 预期月收益率: {capm_return_monthly:.6f} ({capm_return_monthly*100:.4f}%)")
    print("结果字典 result:", result)
