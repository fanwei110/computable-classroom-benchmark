import numpy as np
from scipy.optimize import minimize

def calculate_minimum_variance_portfolio():
    """
    计算三个资产的最小方差组合（允许做空，资金全额投资）。
    
    步骤：
    1. 由年化波动率与相关系数构建协方差矩阵。
    2. 使用优化求解器寻找最小方差的权重，满足权重之和为1。
    3. 计算组合年化波动率。
    """
    # 给定参数
    vols = np.array([0.187, 0.243, 0.312])  # 年化波动率
    # 相关系数矩阵的下三角部分（不含对角线）
    corr_12 = 0.21
    corr_13 = -0.13
    corr_23 = 0.37
    
    # 构建完整的相关系数矩阵
    corr_matrix = np.array([
        [1.0,   corr_12, corr_13],
        [corr_12, 1.0,   corr_23],
        [corr_13, corr_23, 1.0 ]
    ])
    
    # 由波动率和相关系数计算协方差矩阵
    # Σ[i,j] = corr[i,j] * vol[i] * vol[j]
    cov_matrix = np.outer(vols, vols) * corr_matrix
    
    # 资产数量
    n = len(vols)
    
    # 定义目标函数：组合方差 w' Σ w
    def portfolio_variance(weights):
        return weights @ cov_matrix @ weights
    
    # 约束条件：权重之和等于1（满仓投资）
    constraints = ({'type': 'eq', 'fun': lambda w: np.sum(w) - 1.0})
    
    # 无其他约束，允许做空（权重可为负）
    bounds = None  # 或者 [(None, None)] * n
    
    # 初始猜测：等权重分配
    initial_guess = np.ones(n) / n
    
    # 使用SciPy的SLSQP求解器寻找最小方差组合
    result_opt = minimize(
        portfolio_variance,
        initial_guess,
        method='SLSQP',
        constraints=constraints,
        bounds=bounds,
        options={'disp': False, 'ftol': 1e-12}
    )
    
    # 获取最优权重
    mvp_weights = result_opt.x
    
    # 确保权重之和为1（数值误差处理）
    mvp_weights = mvp_weights / np.sum(mvp_weights)
    
    # 计算最小方差组合的年化波动率
    mvp_variance = portfolio_variance(mvp_weights)
    mvp_vol_annual = np.sqrt(mvp_variance)
    
    return mvp_weights, mvp_vol_annual, cov_matrix

# 执行计算
mvp_weights, mvp_vol_annual, cov_matrix = calculate_minimum_variance_portfolio()

# 构建输出字典
result = {
    'mvp_weights': mvp_weights.tolist(),  # 转换为列表以便JSON序列化
    'mvp_vol_annual': mvp_vol_annual
}

# 打印结果（便于课堂展示）
print("协方差矩阵:")
print(cov_matrix)
print("\n最小方差组合权重:")
for i, w in enumerate(mvp_weights, start=1):
    print(f"资产{i}: {w:.6f} ({w*100:.2f}%)")
print(f"\n权重之和: {np.sum(mvp_weights):.6f}")
print(f"组合年化波动率: {mvp_vol_annual:.6f} ({mvp_vol_annual*100:.2f}%)")

# 最终结果已按要求存储在 'result' 字典中
# 可直接被其他程序调用或序列化输出
