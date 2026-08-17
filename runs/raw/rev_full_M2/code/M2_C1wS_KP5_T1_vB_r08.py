import numpy as np
from scipy.stats import norm

# =========================
# 参数设定
# =========================
position = 1_850_000          # 仓位（人民币元）
annual_vol = 0.218            # 年化波动率
trading_days = 252            # 一年交易日数，业界常用假设
confidence_95 = 0.95          # 95% 置信水平
confidence_99 = 0.99          # 99% 置信水平
horizon_10d = 10              # 十日期限

# =========================
# 计算日波动率
# =========================
daily_vol = annual_vol / np.sqrt(trading_days)

# =========================
# 正态分布分位数
# 使用单尾分位数的绝对值，因为 VaR 定义为损失的正数
# norm.ppf(1 - confidence) 给出负值，取其绝对值得到正的分位数
z_95 = abs(norm.ppf(1 - confidence_95))   # ≈ 1.6449
z_99 = abs(norm.ppf(1 - confidence_99))   # ≈ 2.3263

# =========================
# 计算 VaR
# =========================
var_95_1d = position * daily_vol * z_95
var_99_10d = position * daily_vol * np.sqrt(horizon_10d) * z_99

# =========================
# 结果存入字典（单位：人民币元，保留两位小数）
# =========================
result = {
    'var_95_1d': round(var_95_1d, 2),
    'var_99_10d': round(var_99_10d, 2)
}

if __name__ == "__main__":
    print(result)
