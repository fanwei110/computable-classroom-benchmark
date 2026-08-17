import numpy as np

# ==========================================
# 马科维茨均值-方差组合理论：最小方差组合计算
# ==========================================

# 1. 已知数据设定（波动率与相关系数采用小数形式，确保计算内部一致）
vols = np.array([0.187, 0.243, 0.312])
corr_matrix = np.array([
    [1.00,  0.21, -0.13],
    [0.21,  1.00,  0.37],
    [-0.13, 0.37,  1.00]
])

# 2. 由波动率与相关系数构造协方差矩阵 Σ
# 公式: Σ = D * Corr * D, 其中 D = diag(σ)
D = np.diag(vols)
cov_matrix = D @ corr_matrix @ D

# 3. 求最小方差权重（闭式解）
# 在仅约束满仓(w之和为1)且允许做空的情况下，最小方差组合权重闭式解为:
# w_mvp = Σ^(-1) * 1 / (1^T * Σ^(-1) * 1), 其中1为全1向量
inv_cov = np.linalg.inv(cov_matrix)
ones = np.ones(3)

# 计算权重
w_mvp = (inv_cov @ ones) / (ones @ inv_cov @ ones)

# 4. 计算组合波动率
# 组合方差: σ_p^2 = w^T Σ w
# 组合波动率: σ_p = sqrt(w^T Σ w)
var_mvp = w_mvp @ cov_matrix @ w_mvp
vol_mvp = np.sqrt(var_mvp)

# 5. 按要求键名填充 result 字典
result = {
    'mvp_weights': w_mvp.tolist(),
    'mvp_vol_annual': vol_mvp
}

# ----------------- 课堂投屏展示 -----------------
print("=" * 45)
print(" 马科维茨最小方差组合(MVP)计算结果")
print("=" * 45)
print(f"资产权重 (资产1, 资产2, 资产3):")
for i, w in enumerate(result['mvp_weights']):
    print(f"  资产{i+1}: {w:8.4%}")
print(f"权重之和验证: {sum(result['mvp_weights']):.8f} (应为1.0)")
print("-" * 45)
print(f"最小方差组合年化波动率: {result['mvp_vol_annual']:8.4%}")
print("=" * 45)
