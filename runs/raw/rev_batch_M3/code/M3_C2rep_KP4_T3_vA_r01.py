import numpy as np
from scipy.stats import norm

# ==================== 参数设定 ====================
S = 103.7      # 标的资产现价
K = 97.5       # 行权价
sigma = 0.276  # 初始波动率 (27.6%)
r = 0.043      # 无风险利率 (4.3%)
T = 0.58       # 剩余期限（年）

# ==================== BS 定价公式 ====================
def bs_call_price(S, K, T, r, sigma):
    """
    计算欧式看涨期权的 Black-Scholes 价格
    """
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    return price

# ==================== 计算价格变化 ====================
# 1. 计算当前波动率下的期权价格
price_current = bs_call_price(S, K, T, r, sigma)

# 2. 计算隐含波动率上升一个百分点（1% = 0.01）后的期权价格
sigma_new = sigma + 0.01
price_new = bs_call_price(S, K, T, r, sigma_new)

# 3. 推算期权价格对这一个百分点波动率变化的响应（精确价格变化）
price_change = price_new - price_current

# 注：也可使用希腊字母 Vega 进行一阶线性推算，结果极为接近
# d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
# vega = S * norm.pdf(d1) * np.sqrt(T)
# price_change_vega = vega * 0.01

# ==================== 输出契约 ====================
result = {
    'price_change': price_change
}

# 打印验证（供教师投屏展示）
print(f"当前波动率下的期权价格: {price_current:.4f}")
print(f"波动率上升1%后的期权价格: {price_new:.4f}")
print(f"期权价格变化量: {price_change:.4f}")
