import numpy as np
import pandas as pd

# ============================
# 1. 给定参数（小数形式）
# ============================
sigma_A = 0.184    # 资产 A 年化波动率
sigma_B = 0.297    # 资产 B 年化波动率
w_A = 0.60         # A 权重
w_B = 0.40         # B 权重

rho_before = 0.3   # 原相关系数
rho_after  = 0.8   # 新相关系数

# ============================
# 2. 协方差矩阵与组合波动率计算函数
# ============================
def portfolio_vol(w1, w2, s1, s2, rho):
    """计算两资产组合的年化波动率（小数）"""
    cov = rho * s1 * s2
    var = w1**2 * s1**2 + w2**2 * s2**2 + 2 * w1 * w2 * cov
    return np.sqrt(var)

# ============================
# 3. 计算两个情景下的组合波动率
# ============================
vol_before = portfolio_vol(w_A, w_B, sigma_A, sigma_B, rho_before)
vol_after  = portfolio_vol(w_A, w_B, sigma_A, sigma_B, rho_after)

# ============================
# 4. 结果存入字典
# ============================
result = {
    'vol_before_annual': vol_before,
    'vol_after_annual':  vol_after
}

# ============================
# 5. 输出结果（便于投屏观察）
# ============================
print("资产 A 年化波动率: {:.3%}".format(sigma_A))
print("资产 B 年化波动率: {:.3%}".format(sigma_B))
print("权重 (A/B): {:.0%}/{:.0%}".format(w_A, w_B))
print("-" * 40)
print("相关系数 {:.1f} 时组合年化波动率: {:.4%}".format(rho_before, vol_before))
print("相关系数 {:.1f} 时组合年化波动率: {:.4%}".format(rho_after, vol_after))
print("\nresult 字典内容:")
print(result)
