import numpy as np
from scipy.stats import norm

# ========================
# 输入参数
# ========================
position_value = 1_850_000      # 头寸价值（元）
sigma_annual   = 0.218         # 年化收益波动率
trading_days   = 252           # 一年交易日数假设

# ========================
# 1. 波动率期限换算
# ========================
sigma_daily = sigma_annual / np.sqrt(trading_days)   # 日波动率

# ========================
# 2. 正态分位数
# ========================
z_95 = norm.ppf(0.95)   # 95% 单尾分位数
z_99 = norm.ppf(0.99)   # 99% 单尾分位数

# ========================
# 3. VaR 计算（零均值假设）
# ========================
# (i) 95% 一日 VaR
var_95_1d = position_value * z_95 * sigma_daily

# (ii) 99% 十日 VaR （缩放至10日）
horizon_10 = 10
sigma_10d = sigma_daily * np.sqrt(horizon_10)        # 10日波动率
var_99_10d = position_value * z_99 * sigma_10d

# 也可用年化波动率直接计算：
# var_99_10d = position_value * z_99 * sigma_annual * np.sqrt(horizon_10 / trading_days)

# ========================
# 4. 输出结果
# ========================
result = {
    'var_95_1d':  round(var_95_1d, 2),
    'var_99_10d': round(var_99_10d, 2)
}

# 打印查看（课堂投屏用）
print("=== Delta-Normal VaR 计算结果 ===")
print(f"头寸价值: {position_value:,.0f} 元")
print(f"年化波动率: {sigma_annual*100:.1f}%")
print(f"假设年交易日: {trading_days} 天")
print(f"日波动率: {sigma_daily*100:.4f}%")
print(f"95% 分位数 (z): {z_95:.5f}")
print(f"99% 分位数 (z): {z_99:.5f}")
print(f"95% 一日 VaR: {result['var_95_1d']:,.2f} 元")
print(f"99% 十日 VaR: {result['var_99_10d']:,.2f} 元")
