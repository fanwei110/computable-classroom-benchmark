# 自包含脚本：95% 1日 VaR（参数法 delta-normal）
import numpy as np
from scipy.stats import norm

# 假设：一年 252 个交易日；短期 VaR 忽略均值项，mu = 0
trading_days_per_year = 252

annual_vol = 0.24          # 年化波动率
position = 2700000.0       # 头寸金额
confidence = 0.95          # 95% 置信水平

# 1) 年化波动率换算到一日期限
daily_vol = annual_vol / np.sqrt(trading_days_per_year)

# 2) 95% 正态分位数
z_95 = norm.ppf(confidence)

# 3) 计算 95% 1日 VaR 金额，正值表示损失
var_95_1d = position * daily_vol * z_95

# 输出契约
result = {
    'var_95_1d': float(var_95_1d)
}

if __name__ == '__main__':
    print(f"日波动率: {daily_vol:.6%}")
    print(f"95% 正态分位数: {z_95:.6f}")
    print(f"95% 1日 VaR: {var_95_1d:,.2f}")
    print(result)
