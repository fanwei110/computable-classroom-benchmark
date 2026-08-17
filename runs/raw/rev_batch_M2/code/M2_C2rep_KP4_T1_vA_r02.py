import numpy as np
from scipy.stats import norm

# ============================================
# 输入参数
# ============================================
S = 103.7        # 标的现价
K = 97.5         # 行权价
sigma = 0.276    # 隐含波动率（年化）
r = 0.043        # 无风险利率（年化）
T = 0.58         # 剩余期限（年）

# ============================================
# 步骤1：计算 d1 与 d2
# ============================================
d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
d2 = d1 - sigma * np.sqrt(T)

# ============================================
# 步骤2：计算期权价格与 delta
# ============================================
call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
call_delta = norm.cdf(d1)

# ============================================
# 步骤3：计算 vega
# 注：vega 定义为波动率变化1个百分点（0.01）带来的期权价格变动；
# 这里的公式输出是 sigma 变化1单位（即100个百分点）的敏感度，
# 因此除以100得到平常市场所说的 vega。
# ============================================
vega_raw = S * norm.pdf(d1) * np.sqrt(T)      # 对应 sigma 变动 1（100个百分点）
call_vega = vega_raw / 100.0                  # 对应 sigma 变动 0.01（1个百分点）

# ============================================
# 步骤4：填充结果字典
# ============================================
result = {
    'call_price': call_price,
    'call_delta': call_delta,
    'call_vega': call_vega
}

# ============================================
# 输出结果（便于课堂投屏查看）
# ============================================
print("Black-Scholes 欧式看涨期权计算结果")
print("=" * 45)
print(f"标的现价 S        : {S:.4f}")
print(f"行权价 K          : {K:.4f}")
print(f"波动率 sigma      : {sigma*100:.2f}%")
print(f"无风险利率 r      : {r*100:.2f}%")
print(f"剩余期限 T        : {T:.4f} 年")
print("-" * 45)
print(f"d1                : {d1:.6f}")
print(f"d2                : {d2:.6f}")
print("-" * 45)
print(f"期权价格 (call)   : {call_price:.4f}")
print(f"Delta  (call)     : {call_delta:.4f}")
print(f"Vega   (call)     : {call_vega:.4f}  (每1个百分点波动率变动)")
print("=" * 45)

# 最终 result 字典可直接供后续使用
print("\n>>> result 字典内容：")
for k, v in result.items():
    print(f"    {k}: {v:.6f}")
