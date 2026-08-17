import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import minimize

# 设置参数
mu = np.array([0.071, 0.124])  # 期望年收益
sigma = np.array([0.163, 0.289])  # 年化波动率
rhos = [0.15, 0.45, 0.75]  # 相关系数

# 输出字典
result = {}

# 创建图形
plt.figure(figsize=(10, 6))

# 为每个相关系数绘制前沿
for rho in rhos:
    # 构造协方差矩阵
    cov_matrix = np.array([[sigma[0]**2, rho*sigma[0]*sigma[1]],
                           [rho*sigma[0]*sigma[1], sigma[1]**2]])
    
    # 计算最小方差组合（允许卖空，满仓约束）
    # 解析解：w_mvp = (inv(Σ)·1) / (1'·inv(Σ)·1)
    inv_cov = np.linalg.inv(cov_matrix)
    ones = np.ones(2)
    w_mvp = inv_cov @ ones / (ones @ inv_cov @ ones)
    mu_mvp = w_mvp @ mu
    sigma_mvp = np.sqrt(w_mvp @ cov_matrix @ w_mvp)
    
    # 如果是rho=0.45的情况，保存MVP波动率
    if rho == 0.45:
        result['mvp_vol_at_rho45'] = sigma_mvp
    
    # 扫描有效前沿
    target_returns = np.linspace(mu_mvp, max(mu), 200)
    frontier_vols = []
    
    for target_ret in target_returns:
        # 优化问题：最小化波动率，满足期望收益目标和满仓约束
        def objective(w):
            return np.sqrt(w @ cov_matrix @ w)
        
        constraints = [
            {'type': 'eq', 'fun': lambda w: w @ mu - target_ret},  # 收益约束
            {'type': 'eq', 'fun': lambda w: w.sum() - 1}  # 满仓约束
        ]
        
        # 初始猜测使用最小方差组合
        result_opt = minimize(objective, w_mvp, method='SLSQP', 
                            constraints=constraints, 
                            bounds=[(None, None), (None, None)],  # 允许卖空
                            options={'ftol': 1e-9})
        
        frontier_vols.append(result_opt.fun)
    
    frontier_vols = np.array(frontier_vols)
    
    # 绘制前沿曲线
    plt.plot(frontier_vols, target_returns, linewidth=2, 
             label=f'ρ = {rho}')
    
    # 标记最小方差组合
    plt.scatter(sigma_mvp, mu_mvp, color='red', s=100, zorder=5)
    plt.annotate(f'MVP (σ={sigma_mvp:.3f})', (sigma_mvp, mu_mvp), 
                xytext=(10, 10), textcoords='offset points', fontsize=9)

# 对rho=0.45计算目标期望收益10%下的最小波动率
target_ret_10 = 0.10
cov_matrix_rho45 = np.array([[sigma[0]**2, 0.45*sigma[0]*sigma[1]],
                              [0.45*sigma[0]*sigma[1], sigma[1]**2]])
inv_cov_rho45 = np.linalg.inv(cov_matrix_rho45)
ones = np.ones(2)
w_mvp_rho45 = inv_cov_rho45 @ ones / (ones @ inv_cov_rho45 @ ones)

# 优化目标收益为10%的组合
def objective(w):
    return np.sqrt(w @ cov_matrix_rho45 @ w)

constraints_10 = [
    {'type': 'eq', 'fun': lambda w: w @ mu - target_ret_10},
    {'type': 'eq', 'fun': lambda w: w.sum() - 1}
]

result_opt_10 = minimize(objective, w_mvp_rho45, method='SLSQP',
                        constraints=constraints_10,
                        bounds=[(None, None), (None, None)],
                        options={'ftol': 1e-9})

frontier_vol_at_target = result_opt_10.fun
result['frontier_vol_at_target'] = frontier_vol_at_target

# 打印计算结果
print("=== 相关系数 0.45 的计算结果 ===")
print(f"最小方差组合年化波动率: {result['mvp_vol_at_rho45']:.4f} ({result['mvp_vol_at_rho45']*100:.2f}%)")
print(f"目标期望收益 10% 的最小年化波动率: {result['frontier_vol_at_target']:.4f} ({result['frontier_vol_at_target']*100:.2f}%)")

# 添加图形元素
plt.xlabel('年化波动率', fontsize=12)
plt.ylabel('期望年收益', fontsize=12)
plt.title('马科维茨均值-方差前沿 (不同相关系数)', fontsize=14)
plt.grid(True, alpha=0.3)
plt.legend(loc='lower right')
plt.axis([0.0, 0.35, 0.06, 0.14])

# 添加目标收益线
plt.axhline(y=target_ret_10, color='gray', linestyle='--', alpha=0.5)
plt.text(0.30, target_ret_10+0.001, '10% 目标收益', fontsize=9)

# 保存图形
figure_path = 'mean_variance_frontier.png'
plt.savefig(figure_path, dpi=150, bbox_inches='tight')
result['figure_path'] = figure_path
print(f"\n图形已保存至: {figure_path}")

plt.show()

# 输出完整的result字典
print("\n=== 结果汇总 ===")
for key, value in result.items():
    print(f"{key}: {value}")
