import numpy as np

# ================= 1. 参数设定与假设 =================
# 假设：题目中的"60/40组合"对应资产A权重为60%，资产B权重为40%
# （这也是传统股债配置中最经典的对应方式，即高波动资产B配40%，低波动资产A配60%）
vol_A = 0.184
vol_B = 0.297

w_A = 0.6
w_B = 0.4
weights = np.array([w_A, w_B])

rho_before = 0.3
rho_after = 0.8

# ================= 2. 构造协方差矩阵 =================
# 协方差矩阵公式: Σ = [[σ_A^2, ρ*σ_A*σ_B], [ρ*σ_A*σ_B, σ_B^2]]
cov_before = np.array([
    [vol_A**2, rho_before * vol_A * vol_B],
    [rho_before * vol_A * vol_B, vol_B**2]
])

cov_after = np.array([
    [vol_A**2, rho_after * vol_A * vol_B],
    [rho_after * vol_A * vol_B, vol_B**2]
])

# ================= 3. 计算组合波动率 =================
# 组合方差: σ_p^2 = w'Σw
var_before = weights.T @ cov_before @ weights
var_after = weights.T @ cov_after @ weights

# 年化波动率: σ_p = sqrt(σ_p^2)
vol_before_annual = np.sqrt(var_before)
vol_after_annual = np.sqrt(var_after)

# ================= 4. 填充结果 =================
# 保留4位小数以保证展示清晰度与可复现性
result = {
    'vol_before_annual': round(vol_before_annual, 4),
    'vol_after_annual': round(vol_after_annual, 4)
}

# 打印结果以供课堂投屏验证
if __name__ == "__main__":
    print(f"相关系数为 0.3 时的组合年化波动率: {result['vol_before_annual']:.2%}")
    print(f"相关系数为 0.8 时的组合年化波动率: {result['vol_after_annual']:.2%}")
    print("\n最终输出字典 result:")
    print(result)
