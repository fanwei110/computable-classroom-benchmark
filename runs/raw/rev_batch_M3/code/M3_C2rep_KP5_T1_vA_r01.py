import numpy as np
from scipy import stats

# ============================================================
# 在险价值（VaR）计算 —— Delta-Normal（参数法）
# ============================================================

# ---------- 输入参数 ----------
V = 1_850_000          # 头寸价值（元）
sigma_annual = 0.218   # 年化收益波动率

# ---------- 步骤1：年化波动率 → 一日波动率 ----------
# 假设：一年 252 个交易日（市场惯例）
trading_days_per_year = 252
sigma_daily = sigma_annual / np.sqrt(trading_days_per_year)

# ---------- 步骤2：正态分位数 ----------
z_95 = stats.norm.ppf(0.95)   # 单侧 95% 分位数 ≈ 1.6449
z_99 = stats.norm.ppf(0.99)   # 单侧 99% 分位数 ≈ 2.3263

# ---------- (i) 95% 一日 VaR ----------
var_95_1d = V * sigma_daily * z_95

# ---------- 步骤3：缩放到十日期限 ----------
# Delta-normal 下，波动率按 sqrt(T) 缩放
sigma_10d = sigma_daily * np.sqrt(10)

# ---------- (ii) 99% 十日 VaR ----------
var_99_10d = V * sigma_10d * z_99

# ---------- 输出 ----------
print("=" * 50)
print("VaR 计算结果（Delta-Normal 参数法）")
print("=" * 50)
print(f"头寸价值:           {V:>14,.2f} 元")
print(f"年化波动率:         {sigma_annual:>14.2%}")
print(f"一年交易日:         {trading_days_per_year:>14d} 天")
print("-" * 50)
print(f"一日波动率:         {sigma_daily:>14.6f}")
print(f"十日波动率:         {sigma_10d:>14.6f}")
print(f"z(95%):             {z_95:>14.4f}")
print(f"z(99%):             {z_99:>14.4f}")
print("-" * 50)
print(f"95% 一日 VaR:       {var_95_1d:>14,.2f} 元")
print(f"99% 十日 VaR:       {var_99_10d:>14,.2f} 元")
print("=" * 50)

# ---------- 按契约存入 result ----------
result = {
    'var_95_1d': var_95_1d,
    'var_99_10d': var_99_10d
}
