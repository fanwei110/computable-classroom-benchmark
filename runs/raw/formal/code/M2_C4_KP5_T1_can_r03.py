import numpy as np
from scipy.stats import norm

# ------------------------------
# 1. 给定参数
# ------------------------------
position_value = 1_850_000.0      # 头寸市值（元）
annual_vol = 0.218                # 年化收益波动率（小数）
trading_days = 252                # 每年交易日
confidence_95 = 0.95
confidence_99 = 0.99
horizon_10d = 10                  # 十日

# ------------------------------
# 2. 波动率转换
# ------------------------------
daily_vol = annual_vol / np.sqrt(trading_days)       # 日波动率
vol_10d = daily_vol * np.sqrt(horizon_10d)            # 十日波动率

# ------------------------------
# 3. 单尾正态分位数
# ------------------------------
z_95 = norm.ppf(confidence_95)   # 95% 单尾分位数
z_99 = norm.ppf(confidence_99)   # 99% 单尾分位数

# ------------------------------
# 4. 计算 VaR（均值取零，报正损失金额）
# ------------------------------
var_95_1d = position_value * daily_vol * z_95
var_99_10d = position_value * vol_10d * z_99

# ------------------------------
# 5. 输出结果字典
# ------------------------------
result = {
    'var_95_1d': var_95_1d,
    'var_99_10d': var_99_10d
}

# 若需打印，可保留以下代码
if __name__ == "__main__":
    print("=== 在险价值（Delta-Normal 参数法） ===")
    print(f"头寸市值: {position_value:,.2f} 元")
    print(f"年化波动率: {annual_vol*100:.2f}%")
    print(f"交易日/年: {trading_days}")
    print("--------------------------------------")
    print(f"95% 一日 VaR : {var_95_1d:,.2f} 元")
    print(f"99% 十日 VaR: {var_99_10d:,.2f} 元")
    print("--------------------------------------")
    print("结果字典 (result):", result)
