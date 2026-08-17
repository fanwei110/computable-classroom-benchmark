import numpy as np
from scipy import stats

# ============================================================
# 参数法（Delta-Normal）在险价值（VaR）计算
# ============================================================

# ---------- 输入参数 ----------
position    = 1_850_000    # 仓位：185万人民币
annual_vol  = 0.218        # 年化波动率：21.8%
trading_days = 252         # 一年交易日数（未指明时采用市场惯例252天）

# ---------- 步骤1：年化波动率 → 一日波动率 ----------
# 原理：σ_annual = σ_daily × sqrt(T)，故 σ_daily = σ_annual / sqrt(T)
daily_vol = annual_vol / np.sqrt(trading_days)

# ---------- 步骤2：正态分位数 ----------
z_95 = stats.norm.ppf(0.95)   # 95% 置信水平对应分位数
z_99 = stats.norm.ppf(0.99)   # 99% 置信水平对应分位数

# ---------- 步骤3：缩放至10天期限并计算VaR ----------
# Delta-Normal VaR = 仓位 × z_α × σ
# 期限缩放：σ_T = σ_1d × sqrt(T)

# 95% 置信水平，1天VaR
var_95_1d = position * z_95 * daily_vol

# 99% 置信水平，10天VaR
vol_10d   = daily_vol * np.sqrt(10)
var_99_10d = position * z_99 * vol_10d

# ---------- 输出契约 ----------
result = {
    'var_95_1d':  var_95_1d,
    'var_99_10d': var_99_10d
}

# ---------- 打印中间过程与结果（便于课堂展示） ----------
print("=" * 60)
print("参数法（Delta-Normal）VaR 计算")
print("=" * 60)
print(f"仓位：              ¥{position:>14,.2f}")
print(f"年化波动率：        {annual_vol*100:>13.1f}%")
print(f"一年交易日数：      {trading_days:>14d}")
print("-" * 60)
print(f"一日波动率：        {daily_vol*100:>13.4f}%")
print(f"十日波动率：        {vol_10d*100:>13.4f}%")
print("-" * 60)
print(f"z(95%)：            {z_95:>14.4f}")
print(f"z(99%)：            {z_99:>14.4f}")
print("=" * 60)
print(f"VaR(95%, 1天)：     ¥{var_95_1d:>14,.2f}")
print(f"VaR(99%, 10天)：    ¥{var_99_10d:>14,.2f}")
print("=" * 60)
