import numpy as np

# ==================== 1. 参数设定 ====================
# 三只资产的年化波动率
vols = np.array([0.187, 0.243, 0.312])

# 相关系数
rho12 = 0.21
rho13 = -0.13
rho23 = 0.37

# ==================== 2. 构造协方差矩阵 ====================
# 相关系数矩阵
corr_matrix = np.array([
    [1.0,  rho12, rho13],
    [rho12, 1.0,  rho23],
    [rho13, rho23, 1.0 ]
])

# 协方差矩阵 Σ = D * R * D，其中 D 为波动率构成的对角阵
D = np.diag(vols)
cov_matrix = D @ corr_matrix @ D

# ==================== 3. 求解最小方差组合权重 ====================
# 允许卖空且满仓约束下，最小方差组合权重的闭式解为：
# w_mvp = (Σ^-1 * 1) / (1^T * Σ^-1 * 1)
ones = np.ones(3)
cov_matrix_inv = np.linalg.inv(cov_matrix)

# 计算未归一化的权重
w_unnorm = cov_matrix_inv @ ones

# 归一化使权重和为1
mvp_weights = w_unnorm / np.sum(w_unnorm)

# ==================== 4. 计算组合年化波动率 ====================
# 组合方差 w'Σw，组合波动率为其平方根
mvp_var = mvp_weights.T @ cov_matrix @ mvp_weights
mvp_vol_annual = np.sqrt(mvp_var)

# ==================== 5. 填充输出字典 ====================
result = {
    'mvp_weights': mvp_weights,
    'mvp_vol_annual': mvp_vol_annual
}

# ------------------- 课堂投屏辅助打印 -------------------
print("="*50)
print(" 马科维茨最小方差组合计算结果")
print("="*50)
print(f"协方差矩阵:\n{cov_matrix}\n")
print(f"最小方差组合权重:")
for i, w in enumerate(mvp_weights, 1):
    print(f"  资产{i}: {w:.4f} ({w*100:.2f}%)")
print(f"  权重之和: {np.sum(mvp_weights):.4f}\n")
print(f"组合年化波动率: {mvp_vol_annual:.4f} ({mvp_vol_annual*100:.2f}%)")
print("="*50)
