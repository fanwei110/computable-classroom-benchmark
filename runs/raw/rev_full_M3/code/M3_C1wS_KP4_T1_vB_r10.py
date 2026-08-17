import numpy as np
from scipy.stats import norm

# ================= 假设与参数设定 =================
# 标的资产价格
S = 103.7
# 行权价
K = 97.5
# 波动率 (年化)
vol = 0.276
# 无风险利率 (年化连续复利)
r = 0.043
# 剩余期限 (年)
T = 0.58

# ================= 步骤1：计算 d1 与 d2 =================
d1 = (np.log(S / K) + (r + 0.5 * vol**2) * T) / (vol * np.sqrt(T))
d2 = d1 - vol * np.sqrt(T)

# ================= 步骤2：计算期权价格与 delta =================
# 欧式看涨期权价格 (Black-Scholes 闭式解，不分红)
call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

# 欧式看涨期权 delta (不分红标的)
call_delta = norm.cdf(d1)

# ================= 步骤3：计算 vega =================
# vega 的数学定义为对波动率的一阶偏导数，Call与Put相等
# 注：此处按数学严格定义计算。若需实务中"vol变动1%对应价格变动"的数值，需将此结果除以100。
call_vega = S * np.sqrt(T) * norm.pdf(d1)

# ================= 步骤4：填充 result =================
result = {
    'call_price': call_price,
    'call_delta': call_delta,
    'call_vega': call_vega
}

# ================= 课堂投屏展示辅助 =================
if __name__ == "__main__":
    print("=" * 40)
    print("Black-Scholes 欧式看涨期权定价与希腊字母")
    print("=" * 40)
    print(f"参数: S={S}, K={K}, vol={vol*100}%, r={r*100}%, T={T}年")
    print("-" * 40)
    print(f"d1       = {d1:.6f}")
    print(f"d2       = {d2:.6f}")
    print("-" * 40)
    print(f"Call 价格 = {result['call_price']:.4f}")
    print(f"Call Delta= {result['call_delta']:.6f}")
    print(f"Call Vega = {result['call_vega']:.4f} (数学偏导值，即vol变动1单位的价格变动)")
    print("=" * 40)
