import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import minimize

# ==================== 步骤1：构造协方差矩阵 ====================

# 三只风险资产的年化波动率
vol_1 = 0.187  # 18.7%
vol_2 = 0.243  # 24.3%
vol_3 = 0.312  # 31.2%

# 相关系数矩阵
corr_12 = 0.21
corr_13 = -0.13
corr_23 = 0.37

# 构建相关系数矩阵
corr_matrix = np.array([
    [1.0,    corr_12, corr_13],
    [corr_12, 1.0,    corr_23],
    [corr_13, corr_23, 1.0]
])

# 构造协方差矩阵：Σ = D * R * D，其中D是对角线为波动率的对角矩阵
vol_vector = np.array([vol_1, vol_2, vol_3])
D = np.diag(vol_vector)
cov_matrix = D @ corr_matrix @ D

print("协方差矩阵 Σ：")
print(cov_matrix)
print()

# ==================== 步骤2：求最小方差权重 ====================

# 方法1：使用闭式解（允许卖空，满仓约束）
# 最小方差组合权重公式：w_mvp = (Σ^(-1) * 1) / (1^T * Σ^(-1) * 1)

n_assets = 3
ones_vector = np.ones(n_assets)

# 计算协方差矩阵的逆
cov_matrix_inv = np.linalg.inv(cov_matrix)

# 计算最小方差组合权重
w_mvp = cov_matrix_inv @ ones_vector / (ones_vector.T @ cov_matrix_inv @ ones_vector)

print("全局最小方差组合权重：")
print(f"资产1 (波动率 {vol_1*100:.1f}%): {w_mvp[0]:.6f} ({w_mvp[0]*100:.4f}%)")
print(f"资产2 (波动率 {vol_2*100:.1f}%): {w_mvp[1]:.6f} ({w_mvp[1]*100:.4f}%)")
print(f"资产3 (波动率 {vol_3*100:.1f}%): {w_mvp[2]:.6f} ({w_mvp[2]*100:.4f}%)")
print(f"权重之和: {np.sum(w_mvp):.10f}")
print()

# 验证：使用优化器求解，确保结果一致
def portfolio_variance(weights):
    return weights @ cov_matrix @ weights

# 约束条件：权重和为1
constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
# 无边界约束（允许卖空）
bounds = tuple([(None, None) for _ in range(n_assets)])
# 初始猜测：等权重
initial_guess = np.array([1/3, 1/3, 1/3])

result_opt = minimize(portfolio_variance, initial_guess, method='SLSQP', 
                      bounds=bounds, constraints=constraints)
w_mvp_opt = result_opt.x

print("优化器求解的全局最小方差组合权重：")
print(f"资产1: {w_mvp_opt[0]:.6f} ({w_mvp_opt[0]*100:.4f}%)")
print(f"资产2: {w_mvp_opt[1]:.6f} ({w_mvp_opt[1]*100:.4f}%)")
print(f"资产3: {w_mvp_opt[2]:.6f} ({w_mvp_opt[2]*100:.4f}%)")
print(f"权重之和: {np.sum(w_mvp_opt):.10f}")
print()
print("两种方法权重差异：", np.max(np.abs(w_mvp - w_mvp_opt)))

# 选择闭式解作为最终结果
w_final = w_mvp

# ==================== 步骤3：计算组合年化波动率 ====================

portfolio_variance_value = w_final @ cov_matrix @ w_final
portfolio_volatility = np.sqrt(portfolio_variance_value)

print(f"组合年化方差: {portfolio_variance_value:.8f}")
print(f"组合年化波动率: {portfolio_volatility:.6f} ({portfolio_volatility*100:.4f}%)")

# ==================== 步骤4：填充result字典 ====================

result = {
    'mvp_weights': w_final,  # numpy数组，三个权重值
    'mvp_vol_annual': portfolio_volatility  # 标量，年化波动率
}

print("\n=== 输出结果 ===")
print("result字典内容：")
for key, value in result.items():
    if key == 'mvp_weights':
        print(f"  {key}: {value}")
        print(f"    资产1权重: {value[0]:.6f}")
        print(f"    资产2权重: {value[1]:.6f}")
        print(f"    资产3权重: {value[2]:.6f}")
    else:
        print(f"  {key}: {value:.6f}")

# 额外展示：模拟有效前沿（可视化确认）
print("\n=== 有效前沿可视化 ===")

# 设置目标收益范围
target_returns = np.linspace(-0.05, 0.25, 100)

# 对于每个目标收益，求解最小方差组合
def min_variance_for_target_return(target_ret):
    # 需要各资产的预期收益（这里用简单假设）
    # 实际教学中，通常会给定或估计预期收益
    # 这里我们假设各资产预期收益与波动率成正比作为演示
    expected_returns = np.array([0.08, 0.10, 0.12])  # 假设的预期收益
    
    constraints = (
        {'type': 'eq', 'fun': lambda x: np.sum(x) - 1},  # 满仓
        {'type': 'eq', 'fun': lambda x: x @ expected_returns - target_ret}  # 目标收益
    )
    result = minimize(portfolio_variance, initial_guess, method='SLSQP',
                     bounds=bounds, constraints=constraints)
    return result.x, np.sqrt(result.fun)

# 计算有效前沿上的点
frontier_vols = []
valid_returns = []
mvp_return = w_final @ np.array([0.08, 0.10, 0.12])  # MVP对应的收益

for target_ret in target_returns:
    try:
        w_opt, vol = min_variance_for_target_return(target_ret)
        if vol > 0 and not np.isnan(vol):
            frontier_vols.append(vol)
            valid_returns.append(target_ret)
    except:
        continue

# 绘制有效前沿
plt.figure(figsize=(10, 6))
plt.plot(frontier_vols, valid_returns, 'b-', linewidth=2, label='有效前沿')
plt.scatter([portfolio_volatility], [mvp_return], color='red', s=100, 
            marker='*', label='全局最小方差组合 (MVP)', zorder=5)
plt.xlabel('年化波动率')
plt.ylabel('预期年化收益率')
plt.title('马科维茨有效前沿')
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.show()

print("脚本执行完成。")
