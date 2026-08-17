import numpy as np
from scipy.stats import norm

# --- 输入参数 ---
sigma_annual = 0.24         # 年化波动率 (24%)
position_value = 2700000    # 头寸价值（元）
confidence_level = 0.95     # 置信水平 (95%)
trading_days = 252          # 假设：一年包含252个交易日（金融市场标准惯例）

# --- 步骤 1: 把年化波动率换算到一日期限 ---
# 应用平方根时间法则 (Square-root-of-time rule): sigma_daily = sigma_annual / sqrt(T)
# 假设：短期限下预期收益率为0，波动率与时间的平方根成正比
sigma_daily = sigma_annual / np.sqrt(trading_days)

# --- 步骤 2: 套用 95% 正态分位数 ---
# 参数法(delta-normal)假设损益分布服从正态分布
# 计算 95% 置信水平下的左尾分位数，并取绝对值（VaR通常表示为正数）
z_score = abs(norm.ppf(1 - confidence_level))

# --- 步骤 3: 计算 VaR 金额 ---
# VaR = 头寸价值 × Z分位数 × 一日波动率
var_95_1d = position_value * z_score * sigma_daily

# --- 输出契约 ---
result = {
    'var_95_1d': var_95_1d
}

# --- 课堂演示打印 ---
print("="*40)
print("《证券投资学》- 在险价值(VaR)计算")
print("="*40)
print(f"1. 年化波动率: {sigma_annual:.2%}")
print(f"   一日波动率 (假设{trading_days}个交易日/年): {sigma_daily:.4%}")
print(f"2. 95% 正态分位数 (Z值): {z_score:.4f}")
print(f"3. 头寸价值: {position_value:,.2f} 元")
print("-" * 40)
print(f"=> 95% 一日 VaR: {var_95_1d:,.2f} 元")
print("="*40)
