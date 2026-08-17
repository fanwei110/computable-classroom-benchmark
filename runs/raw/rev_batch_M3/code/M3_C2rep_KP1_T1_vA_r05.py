import numpy as np

# ==================== 1. 输入参数 ====================
# 三只风险资产的年化波动率
vols = np.array([0.187, 0.243, 0.312])

# 相关系数 (键为资产索引对，从0起)
corrs_dict = {
    (0, 1): 0.21,
    (0, 2): -0.13,
    (1, 2): 0.37
}

# ==================== 2. 构造协方差矩阵 ====================
n_assets = len(vols)
cov_matrix = np.zeros((n_assets, n_assets))

for i in range(n_assets):
    for j in range(n_assets):
        if i == j:
            # 对角线元素为方差
            cov_matrix[i, j] = vols[i] ** 2
        elif i < j:
            # 非对角线元素为协方差: cov(i,j) = corr(i,j) * vol_i * vol_j
            cov_matrix[i, j] = corrs_dict[(i, j)] * vols[i] * vols[j]
            cov_matrix[j, i] = cov_matrix[i, j]

# ==================== 3. 求全局最小方差组合权重 ====================
ones = np.ones(n_assets)
cov_matrix_inv = np.linalg.inv(cov_matrix)

# 马科维茨最小方差组合闭式解: w_mvp = (Σ^-1 * 1) / (1^T * Σ^-1 * 1)
# 此闭式解自动满足资金全部投出（权重和为1）的约束
w_mvp = (cov_matrix_inv @ ones) / (ones @ cov_matrix_inv @ ones)

# ==================== 4. 计算组合年化波动率 ====================
# 组合方差 = w'Σw
var_mvp = w_mvp.T @ cov_matrix @ w_mvp
# 组合年化波动率 = sqrt(w'Σw)
vol_mvp = np.sqrt(var_mvp)

# ==================== 5. 按契约组装输出结果 ====================
result = {
    'mvp_weights': w_mvp.tolist(),
    'mvp_vol_annual': float(vol_mvp)
}

# ==================== 课堂展示打印 ====================
print("====== 马科维茨全局最小方差组合(GMVP)计算结果 ======")
print(f"组合权重 (mvp_weights): {result['mvp_weights']}")
print(f"年化波动率 (mvp_vol_annual): {result['mvp_vol_annual']:.6f} (即 {result['mvp_vol_annual']*100:.4f}%)")
print("\n完整输出字典 `result`：")
print(result)
