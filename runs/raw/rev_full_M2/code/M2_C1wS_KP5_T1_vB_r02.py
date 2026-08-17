import numpy as np
from scipy.stats import norm

# ============================================================
# 参数法 (Delta-Normal) VaR 计算
# ============================================================

# 给定参数
position_value = 1_850_000          # 仓位价值（人民币元）
annual_vol = 0.218                  # 年化波动率
trading_days = 252                  # 假设一年252个交易日

# --- 步骤 1: 年化波动率换算为日波动率 ---
daily_vol = annual_vol / np.sqrt(trading_days)

# --- 步骤 2: 获取正态分布分位数 ---
z_95 = norm.ppf(0.05)   # 95% 置信水平（左尾 5%）
z_99 = norm.ppf(0.01)   # 99% 置信水平（左尾 1%）

# --- 步骤 3: 计算 VaR ---

# VaR_95_1day: 95% 置信水平，1 天持有期
var_95_1d = position_value * (-z_95) * daily_vol
# 注意：z_95 本身为负值，取 -z_95 得到正数，再乘以仓位和日波动率

# VaR_99_10day: 99% 置信水平，10 天持有期（采用平方根法则缩放）
var_99_10d = position_value * (-z_99) * daily_vol * np.sqrt(10)

# --- 步骤 4: 填充结果字典 ---
result = {
    'var_95_1d': round(var_95_1d, 2),    # 人民币元，保留两位小数
    'var_99_10d': round(var_99_10d, 2)
}

# --- 打印结果 ---
print("=" * 55)
print("参数法 (Delta-Normal) 在险价值 (VaR)")
print("=" * 55)
print(f"仓位价值:         {position_value:>12,.2f} 元")
print(f"年化波动率:       {annual_vol*100:>12.2f}%")
print(f"日波动率:         {daily_vol*100:>12.4f}%")
print(f"交易日/年:        {trading_days:>12d}")
print("-" * 55)
print(f"Z(95%) 分位数:    {z_95:>12.6f}")
print(f"Z(99%) 分位数:    {z_99:>12.6f}")
print("-" * 55)
print(f"VaR 95%, 1天:     {result['var_95_1d']:>12,.2f} 元")
print(f"VaR 99%, 10天:    {result['var_99_10d']:>12,.2f} 元")
print("=" * 55)

# 结果字典已准备就绪
