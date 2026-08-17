import numpy as np

# ==================== 1. 参数与假设设定 ====================
# 题目未指明60/40具体对应哪只资产，按照惯例，假设第一只提到的资产A权重为60%，资产B权重为40%
w_A, w_B = 0.6, 0.4
w = np.array([w_A, w_B])

# 资产A与B的年化波动率
vol_A = 0.184  # 18.4%
vol_B = 0.297  # 29.7%

# 相关系数
rho_before = 0.3
rho_after = 0.8

# ==================== 2. 构造协方差矩阵 ====================
def get_cov_matrix(vol_A, vol_B, rho):
    """根据波动率和相关系数构造协方差矩阵"""
    cov_AB = rho * vol_A * vol_B
    cov_matrix = np.array([
        [vol_A**2, cov_AB],
        [cov_AB, vol_B**2]
    ])
    return cov_matrix

cov_before = get_cov_matrix(vol_A, vol_B, rho_before)
cov_after  = get_cov_matrix(vol_A, vol_B, rho_after)

# ==================== 3. 计算组合波动率 ====================
def calc_portfolio_vol(w, cov_matrix):
    """计算组合波动率: sqrt(w'Σw)"""
    port_var = w.T @ cov_matrix @ w
    return np.sqrt(port_var)

vol_before_annual = calc_portfolio_vol(w, cov_before)
vol_after_annual  = calc_portfolio_vol(w, cov_after)

# ==================== 4. 填充结果 ====================
result = {
    'vol_before_annual': vol_before_annual,
    'vol_after_annual': vol_after_annual
}

# ==================== 课堂投屏展示辅助 ====================
if __name__ == "__main__":
    print("="*50)
    print("马科维茨均值-方差组合理论 - 组合波动率计算")
    print("="*50)
    print(f"假设: 资产A权重 = {w_A:.0%}, 资产B权重 = {w_B:.0%}")
    print(f"资产A波动率 = {vol_A:.1%}, 资产B波动率 = {vol_B:.1%}\n")
    
    print(f"【情景1】相关系数 = {rho_before}")
    print(f"协方差矩阵:\n{cov_before}")
    print(f"组合年化波动率: {vol_before_annual:.4%}\n")
    
    print(f"【情景2】相关系数 = {rho_after}")
    print(f"协方差矩阵:\n{cov_after}")
    print(f"组合年化波动率: {vol_after_annual:.4%}\n")
    
    print("="*50)
    print("输出契约字典 result:")
    print(result)
