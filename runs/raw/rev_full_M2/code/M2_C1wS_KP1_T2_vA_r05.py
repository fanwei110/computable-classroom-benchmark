import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import minimize

# 资产参数
mu = np.array([0.071, 0.124])  # 年期望收益
sigma = np.array([0.163, 0.289])  # 年化波动率
correlations = [0.15, 0.45, 0.75]
target_return = 0.10  # 目标收益 10%

# 结果存储
result = {}

# 绘图设置
fig, ax = plt.subplots(figsize=(10, 6))
colors = ['blue', 'orange', 'green']

# 全局最小方差组合函数（满仓约束：权重和为1）
def portfolio_volatility(weights, cov_matrix):
    return np.sqrt(weights.T @ cov_matrix @ weights)

def portfolio_return(weights, mu):
    return weights @ mu

def min_variance_portfolio(cov_matrix):
    """求解全局最小方差组合"""
    n = len(mu)
    # 目标函数：最小化方差
    fun = lambda w: w.T @ cov_matrix @ w
    # 约束：权重和为1
    cons = ({'type': 'eq', 'fun': lambda w: np.sum(w) - 1})
    # 边界：允许卖空？这里假设不允许卖空（长仓约束），但有效前沿通常允许卖空。
    # 为通用性，此处不做权重非负约束，仅做满仓约束。
    bounds = None  # 或无界
    # 初始猜测：等权重
    w0 = np.ones(n) / n
    res = minimize(fun, w0, method='SLSQP', constraints=cons, bounds=bounds)
    return res.x

def efficient_frontier(cov_matrix, mu, num_points=200):
    """生成有效前沿上的收益序列和对应的最小波动率（允许卖空）"""
    # 利用解析公式：有效前沿为双曲线，可在满仓约束下通过二次规划得到。
    # 这里采用数值方法：对每个目标收益，求解最小方差组合。
    target_returns = np.linspace(min(mu), max(mu), num_points)
    frontier_vols = []
    
    n = len(mu)
    # 约束：权重和为1，收益等于目标
    for r_target in target_returns:
        constraints = (
            {'type': 'eq', 'fun': lambda w: np.sum(w) - 1},
            {'type': 'eq', 'fun': lambda w: w @ mu - r_target}
        )
        fun = lambda w: w.T @ cov_matrix @ w
        w0 = np.ones(n) / n
        res = minimize(fun, w0, method='SLSQP', constraints=constraints, bounds=None)
        if res.success:
            frontier_vols.append(np.sqrt(res.fun))
        else:
            frontier_vols.append(np.nan)
    
    return target_returns, np.array(frontier_vols)

# 处理每个相关系数
for idx, rho in enumerate(correlations):
    # 构造协方差矩阵
    cov_matrix = np.array([
        [sigma[0]**2, rho * sigma[0] * sigma[1]],
        [rho * sigma[0] * sigma[1], sigma[1]**2]
    ])
    
    # 计算全局最小方差组合
    w_mvp = min_variance_portfolio(cov_matrix)
    mvp_ret = portfolio_return(w_mvp, mu)
    mvp_vol = portfolio_volatility(w_mvp, cov_matrix)
    
    # 生成有效前沿（允许卖空下的解析双曲线，覆盖包含最小方差组合的区间）
    # 为了完整展示，收益范围从MVP收益到略高于最高资产收益
    ret_range = np.linspace(min(mu), max(mu) + 0.01, 200)
    frontier_vols = []
    
    for r_target in ret_range:
        constraints = (
            {'type': 'eq', 'fun': lambda w: np.sum(w) - 1},
            {'type': 'eq', 'fun': lambda w: w @ mu - r_target}
        )
        fun = lambda w: w.T @ cov_matrix @ w
        w0 = np.ones(2) / 2
        res = minimize(fun, w0, method='SLSQP', constraints=constraints, bounds=None)
        if res.success:
            frontier_vols.append(np.sqrt(res.fun))
        else:
            frontier_vols.append(np.nan)
    frontier_vols = np.array(frontier_vols)
    
    # 绘制有效前沿
    ax.plot(frontier_vols, ret_range, color=colors[idx], label=f'$\\rho$ = {rho}')
    
    # 标出最小方差组合
    ax.scatter(mvp_vol, mvp_ret, color=colors[idx], marker='o', s=60, zorder=5)
    # 添加注释
    ax.annotate(f'MVP\n(vol={mvp_vol:.3f})',
                xy=(mvp_vol, mvp_ret),
                xytext=(mvp_vol + 0.005, mvp_ret - 0.003),
                arrowprops=dict(arrowstyle='->', color=colors[idx]),
                fontsize=8, color=colors[idx])
    
    # 存储ρ=0.45时的结果
    if rho == 0.45:
        result['mvp_vol_at_rho45'] = mvp_vol
        # 计算目标收益10%时的最小波动率
        # 再次精确求解
        constraints = (
            {'type': 'eq', 'fun': lambda w: np.sum(w) - 1},
            {'type': 'eq', 'fun': lambda w: w @ mu - target_return}
        )
        fun = lambda w: w.T @ cov_matrix @ w
        w0 = np.ones(2) / 2
        res_target = minimize(fun, w0, method='SLSQP', constraints=constraints, bounds=None)
        if res_target.success:
            frontier_vol_at_target = np.sqrt(res_target.fun)
        else:
            frontier_vol_at_target = np.nan
        result['frontier_vol_at_target'] = frontier_vol_at_target

# 图表装饰
ax.set_xlabel('Portfolio Volatility (Std Dev)', fontsize=12)
ax.set_ylabel('Expected Return', fontsize=12)
ax.set_title('Efficient Frontier for Two Assets under Different Correlations', fontsize=14)
ax.legend(loc='lower right')
ax.grid(True, linestyle='--', alpha=0.6)

# 保存图形
figure_path = 'efficient_frontier.png'
plt.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close()

result['figure_path'] = figure_path

# 打印结果
print("结果字典:", result)
print(f"ρ=0.45时最小方差组合波动率: {result['mvp_vol_at_rho45']:.4f}")
print(f"ρ=0.45、目标收益10%时最小波动率: {result['frontier_vol_at_target']:.4f}")
print(f"图形已保存至: {result['figure_path']}")
