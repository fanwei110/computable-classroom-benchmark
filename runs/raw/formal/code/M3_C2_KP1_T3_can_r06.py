import numpy as np

# ==================== 假设与参数设定 ====================
# 1. 60/40 权重对应方式：假设资产 A 占 60%，资产 B 占 40%
w_A = 0.6
w_B = 0.4
w = np.array([w_A, w_B])

# 2. 年化波动率（标准差）
vol_A = 0.184
vol_B = 0.297

# 3. 相关系数设定
rho_before = 0.3
rho_after = 0.8

# ==================== 构造协方差矩阵 ====================
# 协方差公式：Cov(A, B) = rho * vol_A * vol_B
cov_before = rho_before * vol_A * vol_B
cov_after = rho_after * vol_A * vol_B

# 资产 A 和 B 的方差
var_A = vol_A ** 2
var_B = vol_B ** 2

# 构造相关系数为 0.3 的协方差矩阵
sigma_before = np.array([
    [var_A, cov_before],
    [cov_before, var_B]
])

# 构造相关系数为 0.8 的协方差矩阵
sigma_after = np.array([
    [var_A, cov_after],
    [cov_after, var_B]
])

# ==================== 计算组合波动率 ====================
# 组合方差公式：sigma_p^2 = w' * Sigma * w
port_var_before = w.T @ sigma_before @ w
port_var_after = w.T @ sigma_after @ w

# 组合波动率（开方），即年化波动率
vol_before_annual = np.sqrt(port_var_before)
vol_after_annual = np.sqrt(port_var_after)

# ==================== 填充输出契约 ====================
result = {
    'vol_before_annual': vol_before_annual,
    'vol_after_annual': vol_after_annual
}

# （可选）课堂展示打印，便于教师投屏讲解
if __name__ == '__main__':
    print(f"资产 A 权重: {w_A:.0%}，波动率: {vol_A:.1%}")
    print(f"资产 B 权重: {w_B:.0%}，波动率: {vol_B:.1%}")
    print("-" * 40)
    print(f"相关系数 = {rho_before} 时，组合年化波动率: {result['vol_before_annual']:.4%}")
    print(f"相关系数 = {rho_after} 时，组合年化波动率: {result['vol_after_annual']:.4%}")
    increase_pct = (result['vol_after_annual'] - result['vol_before_annual']) / result['vol_before_annual']
    print(f"波动率增幅: {increase_pct:.2%}")
