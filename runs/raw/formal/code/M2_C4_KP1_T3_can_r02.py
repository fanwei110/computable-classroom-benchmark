import numpy as np

# --- 给定参数 ---
sigma_A_annual = 0.184   # A 的年化波动率
sigma_B_annual = 0.297   # B 的年化波动率
w_A = 0.60               # A 的权重
w_B = 0.40               # B 的权重

rho_low = 0.3            # 原相关系数
rho_high = 0.8           # 新相关系数

def portfolio_vol(w1, w2, s1, s2, rho):
    """计算两资产组合的年化波动率"""
    cov = rho * s1 * s2
    variance = (w1**2) * (s1**2) + (w2**2) * (s2**2) + 2 * w1 * w2 * cov
    return np.sqrt(variance)

# 计算相关系数为 0.3 时的组合波动率
vol_before = portfolio_vol(w_A, w_B, sigma_A_annual, sigma_B_annual, rho_low)

# 计算相关系数为 0.8 时的组合波动率
vol_after  = portfolio_vol(w_A, w_B, sigma_A_annual, sigma_B_annual, rho_high)

# 结果存入字典
result = {
    'vol_before_annual': vol_before,   # 相关系数 0.3 时的年化波动率（小数）
    'vol_after_annual':  vol_after     # 相关系数 0.8 时的年化波动率（小数）
}

# 课堂展示输出
print("组合波动率计算结果（小数形式）")
print(f"相关系数  0.3  ->  年化波动率 = {vol_before:.4f}  ({vol_before*100:.2f}%)")
print(f"相关系数  0.8  ->  年化波动率 = {vol_after:.4f}  ({vol_after*100:.2f}%)")
print("\n字典 result:", result)
