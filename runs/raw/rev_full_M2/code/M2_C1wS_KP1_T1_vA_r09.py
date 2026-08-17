import numpy as np

# 1. 资产年化波动率与相关系数矩阵
vol = np.array([0.187, 0.243, 0.312])  # σ₁, σ₂, σ₃
rho = np.array([
    [ 1.00,  0.21, -0.13],
    [ 0.21,  1.00,  0.37],
    [-0.13,  0.37,  1.00]
])

# 2. 协方差矩阵 Σ = diag(σ) * ρ * diag(σ)
cov = np.diag(vol) @ rho @ np.diag(vol)

# 3. 最小方差组合（允许卖空，满仓 sum(w)=1）的闭式解
# w = (Σ⁻¹ 𝟏) / (𝟏ᵗ Σ⁻¹ 𝟏)
ones = np.ones(3)
inv_cov = np.linalg.inv(cov)
w = inv_cov @ ones / (ones @ inv_cov @ ones)

# 4. 组合年化波动率 = √(wᵗ Σ w)
mvp_vol = np.sqrt(w @ cov @ w)

# 5. 按要求将结果存入字典
result = {
    'mvp_weights': w.tolist(),
    'mvp_vol_annual': float(mvp_vol)
}

# 输出供课堂查看
if __name__ == "__main__":
    print("最小方差组合权重:", result['mvp_weights'])
    print("组合年化波动率:", result['mvp_vol_annual'])
