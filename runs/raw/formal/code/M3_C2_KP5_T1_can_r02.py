import numpy as np
from scipy import stats

# ==========================================
# 《证券投资学》课堂实时编程：Delta-Normal VaR 计算
# ==========================================

# --- 题目给定参数 ---
position_value = 1_850_000  # 头寸价值（元）
annual_volatility = 0.218   # 年化收益波动率

# --- 假设处理 ---
# 题目未指明一年中的交易日数，采用行业通用假设：一年包含 252 个交易日
trading_days_per_year = 252

# --- 步骤1：将年化波动率换算到一日期限 ---
# 根据平方根时间法则：sigma_daily = sigma_annual / sqrt(T)
daily_volatility = annual_volatility / np.sqrt(trading_days_per_year)

# --- 步骤2：套用正态分位数 ---
# 使用 scipy 获取标准正态分布的分位数（单侧，取绝对值因为 VaR 衡量损失）
z_95 = stats.norm.ppf(0.95)
z_99 = stats.norm.ppf(0.99)

# --- 步骤3：计算 VaR 并缩放到十日期限 ---
# (i) 95% 一日 VaR
var_95_1d = position_value * daily_volatility * z_95

# (ii) 99% 十日 VaR
# 首先将日波动率缩放至10日：sigma_10d = sigma_daily * sqrt(10)
volatility_10d = daily_volatility * np.sqrt(10)
var_99_10d = position_value * volatility_10d * z_99

# --- 步骤4：填充 result ---
result = {
    'var_95_1d': var_95_1d,
    'var_99_10d': var_99_10d
}

# --- 课堂投屏辅助输出 ---
print("="*45)
print(" Delta-Normal 参数法 VaR 计算结果")
print("="*45)
print(f"头寸价值:          ¥{position_value:>14,.2f}")
print(f"年化波动率:        {annual_volatility:>14.2%}")
print(f"一年交易日假设:    {trading_days_per_year:>14d} 天")
print("-"*45)
print(f"日化波动率:        {daily_volatility:>14.4%}")
print(f"10日波动率:        {volatility_10d:>14.4%}")
print("-"*45)
print(f"正态分布 95% 分位: {z_95:>14.4f}")
print(f"正态分布 99% 分位: {z_99:>14.4f}")
print("-"*45)
print(f"(i)  95% 一日 VaR: ¥{result['var_95_1d']:>14,.2f}")
print(f"(ii) 99% 十日 VaR: ¥{result['var_99_10d']:>14,.2f}")
print("="*45)
