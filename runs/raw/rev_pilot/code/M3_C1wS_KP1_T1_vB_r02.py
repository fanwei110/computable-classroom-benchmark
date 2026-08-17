import numpy as np

# ================= 1. 输入数据 =================
# 三个资产的波动率（年化）
vols = np.array([0.187, 0.243, 0.312])

# 相关系数矩阵
# rho_12 = 0.21, rho_13 = -0.13, rho_23 = 0.37
rho = np.array([
    [1.0,  0.21, -0.13],
    [0.21, 1.0,   0.37],
    [-0.13, 0.37, 1.0 ]
])

# ================= 2. 构造协方差矩阵 =================
# Σ = diag(σ) @ Corr @ diag(σ) 等价于外积逐元素乘相关系数
cov_matrix = np.outer(vols, vols) * rho

# ================= 3. 求解最小方差组合权重 =================
# 闭式解：在满仓约束(w'1=1)下，最小方差组合权重为 w = Σ^-1 * 1 / (1' * Σ^-1 * 1)
ones = np.ones(len(vols))
inv_cov = np.linalg.inv(cov_matrix)

# 计算未归一化的权重
w_unnormalized = inv_cov @ ones

# 归一化使权重和为1
w_mvp = w_unnormalized / np.sum(w_unnormalized)

# ================= 4. 计算组合波动率 =================
# 组合方差 = w' Σ w，组合波动率 = sqrt(w' Σ w)
mvp_var = w_mvp.T @ cov_matrix @ w_mvp
mvp_vol = np.sqrt(mvp_var)

# ================= 5. 填充结果字典 =================
result = {
    'mvp_weights': w_mvp.tolist(),
    'mvp_vol_annual': float(mvp_vol)
}

# 课堂投屏展示打印
if __name__ == "__main__":
    print("马科维茨最小方差组合计算结果：")
    print(f"资产权重: {[f'{w:.4f}' for w in result['mvp_weights']]}")
    print(f"权重之和: {sum(result['mvp_weights']):.6f}")
    print(f"组合年化波动率: {result['mvp_vol_annual']:.4f} ({result['mvp_vol_annual']*100:.2f}%)")
