import numpy as np

# ==========================================
# 1. 确定 60/40 权重与两只资产的对应方式
# ==========================================
# 根据题意，"A占六成、B占四成"，即资产A权重为0.6，资产B权重为0.4
w = np.array([0.6, 0.4])

# 给定的资产年化波动率
vol_A = 0.184
vol_B = 0.297
vols = np.array([vol_A, vol_B])

# ==========================================
# 2. 构造相关系数 0.3 与 0.8 两个协方差矩阵
# ==========================================
# 相关系数矩阵（前方为0.3，后方为0.8）
corr_before = np.array([
    [1.0, 0.3],
    [0.3, 1.0]
])

corr_after = np.array([
    [1.0, 0.8],
    [0.8, 1.0]
])

# 协方差矩阵公式：Σ = D @ Corr @ D，其中 D 为标准差对角阵
D = np.diag(vols)
cov_before = D @ corr_before @ D
cov_after = D @ corr_after @ D

# ==========================================
# 3. 计算两个组合波动率
# ==========================================
# 组合方差公式：σ_p^2 = w' Σ w
var_before = w.T @ cov_before @ w
var_after = w.T @ cov_after @ w

vol_before = np.sqrt(var_before)
vol_after = np.sqrt(var_after)

# ==========================================
# 4. 填充 result
# ==========================================
result = {
    'vol_before_annual': vol_before,
    'vol_after_annual': vol_after
}

# 为方便投屏展示，格式化输出结果
print(f"相关系数 0.3 时的组合年化波动率: {result['vol_before_annual']:.4%}")
print(f"相关系数 0.8 时的组合年化波动率: {result['vol_after_annual']:.4%}")
print(f"\nresult字典完整输出: \n{result}")
