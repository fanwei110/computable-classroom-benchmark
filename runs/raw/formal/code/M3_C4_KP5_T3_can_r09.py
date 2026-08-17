import numpy as np
from scipy.stats import norm

# 1. 定义已知参数（小数表示）
sigma_annual = 0.24       # 年化波动率 24%
position = 2700000        # 头寸金额 2,700,000 元
trading_days = 252        # 每年交易日数

# 2. 按每年 252 个交易日把年化波动率去年化到一日
# 波动率按 sqrt(T) 缩放
sigma_daily = sigma_annual / np.sqrt(trading_days)

# 3. 使用单尾 95% 正态分位数，均值取零
z_95 = norm.ppf(0.95)

# 计算 95% 一日 VaR（报告为正的损失金额）
var_95_1d = position * z_95 * sigma_daily

# 4. 将结果存入指定格式的字典
result = {
    'var_95_1d': var_95_1d
}

# 供课堂投屏验证打印
print(f"日波动率: {sigma_daily:.6f}")
print(f"95%正态分位数 (Z值): {z_95:.6f}")
print(f"95% 一日 VaR: {var_95_1d:.2f} 元")
print(f"结果字典: {result}")
