import numpy as np
from scipy.stats import norm

# ==================== 参数设定 ====================
S = 103.7      # 标的资产价格
K = 97.5       # 行权价
vol = 0.276    # 波动率 (27.6%)
r = 0.043      # 无风险利率 (4.3%)
T = 0.58       # 剩余期限 (年)

# ==================== 步骤1：计算 d1 与 d2 ====================
d1 = (np.log(S / K) + (r + 0.5 * vol**2) * T) / (vol * np.sqrt(T))
d2 = d1 - vol * np.sqrt(T)

# ==================== 步骤2：计算期权价格与 delta ====================
# 欧式看涨期权价格 (无分红)
call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

# 欧式看涨期权 delta (无分红)
call_delta = norm.cdf(d1)

# ==================== 步骤3：计算 vega ====================
# vega = dV/d(vol)，数学定义为 S * sqrt(T) * N'(d1)
# 注意：此处计算的是波动率绝对量变动1时的vega，若需1%变动的vega，需再除以100
call_vega = S * np.sqrt(T) * norm.pdf(d1)

# ==================== 步骤4：填充 result ====================
result = {
    'call_price': call_price,
    'call_delta': call_delta,
    'call_vega': call_vega
}

# 课堂演示输出
if __name__ == '__main__':
    print(f"d1 = {d1:.6f}")
    print(f"d2 = {d2:.6f}")
    print("-" * 30)
    print(f"Call Price : {result['call_price']:.6f}")
    print(f"Call Delta : {result['call_delta']:.6f}")
    print(f"Call Vega  : {result['call_vega']:.6f}")
    print("-" * 30)
    print("Result Dictionary:", result)
