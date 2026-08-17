import numpy as np
from scipy.stats import norm

# =====================
# 1. 参数与假设设定
# =====================
position_value = 1_850_000.0  # 头寸价值（元）
sigma_annual = 0.218          # 年化收益波动率

# 假设：一年包含252个交易日（金融学Delta-Normal参数法下的行业标准假设）
trading_days_per_year = 252

# =====================
# 2. 年化波动率换算到一日期限
# =====================
# 在独立同分布假设下，日波动率 = 年化波动率 / sqrt(交易日天数)
sigma_daily = sigma_annual / np.sqrt(trading_days_per_year)

# =====================
# 3. 套用正态分位数
# =====================
# 使用 scipy.stats.norm.ppf 计算标准正态分布的累积概率逆函数
z_95 = norm.ppf(0.95)
z_99 = norm.ppf(0.99)

# =====================
# 4. 计算并缩放 VaR
# =====================
# (i) 95% 一日 VaR
# 公式：VaR = 头寸价值 × Z分数 × 日波动率
var_95_1d = position_value * z_95 * sigma_daily

# (ii) 99% 十日 VaR
# 时间缩放法则：多期VaR = 单期VaR × sqrt(期限)
# 公式：VaR = 头寸价值 × Z分数 × 日波动率 × sqrt(10)
var_99_10d = position_value * z_99 * sigma_daily * np.sqrt(10)

# =====================
# 5. 填充 result 字典
# =====================
result = {
    'var_95_1d': var_95_1d,
    'var_99_10d': var_99_10d
}

# 投屏展示输出
print("--- 在险价值计算结果 ---")
print(f"日波动率: {sigma_daily:.6f}")
print(f"95% 一日 VaR: ¥{result['var_95_1d']:,.2f}")
print(f"99% 十日 VaR: ¥{result['var_99_10d']:,.2f}")
