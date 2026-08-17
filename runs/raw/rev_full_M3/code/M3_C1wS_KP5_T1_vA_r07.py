import numpy as np
from scipy.stats import norm

# ================= 输入参数 =================
position = 1_850_000  # 头寸（人民币）
ann_vol = 0.218       # 年化波动率
# 假设：一年包含252个交易日（金融市场参数法计算VaR的通行假设）
trading_days_per_year = 252 

# ================= 步骤1：年化波动率换算到一日期限 =================
# 参数法下，波动率随时间的平方根缩放：sigma_daily = sigma_annual / sqrt(T)
daily_vol = ann_vol / np.sqrt(trading_days_per_year)

# ================= 步骤2：对两个置信水平套用正态分位数 =================
# 95%和99%置信水平下的正态分布上侧分位数（由于VaR取绝对值，即损失大小，取上侧分位数）
z_95 = norm.ppf(0.95)
z_99 = norm.ppf(0.99)

# 95%置信水平的一日VaR
var_95_1d = position * z_95 * daily_vol

# ================= 步骤3：缩放到十日期限并计算99% VaR =================
# 10日波动率 = 1日波动率 * sqrt(10)
# 99%置信水平的十日VaR
var_99_10d = position * z_99 * daily_vol * np.sqrt(10)

# ================= 步骤4：填充 result =================
result = {
    'var_95_1d': var_95_1d,
    'var_99_10d': var_99_10d
}

# ================= 课堂投屏展示 =================
print("="*50)
print("《证券投资学》课堂演示：参数法计算在险价值
print("="*50)
print(f"初始头寸: {position:,.2f} 人民币")
print(f"年化波动率: {ann_vol:.1%}")
print(f"假设年交易日: {trading_days_per_year} 天")
print("-"*50)
print(f"步骤1: 一日波动率 = {ann_vol:.3f} / √{trading_days_per_year} = {daily_vol:.6f}")
print(f"步骤2: 95%分位数 Z = {z_95:.4f}, 99%分位数 Z = {z_99:.4f}")
print(f"步骤3: 十日波动率缩放比例 = √10 ≈ {np.sqrt(10):.4f}")
print("-"*50)
print(f"95%置信水平的一日VaR: {result['var_95_1d']:>12,.2f} 人民币")
print(f"99%置信水平的十日VaR: {result['var_99_10d']:>12,.2f} 人民币")
print("="*50)
