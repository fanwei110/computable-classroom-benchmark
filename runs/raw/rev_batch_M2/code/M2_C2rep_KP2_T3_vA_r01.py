import numpy as np

# 给定参数
beta = 1.42
market_return_monthly = -0.058        # 上个月市场跌了5.8%
risk_free_annual = 0.047              # 年化无风险利率4.7%

# 将年无风险利率折算为月利率
# 假设：年利率为名义年利率，按月单利折算（教学中常见处理）
risk_free_monthly = risk_free_annual / 12.0

# 按CAPM计算该股票上个月的期望月度收益
# CAPM: E(R_i) = R_f + beta * (E(R_m) - R_f)
capm_return_monthly = risk_free_monthly + beta * (market_return_monthly - risk_free_monthly)

# 输出契约
result = {
    'capm_return_monthly': capm_return_monthly
}

if __name__ == "__main__":
    print(result)
