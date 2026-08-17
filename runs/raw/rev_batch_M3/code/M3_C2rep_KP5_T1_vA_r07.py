import numpy as np
from scipy.stats import norm

# ==================== 已知参数 ====================
V = 1_850_000          # 头寸价值（元）
sigma_annual = 0.218   # 年化收益波动率

# ==================== 假设 ====================
# 假设一年有 252 个交易日，这是金融市场参数法计算的最通行假设
trading_days_per_year = 252

# ==================== 步骤 1：年化波动率换算到一日期限 ====================
# 波动率与时间的平方根成正比：sigma_daily = sigma_annual / sqrt(T)
sigma_daily = sigma_annual / np.sqrt(trading_days_per_year)

# ==================== 步骤 2：套用正态分位数计算 95% 一日 VaR ====================
# Delta-normal 模型下：VaR = 头寸价值 × 日波动率 × 正态分布分位数
# 95% 置信水平对应的左尾分位数
z_95 = norm.ppf(0.95)
var_95_1d = V * sigma_daily * z_95

# ==================== 步骤 3：缩放到十日期限并计算 99% 十日 VaR ====================
# 99% 置信水平对应的正态分布分位数
z_99 = norm.ppf(0.99)

# 运用 square-root-of-time 法则将 1 日波动率缩放至 10 日
sigma_10d = sigma_daily * np.sqrt(10)

# 计算 99% 十日 VaR
var_99_10d = V * sigma_10d * z_99

# ==================== 步骤 4：填充 result ====================
result = {
    'var_95_1d': var_95_1d,
    'var_99_10d': var_99_10d
}

# ==================== 课堂输出展示 ====================
print(f"--- 参数法计算在险价值 ---")
print(f"头寸价值: {V:,.2f} 元")
print(f"年化波动率: {sigma_annual:.2%}")
print(f"日波动率 (按252日换算): {sigma_daily:.6f}")
print(f"10日波动率: {sigma_10d:.6f}")
print(f"-" * 30)
print(f"95% 一日 VaR: {result['var_95_1d']:,.2f} 元")
print(f"99% 十日 VaR: {result['var_99_10d']:,.2f} 元")
