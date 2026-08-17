import numpy as np

# ===================== 输入数据 =====================
# 年化波动率
sigma = np.array([0.187, 0.243, 0.312])
# 相关系数矩阵（下三角给出，但为清晰显式定义）
corr = np.array([
    [1.0,   0.21, -0.13],
    [0.21,  1.0,   0.37],
    [-0.13, 0.37,  1.0 ]
])

# ===================== 步骤1：构造协方差矩阵 =====================
# Σ[i,j] = σ[i] * σ[j] * ρ[i,j]
cov_matrix = np.outer(sigma, sigma) * corr

# ===================== 步骤2：全局最小方差组合（允许卖空，资金全部投出） =====================
# 目标：min w' Σ w，约束：w' 1 = 1
# 闭式解：w = (Σ^{-1} 1) / (1' Σ^{-1} 1)
inv_cov = np.linalg.inv(cov_matrix)
ones = np.ones(len(sigma))
numerator = inv_cov @ ones           # Σ^{-1} 1
denominator = ones @ numerator       # 1' Σ^{-1} 1，标量
w_mvp = numerator / denominator      # 权重向量

# ===================== 步骤3：组合年化波动率 =====================
# σ_p = sqrt(w' Σ w)
var_mvp = w_mvp @ cov_matrix @ w_mvp
vol_mvp = np.sqrt(var_mvp)

# ===================== 步骤4：输出字典 =====================
result = {
    'mvp_weights': w_mvp.tolist(),  # 转为列表，便于查看
    'mvp_vol_annual': float(vol_mvp)
}

# 打印结果（投屏用）
if __name__ == "__main__":
    print("协方差矩阵：")
    print(cov_matrix)
    print("\n全局最小方差组合权重（资产1,2,3）：")
    for i, w in enumerate(w_mvp, start=1):
        print(f"  资产{i}: {w:.6f}")
    print(f"\n全局最小方差组合年化波动率：{vol_mvp:.6f} ({vol_mvp*100:.4f}%)")
    print("\n结果字典：")
    print(result)
