import numpy as np

# ========================
# 1. 给定参数与权重设定
# ========================
# 年化波动率（小数形式）
sigma_A = 0.184    # 资产 A
sigma_B = 0.297    # 资产 B

# 组合权重：60% A, 40% B
w = np.array([0.6, 0.4])

# 相关系数情景
rho_before = 0.3
rho_after  = 0.8

# ========================
# 2. 计算组合波动率的函数
# ========================
def portfolio_volatility(weights, sigma_a, sigma_b, rho):
    """
    计算两资产组合的年化波动率。
    weights : [w_a, w_b]
    sigma_a, sigma_b : 年化波动率
    rho : 相关系数
    """
    cov = rho * sigma_a * sigma_b
    # 组合方差 = w_a^2 * σ_a^2 + w_b^2 * σ_b^2 + 2 * w_a * w_b * cov
    var = (weights[0]**2 * sigma_a**2 +
           weights[1]**2 * sigma_b**2 +
           2 * weights[0] * weights[1] * cov)
    return np.sqrt(var)

# ========================
# 3. 计算两种情景下的波动率
# ========================
vol_before = portfolio_volatility(w, sigma_A, sigma_B, rho_before)
vol_after  = portfolio_volatility(w, sigma_A, sigma_B, rho_after)

# ========================
# 4. 输出契约：存入字典 result
# ========================
result = {
    'vol_before_annual': vol_before,
    'vol_after_annual':  vol_after
}

# 仅供本地验证（课堂投屏执行时会显示字典内容）
if __name__ == "__main__":
    print(f"相关系数 {rho_before} 时，60/40组合年化波动率：{vol_before:.4%}")
    print(f"相关系数 {rho_after} 时，60/40组合年化波动率：{vol_after:.4%}")
    print("\nresult 字典内容：")
    print(result)
