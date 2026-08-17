import numpy as np
from scipy.stats import norm

# ==================== 给定参数 ====================
position = 1_850_000.0          # 头寸（元）
annual_vol = 0.218              # 年化波动率
trading_days = 252              # 一年交易日数假设
# =================================================

# --- 1. 年化波动率转换为日波动率 ---
daily_vol = annual_vol / np.sqrt(trading_days)

# --- 2. 正态分位数 ---
z_95 = norm.ppf(0.95)   # 95% 置信水平
z_99 = norm.ppf(0.99)   # 99% 置信水平

# --- 3. 计算 VaR（损失取正数） ---
var_95_1d = position * daily_vol * z_95           # 一日 95% VaR
var_99_10d = position * daily_vol * np.sqrt(10) * z_99   # 十日 99% VaR

# --- 4. 结果汇总 ---
result = {
    'var_95_1d': round(var_95_1d, 2),
    'var_99_10d': round(var_99_10d, 2)
}

# 输出到控制台，方便课堂投屏演示
print("参数法 VaR 计算结果：")
print(f"95%置信水平一日 VaR: {result['var_95_1d']:,.2f} 元")
print(f"99%置信水平十日 VaR: {result['var_99_10d']:,.2f} 元")
