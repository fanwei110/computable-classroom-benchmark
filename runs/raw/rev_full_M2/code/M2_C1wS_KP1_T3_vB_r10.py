import numpy as np

# 资产年化波动率（题目给出的近似值，此处使用精确小数）
sigma_A = 0.184   # 资产A波动率 18.4%
sigma_B = 0.297   # 资产B波动率 29.7%

# 组合权重：六四开，假设 A 占 60%，B 占 40%
w = np.array([0.6, 0.4])

# 两个情景的相关系数
rho_before = 0.3
rho_after  = 0.8

def portfolio_volatility(w, sigma_vec, rho):
    """
    计算给定权重、波动率向量和相关系数下的组合年化波动率
    sigma_vec: [sigma_A, sigma_B]
    rho: 相关系数
    """
    sigma_A, sigma_B = sigma_vec
    cov = rho * sigma_A * sigma_B
    Sigma = np.array([[sigma_A**2, cov],
                      [cov, sigma_B**2]])
    var = w @ Sigma @ w
    return np.sqrt(var)

# 计算两个情景的波动率
vol_before = portfolio_volatility(w, [sigma_A, sigma_B], rho_before)
vol_after  = portfolio_volatility(w, [sigma_A, sigma_B], rho_after)

# 按要求存入字典，波动率为小数形式
result = {
    'vol_before_annual': vol_before,
    'vol_after_annual': vol_after
}

# 打印结果以便课堂投屏观察
print("组合波动率（年化）：")
print(f"相关系数 0.3 时：{vol_before*100:.2f}%")
print(f"相关系数 0.8 时：{vol_after*100:.2f}%")
print("\nresult 字典内容：")
print(result)
