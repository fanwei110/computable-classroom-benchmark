"""
CAPM 月度预期收益计算脚本
- 给定年化无风险利率 4.7%，按复利折算为月利率
- 大盘上月实际收益 -5.8%
- 股票 beta = 1.42
- 计算 CAPM 框架下该股票上月的应有收益
输出：字典 result，包含键 'capm_return_monthly'
"""

import numpy as np

# 输入参数
beta = 1.42
market_return_monthly = -0.058          # 大盘上月收益率
rf_annual = 0.047                       # 年化无风险利率

# 1. 将年化无风险利率折算为月利率（有效月利率，复利折算）
rf_monthly = (1 + rf_annual) ** (1/12) - 1

# 2. 在月度层面应用 CAPM 公式：E(R_i) = R_f + beta * (E(R_m) - R_f)
capm_expected_return = rf_monthly + beta * (market_return_monthly - rf_monthly)

# 3. 填入结果字典
result = {
    'capm_return_monthly': capm_expected_return
}

# 如需查看结果（课堂投屏时可保留）
if __name__ == "__main__":
    print(f"月无风险利率: {rf_monthly:.6f} ({rf_monthly*100:.4f}%)")
    print(f"CAPM 预期月度收益: {capm_expected_return:.6f} ({capm_expected_return*100:.4f}%)")
