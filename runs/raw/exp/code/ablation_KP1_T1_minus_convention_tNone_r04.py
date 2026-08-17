import numpy as np
import pandas as pd

# ========== 第1步：构造协方差矩阵 ==========
# 年化波动率
vol = np.array([0.187, 0.243, 0.312])

# 相关系数矩阵
corr_matrix = np.array([
    [1.0,   0.21, -0.13],
    [0.21,  1.0,   0.37],
    [-0.13, 0.37,  1.0 ]
])

# 协方差矩阵 = 波动率对角矩阵 @ 相关系数矩阵 @ 波动率对角矩阵
D = np.diag(vol)
cov_matrix = D @ corr_matrix @ D

print("协方差矩阵：")
print(pd.DataFrame(cov_matrix, 
                   index=['资产1','资产2','资产3'], 
                   columns=['资产1','资产2','资产3']))

# ========== 第2步：求全局最小方差组合权重（闭式解，允许卖空，满仓）==========
# 闭式解：w = (Σ^(-1) * 1) / (1' * Σ^(-1) * 1)
n = cov_matrix.shape[0]
ones = np.ones(n)
inv_cov = np.linalg.inv(cov_matrix)
mvp_weights = inv_cov @ ones / (ones @ inv_cov @ ones)

print("\n全局最小方差组合权重：")
for i, w in enumerate(mvp_weights, 1):
    print(f"资产{i}: {w:.6f} ({w*100:.2f}%)")
print(f"权重之和: {mvp_weights.sum():.8f}")

# ========== 第3步：计算组合年化波动率 ==========
mvp_variance = mvp_weights @ cov_matrix @ mvp_weights
mvp_vol_annual = np.sqrt(mvp_variance)

print(f"\n组合年化波动率: {mvp_vol_annual:.6f} ({mvp_vol_annual*100:.2f}%)")

# ========== 第4步：按要求打包结果 ==========
result = {
    'mvp_weights': mvp_weights,      # numpy数组，形状(3,)
    'mvp_vol_annual': mvp_vol_annual # 浮点数（小数形式）
}

# 验证结果正确性
print("\n====== 结果字典内容 ======")
print("mvp_weights:", result['mvp_weights'])
print("mvp_vol_annual:", result['mvp_vol_annual'])
