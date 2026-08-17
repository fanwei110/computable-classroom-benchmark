import numpy as np
from scipy.stats import norm

# ---------------------------- 输入参数 ----------------------------
value = 1_850_000.0          # 头寸价值（人民币元）
annual_vol = 0.218           # 年化收益波动率
trading_days = 252           # 年交易日数（市场惯例）
confidence_95 = 0.95         # 置信水平 95%
confidence_99 = 0.99         # 置信水平 99%
horizon_10d = 10             # 10 日期限（交易日）

# ---------------------------- 波动率换算 ----------------------------
# 将年化波动率转换为日波动率
daily_vol = annual_vol / np.sqrt(trading_days)
# 10 日波动率（基于独立同分布假设）
vol_10d = daily_vol * np.sqrt(horizon_10d)

# ---------------------------- 正态分位数 ----------------------------
# 对于损失分位数，VaR 取收益分布的左尾绝对值
# 95% VaR 对应标准正态的 95% 分位数（正值，约为 1.64485）
z_95 = norm.ppf(confidence_95)
# 99% VaR 对应标准正态的 99% 分位数（正值，约为 2.32635）
z_99 = norm.ppf(confidence_99)

# --------------------------- 计算 VaR ---------------------------
# 1 日 95% VaR
var_95_1d = value * daily_vol * z_95
# 10 日 99% VaR
var_99_10d = value * vol_10d * z_99

# ----------------------------- 结果 -----------------------------
result = {
    'var_95_1d': var_95_1d,      # 浮点数，完整精度
    'var_99_10d': var_99_10d
}

# 将结果打印以便课堂投屏展示（保留两位小数，符合货币惯例）
print(f"头寸价值：{value:,.0f} 元")
print(f"年化波动率：{annual_vol*100:.1f}%")
print(f"1 日 95% VaR：{var_95_1d:,.2f} 元")
print(f"10 日 99% VaR：{var_99_10d:,.2f} 元")
print("\n结果字典：")
print(result)
