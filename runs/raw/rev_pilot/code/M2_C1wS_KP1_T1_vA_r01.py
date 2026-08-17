import numpy as np

# 资产参数
vol = np.array([0.187, 0.243, 0.312])          # 年化波动率
# 相关系数矩阵
corr = np.array([
    [1.00, 0.21, -0.13],
    [0.21, 1.00,  0.37],
    [-0.13,0.37,  1.00]
])

# 1. 构建协方差矩阵
# 协方差 = 相关系数 * 标准差_i * 标准差_j
std = vol.reshape(-1, 1)   # 列向量
cov_matrix = corr * (std @ std.T)

# 2. 最小方差组合（允许卖空，满仓约束 sum(w)=1）
# 闭式解：w = Σ^{-1} 1 / (1^T Σ^{-1} 1)
inv_cov = np.linalg.inv(cov_matrix)
ones = np.ones(len(vol))
lambda_ = 1.0 / (ones @ inv_cov @ ones)   # λ = 1/(1^T Σ^{-1} 1)
mvp_weights = lambda_ * (inv_cov @ ones)  # w* = λ Σ^{-1} 1

# 3. 组合年化波动率
mvp_variance = mvp_weights @ cov_matrix @ mvp_weights
mvp_vol_annual = np.sqrt(mvp_variance)

# 4. 填入结果
result = {
    'mvp_weights': mvp_weights.tolist(),  # 列表形式
    'mvp_vol_annual': float(mvp_vol_annual)
}

# 打印输出，便于教师投屏
print("最小方差组合（允许卖空，全额投资）")
print("权重：", result['mvp_weights'])
print("年化波动率：", result['mvp_vol_annual'])

# 如果需要，脚本执行后 result 字典可用
