import numpy as np
from scipy.stats import norm
from scipy.optimize import brentq

# ==========================================
# 已知参数提取
# 格式：价格 / 行权价 / 波动率 / 利率 / 期限
# ==========================================
C_target = 103.7     # 期权价格
K = 97.5             # 行权价
sigma = 0.276        # 隐含波动率 (27.6%)
r = 0.043            # 无风险利率 (4.3%)
T = 0.58             # 期限 (年)
delta_sigma = 0.01   # IV涨1个点 (1个百分点 = 0.01)

# ==========================================
# 核心假设与推演说明：
# 1. 期权类型推断：欧式看跌期权的价格上限为 K*exp(-rT) ≈ 95.1，
#    题目给定价格为 103.7，因此该期权必定为欧式看涨期权。
# 2. 标的资产价格S：题目未直接给出，但欧式看涨期权价格是S的严格单调递增函数，
#    因此可通过 Black-Scholes 闭式解反推唯一确定的标的资产价格S。
# ==========================================

def bs_call_price(S, K, T, r, sigma):
    """Black-Scholes 欧式看涨期权定价公式"""
    if S <= 0:
        return 0.0
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

def bs_vega(S, K, T, r, sigma):
    """Black-Scholes Vega 闭式解 (对应波动率绝对值每变动1单位的价格变化)"""
    if S <= 0:
        return 0.0
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    return S * norm.pdf(d1) * np.sqrt(T)

# 步骤 1：反推标的资产价格 S
# 定义目标函数：使 BS 公式计算价格等于已知价格
def objective_func(S):
    return bs_call_price(S, K, T, r, sigma) - C_target

# 看涨期权价格严格单调递增，S 必然大于 K，设置合理的搜索区间
S_implied = brentq(objective_func, K, K * 5)

# 步骤 2：推算期权价格对1个百分点波动率变化的响应
# 利用希腊字母 Vega: ΔPrice ≈ Vega × Δσ
vega = bs_vega(S_implied, K, T, r, sigma)
price_change = vega * delta_sigma

# 将结果存入字典
result = {
    'price_change': price_change
}

# ==========================================
# 课堂投屏展示打印
# ==========================================
print("=" * 60)
print("《证券投资学》- Black-Scholes 期权希腊字母与 IV 变动响应计算")
print("=" * 60)
print(f"输入参数: 期权价格={C_target}, 行权价={K}, IV={sigma*100}%, r={r*100}%, T={T}年")
print(f"逻辑推断: 期权类型为 看涨期权 (因为价格103.7 > 行权价现值{K*np.exp(-r*T):.2f})")
print(f"步骤1反推: 标的资产价格 S = {S_implied:.4f}")
print(f"步骤2计算: Vega = {vega:.4f} (IV每变动1.0的价格响应)")
print("-" * 60)
print(f"当 IV 上涨 1 个点 (Δσ = 0.01) 时:")
print(f"期权价格变化 (Vega近似) = {price_change:.6f}")

# (附加验证：通过重新定价验证一阶希腊字母近似的精确度)
C_new = bs_call_price(S_implied, K, T, r, sigma + delta_sigma)
exact_price_change = C_new - C_target
print(f"期权价格变化 (重新定价) = {exact_price_change:.6f}")
print("-" * 60)
print(f"结论: IV涨1个点，价格大致上涨 {price_change:.4f}")
print("=" * 60)
print(f"最终输出字典 result: {result}")
